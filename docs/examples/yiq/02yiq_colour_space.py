""" Construction yiq colour space

Parameters
----------
None

Results
-------
image
"""

from PIL import Image,ImageDraw

def yiq_to_rgb(y, i, q):
    """Conversion yiq to rgb
        incoming y 0 to 100, i, q ±100
        
    Parameters
    ----------
    y : str
        luma
    i : str
        chrominance
    q : str
        chrominance
    
    Returns
    -------
    tuple of integers
    """
    
    # assume I and Q between ±1, correct for colorsys
    y=min(max(y,0),100)
    i=min(max(i,-100),100)
    q=min(max(q,-100),100)
    y=y/100
    i=0.599*i/100
    q=0.5251*q/100

    r = y + 0.9468822170900693*i + 0.6235565819861433*q
    g = y - 0.27478764629897834*i - 0.6356910791873801*q
    b = y - 1.1085450346420322*i + 1.7090069284064666*q
    r=min(max(r,0),1)
    g=min(max(g,0),1)
    b=min(max(b,0),1)

    return (int(r*255+0.5), int(g*255+0.5), int(b*255+0.5))

im = Image.new("RGB", (301,301), "#FFFFFF")
centre = 301//2,301//2
pix = im.load()

for x in range(im.width):
    for y in range(im.height):
        i=(x-150)*2/3
        q=(y-150)*2/3
        pix[x,y]=yiq_to_rgb(50,i,q)

im.save('../../figures/colour_space.png')