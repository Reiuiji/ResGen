#!/bin/python
#Outputs svg image with the correct color codes
import re
import os

SVGFILE="4-Band_Resistor.svg"
RESFILE="resvalues.txt"
SVGDIR="svg"

COLORS={
		0:"BLACK",
        1:"BROWN",
        2:"RED",
        3:"ORANGE",
        4:"YELLOW",
        5:"GREEN",
        6:"BLUE",
        7:"VIOLET",
        8:"GREY",
        9:"WHITE"
		}

COLORCODES={
		"BLACK":"000000",
        "BROWN":"663332",
        "RED":"fe0000",
        "ORANGE":"ff6600",
        "YELLOW":"ffff01",
        "GREEN":"33cc33",
        "BLUE":"6766ff",
        "VIOLET":"cd66ff",
        "GREY":"939393",
        "WHITE":"ffffff",
        "GOLD":"cb9a34",
        "SILVER":"cccccc"
		}

def mdecode(value):
    if value == "0":
        return 1
    elif value == "k":
        return 3
    elif value == "M":
        return 6
    else:
        return 0


#decode input values and return color code
def colordecode(value):
    #val = re.split('(\d*)',value) #break apart any k or M "15K"
    multiplier = 0
    tolerance = "5%"
    print("Reading Value: " + str(value) + " | len:" + str(len(value)))
    if len(value) == 2:# ## two digit
        band1 = int(value[0])
        band2 = int(value[1])
    elif len(value) == 3:
        band1 = int(value[0])
        band2 = int(value[1])
        multiplier = mdecode(value[2])
    elif len(value) == 4:
        band1 = int(value[0])
        if value[1] == ".":
            offset = 1
            band2 = int(value[2])
            multiplier = mdecode(value[3])
        else:
            band2 = int(value[1])
            multiplier = mdecode(value[2]) + mdecode(value[3])
    else:
        return ["GOLD","GOLD","GOLD","GOLD"] #Error values

    return [COLORS[band1],COLORS[band2],COLORS[multiplier],"GOLD"]


def colorgen(value):
    band = colordecode(value)
    with open(SVGFILE, "r") as svg:
        lines = svg.readlines()
    svg.close()

    #edit color codes
    for pos in range(len(lines)):
        lines[pos] = re.sub(r'111111', COLORCODES[band[0]], lines[pos])
        lines[pos] = re.sub(r'222222', COLORCODES[band[1]], lines[pos])
        lines[pos] = re.sub(r'333333', COLORCODES[band[2]], lines[pos])
        lines[pos] = re.sub(r'444444', COLORCODES[band[3]], lines[pos])
        lines[pos] = re.sub(r'@', str(value), lines[pos])

    with open(SVGDIR + "/" + str(value) + ".svg", "w") as f:
        for line in lines:
            f.write(line)

def setup():
    if not os.path.exists(SVGDIR):
        print("Create Dir: " + os.getcwd() + "/" + SVGDIR)
        os.mkdir(SVGDIR)


def main():
    setup()
    with open(RESFILE, "r") as f:
        lines = f.readlines()
    f.close()

    for line in lines:
        colorgen(str(line.rstrip('\n')))

#Main Run routine
if __name__ == "__main__":
    main()
