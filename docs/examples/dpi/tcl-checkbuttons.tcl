#!/usr/bin/tclsh
#
# Copyright 2018 Brad Lanam Walnut Creek, CA
#

package require Tk

proc scheckbutton { nm args } {
  scbwidget new $nm {*}$args
  return $nm
}

namespace eval ::scbcmd {
  variable vars

  proc handler { w args } {
    $w {*}$args
  }

  proc initializeAll { } {
    variable vars

    if { [info exists ::scbcmd::initialized] } {
      return
    }
    set ::scbcmd::initialized true

    set tbg [ttk::style lookup TFrame -background]
    if { $::tcl_platform(os) eq "Darwin" } {
      # this isn't going to work...
      set tbg #ececec
    }
    lassign [winfo rgb . $tbg] bg_r bg_g bg_b
    '''
    set bg [format {%02x%02x%02x} \
        [expr {$bg_r / 256}] \
        [expr {$bg_g / 256}] \
        [expr {$bg_b / 256}]]
    '''
    ttk::style configure SCheckbutton.TFrame \
        -background $bg
    ttk::style configure SCheckbutton.TLabel \
        -anchor e \
        -width {} \
        -background $bg \
        -highlightthickness 0
    ttk::style configure Indicator.SCheckbutton.TLabel \
        -anchor {}
  }
}

