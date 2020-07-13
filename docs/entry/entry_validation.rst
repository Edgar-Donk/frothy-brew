Entry Validation
================

Central to our task is determining whether the user input is valid or not. 
Tkinter provides validatation tools, generally both tkinter and ttk entry
widgets react in the same way. We shall use ttk as it continues to validate
without having to be reset. By the way the same system can be used for both 
the spinbox and combobox.

There are 3 options used for entry validation, ``validate`` together with
``validatecommand`` and ``invalidcommand``. Before a validatecommand 
or invalidcommand can be used it first of all must be registered, 
creating a TCL wrapper. These options point to a callback function that 
checks the input and returns a **True** or **False**, if **True** then the 
input is made otherwise the input is blocked. 

.. important:: Every check in the callback function can only return **True** or 
    **False** otherwise the validation stops working.

Validate Options
----------------

Validate has the following options.

.. csv-table::
   :file: ../csv/validate_options.csv
   :header-rows: 1
   :widths: 10, 65

.. note:: The last option is ``none``, not to be confused with the reserved
    word ``None``.

Validatecommand and Invalidcommand Options
------------------------------------------

The commands can take the following substitution codes, as enhancements to
the callback function.

.. csv-table::
   :file: ../csv/command_options.csv
   :header-rows: 1
   :delim: ;
   :widths: 15, 65

Methods Used with Validation
----------------------------

The three most important types of input, string, integer and float, will be dealt 
within the this section. Within Colour Picker :ref:`mod-entry` is shown how to 
deal with a hexadecimal input. In the colour picker you will also see that 
we can check limits when different widgets use the same validation function. 
As with most functions we need only refer to the actual validation parameters 
we are actually using.

As we are validating simple options the **validate** function method together 
with **key** is used and the **validatecommand**. Within these scripts the 
following aliases are used :-

text  %P 
    The value of the entry if the edit is allowed
input  %S 
    The text string being inserted/deleted
index  %i 
    Index of char string to be inserted/deleted
action  %d 
    Type of action: 1 for insert, 0 for delete, or -1 for focus, forced or 
    textvariable validation


    