::oo::class create ::scbwidget {
  constructor { nm args } {
    my variable vars

    ::scbcmd::initializeAll

    #
    set vars(ind.styles) {
        1 {chars {\u2610 \u2611} padding {0 0 0 0}}
        2 {chars {\u2610 \u2612} padding {0 0 0 0}}
        3 {chars {\u25ab \u25aa} padding {0 0 0 3}}
        4 {chars {\u25a1 \u25a0} padding {0 0 0 3}}
        5 {chars {\u25a1 \u25a3} padding {0 0 0 4}}
        6 {chars {\u25fb \u25fc} padding {0 0 0 3}}
        7 {chars {\u25fd \u25fe} padding {0 0 0 3}}
        }
    set vars(max.style) 7
    set vars(char.off) \u2610
    set vars(char.on) \u2611
    set vars(char.disp) $vars(char.off)
    set vars(-indicatorstyle) 1
    set vars(-indicatorcolor) {}
    set vars(-onvalue) 1
    set vars(-offvalue) 0
    set vars(currvalue) 0
    set vars(currstate) {}
    set vars(curr.value.state) off
    set vars(-command) {}
    set vars(font.basesize) 11

    # some defaults

    set vars(frame.cont) [ttk::frame $nm \
        -class Scaled.checkbutton \
        -style SCheckbutton.TFrame \
        ]
    set vars(widget) [ttk::label $nm.indicator \
        -style Indicator.SCheckbutton.TLabel \
        -textvariable [self]::vars(char.disp) \
        ]
    $vars(widget) configure -style 1.Indicator.SCheckbutton.TLabel
    set vars(label) [ttk::label ${nm}.label \
        -style SCheckbutton.TLabel \
        ]
    set vars(scb) ${nm}_scb
    rename $vars(frame.cont) ::$vars(scb)
    interp alias {} $vars(frame.cont) {} ::scbcmd::handler [self]
    uplevel 2 [list $vars(frame.cont) configure {*}$args]

    set vars(bind.tag) scbbt$vars(widget)
    bindtags $vars(widget) [concat [bindtags $vars(widget)] $vars(bind.tag)]

    grid $vars(widget) $vars(label) -in $vars(frame.cont) \
        -sticky {} -padx 0 -pady 0
    grid configure $vars(label) -sticky e
    grid configure $vars(label) -ipadx 1p

    # make sure any binds on the main hull get propagated to the display widget
    set bt [bindtags $vars(widget)]
    bindtags $vars(widget) [list $nm {*}$bt]

    bind $vars(widget) <Destroy> [list [self] destruct]

    bind $vars(widget) <ButtonRelease-1> +[list [self] setvalue]
    bind $vars(label) <ButtonRelease-1> +[list [self] setvalue]
    my adjustpadding
  }

  method adjustpadding { } {
    my variable vars

    set style [$vars(label) cget -style]
    set font [$vars(label) cget -font]
    if { $font eq {} } { set font TkDefaulFont }

    dict for {key info} $vars(ind.styles) {
      set opad [dict get $info padding]
      set sz [font metrics $font -ascent]
      set adj [expr {double($sz)/$vars(font.basesize)}]
      set npad [list]
      foreach {p} $opad {
        set np [expr {round(double($p)*$adj)}]
        lappend npad $np
      }

      ttk::style configure $key.Indicator.$style -padding $npad
      if { $vars(-indicatorcolor) ne {} } {
        set discolor [ttk::style lookup $style -foreground disabled #a3a3a3]
        ttk::style configure $key.Indicator.$style \
            -foreground $vars(-indicatorcolor)
        ttk::style map $key.Indicator.$style \
            -foreground [list disabled $discolor readonly $discolor]
      }
    }
  }

  method destruct { } {
    my variable vars
    interp alias {} $vars(frame.cont) {}
    [self] destroy
  }

  method setvalue { } {
    my variable vars

    if { [$vars(widget) instate readonly] } {
      return
    }
    if { [$vars(widget) instate disabled] } {
      return
    }

    if { $vars(curr.value.state) } {
      set vars(curr.value.state) off
    } else {
      set vars(curr.value.state) on
    }
    set k -variable
    if { [info exists vars($k)] && [info exists $vars($k)] } {
      if { $vars(curr.value.state) } {
        set $vars($k) $vars(-onvalue)
      } else {
        set $vars($k) $vars(-offvalue)
      }
    }
    my checkvalue
    if { $vars(-command) ne {} } {
      {*}$vars(-command)
    }
  }

  method checkvalue { args } {
    my variable vars

    set k -variable
    if { [info exists vars($k)] && [info exists $vars($k)] } {
      if { [set $vars($k)] eq $vars(-onvalue) } {
        set vars(curr.value.state) on
      } else {
        set vars(curr.value.state) off
      }
    }
    if { $vars(curr.value.state) } {
      set vars(char.disp) $vars(char.on);
    } else {
      set vars(char.disp) $vars(char.off);
    }
  }

  method starttrace { } {
    my variable vars

    set k -variable
    if { [info exists vars($k)] && [info exists $vars($k)] } {
      trace add variable $vars($k) write [list [self] checkvalue]
    }
  }

  method unknown { args } {
    my variable vars

    if { [lindex $args 0] eq "instate" && [llength $args] == 2 } {
      return [uplevel 2 [list $vars(widget) {*}$args]]
    }
    if { [lindex $args 0] eq "state" && [llength $args] == 2 } {
      uplevel 2 [list $vars(label) {*}$args]
      return [uplevel 2 [list $vars(widget) {*}$args]]
    }
    return [uplevel 2 [list $vars(label) {*}$args]]
  }

  method cget { key } {
    my variable vars

    set rv {}
    if { $key eq "-variable" ||
        $key eq "-indicatorcolor" ||
        $key eq "-indicatorstyle" ||
        $key eq "-command" ||
        $key eq "-onvalue" ||
        $key eq "-offvalue" } {
      set rv $vars($key)
    } else {
      set rv [$vars(label) cget $key]
    }
    return $rv
  }

  method configure { args } {
    my variable vars

    foreach {key val} $args {
      if { $key eq "-indicatorstyle" } {
        if { ! [string is entier $val] || $val < 1 || $val > $vars(max.style) } {
          return
        }
        set vars(-indicatorstyle) $val
        lassign [dict get $vars(ind.styles) $val chars] \
            vars(char.off) vars(char.on)
        set style [$vars(label) cget -style]
        $vars(widget) configure -style $val.Indicator.$style
        set vars($key) $val
      } elseif { $key eq "-command" ||
          $key eq "-onvalue" ||
          $key eq "-offvalue" ||
          $key eq "-indicatorcolor" } {
        set vars($key) $val
      } elseif { $key eq "-variable" } {
        set fqv {}
        if { [string match {::*} $val] } {
          set fqv $val
        }
        if { $fqv eq {} } {
          set fqv [uplevel 2 [list namespace which -variable $val]]
          if { $fqv eq {} } {
            set ns [uplevel 2 [list namespace current]]
            set fqv $ns$val
            if { [string match ::::* $fqv] } {
              set fqv [string range $fqv 2 end]
            }
          }
        }
        set vars($key) $fqv
        if { ! [info exists $vars($key)] } {
          set $vars($key) {}
        }
        my starttrace
      } elseif { $key eq "-style" } {
        $vars(label) configure -style $val
        $vars(widget) configure -style $vars(-indicatorstyle).Indicator.$val
      } else {
        uplevel 2 [list $vars(label) configure $key $val]
      }
    }
    my checkvalue
    my adjustpadding
    return -code ok
  }
}

package provide scheckbutton 1.2
