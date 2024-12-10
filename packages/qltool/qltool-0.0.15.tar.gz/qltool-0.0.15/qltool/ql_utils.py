#!/usr/bin/env python3

from fire import Fire

import tempfile
import os
import subprocess as sp
import shlex
import random

import numpy as np
import cv2
import screeninfo
from flashcam import usbcheck

import socket
import glob

from  PIL import Image
from PIL import Image, ImageDraw, ImageFont
import math


def main():
    print()


def runme(CMDi, silent = False):
    """
    run with the help of safe shlex
    """
    print("_"*(70-len(CMDi)), CMDi)
    CMD = shlex.split(CMDi)# .split()
    res=sp.check_output( CMD ).decode("utf8")
    if not silent:
        print("i... RESULT:", res)
        #print("#"*70)
    return res



def get_tmp():
    """
    the printer understands to PNG
    """
    suffix = '.png'
    tmp_dir = '/tmp'
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix, dir=tmp_dir, delete=False)
    temp_filename = temp_file.name
    temp_file.close()
    return temp_filename


def get_width(IMG):
  width=f"identify -format %w {IMG}"
  res = runme(width, silent = True).strip()
  res = int(res)
  #print(f"i... image width=/{res}/")
  return res


def get_height(IMG):
  height = f"identify -format %h {IMG}"
  res = runme(height, silent = True).strip()
  res = int(res)
  #print(f"i... image height=/{res}/")
  return res




def guess_points(IMG):
    """
    466 x 624 image has 32 points.....
    """
    WIDTH = get_width(IMG)
    HEIGHT = get_height(IMG)
    #linear:
    #res = 32 * (WIDTH/466)
    res = 68 * (WIDTH/1000)
    return res




def dither(IMG, percent=50):
        #width = 707-10
    OUTPUT = get_tmp()
    #CMD="-auto-level  -scale "+str(width)+"x   -monochrome -dither FloydSteinberg  -remap pattern:gray50  "+OUTPUT
    CMD=f"convert {IMG} -auto-level   -monochrome -dither FloydSteinberg  -remap pattern:gray{percent}  {OUTPUT}"
    runme(CMD)
    return OUTPUT




def monochrom(IMG):
        #width = 707-10
    OUTPUT = get_tmp()
    CMD=f"convert {IMG}   -monochrome  {OUTPUT}"  # soft...
    #CMD=f"convert {IMG}   -threshold 50%  {OUTPUT}" # real brutal
    runme(CMD)
    return OUTPUT



def rotate_img(IMG):
    OUTPUT = get_tmp()
    CMD = f"convert {IMG} -rotate 90 {OUTPUT}"
    runme(CMD)
    return OUTPUT



def resize_img(IMG, factor = 0.5):
    OUTPUT = get_tmp()
    CMD = f"    convert {IMG}    -resize {round(factor*100)}%   {OUTPUT}"
    runme(CMD)
    return OUTPUT

def rescale_img(IMG, maxw = 714):
    """
    62x   brother  eats 714 px width, then it can crash
    """
    OUTPUT = get_tmp()
    CMD = f"    convert {IMG}    -resize x{maxw}   {OUTPUT}"
    runme(CMD)
    return OUTPUT





def annotate_img(IMG, north=" ", south=" ",  points = None):
    """
    points is override for guess_points
    """
    WIDTH = get_width(IMG)
    HEIGHT = get_height(IMG)
    OUTPUTN = get_tmp()
    OUTPUTS = get_tmp()
    OUTPUT = get_tmp()

    POINTS = guess_points(IMG)
    if points is not None:
        POINTS = points

    IMN=""
    IMS=""
    if north is not None and len(north.strip())>0:
        #CMD = f"convert -background white -fill black -gravity center -size {WIDTH}x label:{north} NORTH.png"
        CMD = f"convert -background white -fill black -gravity center -pointsize {POINTS} -size {WIDTH}x{POINTS}  label:'{north}' {OUTPUTN}"
        runme(CMD)
        IMN=OUTPUTN#"NORTH.png"
    if south is not None and len(south.strip())>0:
        #CMD = f"convert -background white -fill black -gravity center -size {WIDTH}x label:{south} SOUTH.png"
        CMD = f"convert -background white -fill black -gravity center -pointsize {POINTS} -size {WIDTH}x{POINTS}  label:'{south}' {OUTPUTS}"
        runme(CMD)
        IMS=OUTPUTS#"SOUTH.png"
    CMD = f'montage -geometry +0+0 -set label "" -tile 1x {IMN} {IMG} {IMS} {OUTPUT}'
    runme(CMD)


    WIDTH = get_width(OUTPUT)
    HEIGHT = get_height(OUTPUT)
    print("i... +++++++++++++++++++++++++++++++++++++++++++++++++++++annotate" )
    print("i... HEIGHT==",HEIGHT)
    print("i... WIDTH==",WIDTH)
    print(OUTPUT)
    print("i... +++++++++++++++++++++++++++++++++++++++++++++++++++++annotate" )
    return OUTPUT







def make_triple(fname, nlabel=None, slabel=None, midlabel=None, destination='/tmp/qr_tripled.png'):
    """
    This make 4 images in a row, 1st one is QR.
    """
    OUTIMG = destination
    # Load the QR image - can be various sizes....  AND ALWAYS CONVERT TO 570
    qr_image = Image.open( fname ).resize((570, 570))
    width, height = qr_image.size
    #print(width, height)
    border = 9 # ?I guess a nice value for convert.....

    # # trick to fins fontsize ------------------- NON O NO
    # draw = ImageDraw.Draw(qr_image)
    # font_size = 1
    # font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    # font = ImageFont.truetype( font_path, font_size)
    # text = nlabel
    # if text is not None and slabel is not None and len(text) < len(slabel):
    #     text = slabel
    # text_width, text_height = draw.textsize(text, font=font)
    # while text_width < (width - 2 * border):
    #     font_size += 1
    #     font = ImageFont.truetype(font_path, font_size)
    #     text_width, text_height = draw.textsize(text, font=font)
    # font_size -= 1  # Adjust to the last fitting size


    # Create blank white images
    blank_image1 = Image.new('RGB', (width, height), 'white')
    blank_image2 = Image.new('RGB', (width, height), 'white')
    blank_image3 = Image.new('RGB', (width, height), 'white')

    # Create a new image with the combined width
    combined_width = width * 4
    combined_image = Image.new('RGB', (combined_width, height))

    # Paste the images into the combined image
    combined_image.paste(qr_image, (0, 0))
    combined_image.paste(blank_image1, (width, 0))
    combined_image.paste(blank_image2, (width * 2, 0))
    combined_image.paste(blank_image3, (width * 3, 0))

    if nlabel is not None and slabel is not None:
        IMG1 = '/tmp/qr_tripled1.png'
        combined_image.save(IMG1)
        OUTPUTN = get_tmp()
        #CMD = f"convert -background white -fill black -gravity center -pointsize {POINTS} -size {WIDTH}x{POINTS}  label:'{nlabel}' {OUTPUTN}"
        #CMD = f'convert {IMG1}  -gravity northwest -pointsize 40 -fill black  -annotate +%[fx:w/3+10]+%[fx:h/2-40] "nlabel"  -annotate +%[fx:w/3+10]+%[fx:h/2+10] "slabel" {OUTIMG}'
        fsize = 100 # BIG letter - i fit 1234567890123456789
        print(len(slabel), slabel)
        print(len(nlabel), nlabel)
        print(len(midlabel), midlabel)
        mwid = max(len(slabel), len(nlabel) )
        mwid = max(mwid, len(midlabel) )
        # --- adapt fonts to smaller size
        """
        31  97
        32  92
        33  89
        34  87
        35  84
        36  83
        37  81
        38  78
        39  76
        40  74
        41  72
        42  70
        43  69
        45   65
        48  62
        51  58
        54 55import matplotlib.pyplot as plt
import numpy as np
import fire

def plot_graph_with_quadratic_fit():
    x = np.array([31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 48, 51, 54])
    y = np.array([97, 92, 89, 87, 84, 83, 81, 78, 76, 74, 72, 70, 69, 65, 62, 58, 55])

    # Perform quadratic fit
    coefficients = np.polyfit(x, y, 2)
    quadratic_fit = np.poly1d(coefficients)

    # Print coefficients
    print("Quadratic Fit Coefficients:", coefficients)

    # Plot data points
    plt.plot(x, y, 'o', label='Data points')

    # Plot quadratic fit
    x_fit = np.linspace(min(x), max(x), 100)
    plt.plot(x_fit, quadratic_fit(x_fit), '-', label='Quadratic fit')

    # Add coefficients to the plot
    plt.text(0.05, 0.95, f'Coefficients:\n{coefficients[0]:.2f}x² + {coefficients[1]:.2f}x + {coefficients[2]:.2f}',
             transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of y vs. x with Quadratic Fit')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    fire.Fire(plot_graph_with_quadratic_fit)

        """
        if mwid >= 30: # ---------------------- Modify the font size
            fsize = 55 # finish at 55 characters.....
            if mwid < 55:
                fsize = int(0.045166 * mwid * mwid - 5.5735 * mwid + 224.7)
            print(f"D... making font smaller:  maxWid=={mwid}  makes font to ==> {fsize}  (55 IS MAX  ALLOWED) ")

        print("_____________________________________________________FSIZE== ", fsize, "   #", mwid)
        # CMD =f'convert {IMG1}  -gravity NorthWest -pointsize {fsize} -annotate +{width}+50 "{nlabel}"  -gravity SouthWest -pointsize {fsize} -annotate +{width}+50   "{slabel}"  {OUTIMG}'
        # ---------------------- Modify the font size
        if midlabel is None: midlabel = "*"
        if slabel is None: slabel = "*"
        if nlabel is None: nlabel = "*"
        CMD =f'convert {IMG1}  -gravity SouthWest -pointsize {fsize} -annotate +{width}+{int(height*0.8)} "{nlabel}"  -gravity SouthWest -pointsize {fsize} -annotate +{width}+{height//2} "{midlabel}"  -gravity SouthWest -pointsize {fsize} -annotate +{width}+0  "{slabel}"  {OUTIMG}'

        print(CMD)
        runme(CMD)
    else:
        # Save the combined image
        combined_image.save(OUTIMG)
    return OUTIMG




def make_double(fname, nlabel=None, slabel=None, destination='/tmp/qr_tripled.png'):
    """
    This make 3 images in a row, 1st one is QR.
    """

    OUTIMG = destination #'/tmp/qr_tripled.png'
    # Load the QR image
    qr_image = Image.open( fname )

    # Create blank white images
    width, height = qr_image.size
    blank_image1 = Image.new('RGB', (width, height), 'white')
    #blank_image2 = Image.new('RGB', (width, height), 'white')
    #blank_image3 = Image.new('RGB', (width, height), 'white')

    # Create a new image with the combined width
    combined_width = width * 2
    combined_image = Image.new('RGB', (combined_width, height))

    # Paste the images into the combined image
    combined_image.paste(qr_image, (0, 0))
    combined_image.paste(blank_image1, (width, 0))
    #combined_image.paste(blank_image2, (width * 2, 0))
    #combined_image.paste(blank_image3, (width * 3, 0))

    if nlabel is not None and slabel is not None:
        IMG1 = '/tmp/qr_tripled1.png'
        combined_image.save(IMG1)
        OUTPUTN = get_tmp()
        #CMD = f"convert -background white -fill black -gravity center -pointsize {POINTS} -size {WIDTH}x{POINTS}  label:'{nlabel}' {OUTPUTN}"
        CMD = f'convert {IMG1}  -gravity northwest -pointsize 40 -fill black  -annotate +%[fx:w/3+10]+%[fx:h/2-40] "nlabel"  -annotate +%[fx:w/3+10]+%[fx:h/2+10] "slabel" {OUTIMG}'
        fsize = 80
        mwid = max(len(slabel), len(nlabel))
        if mwid > 20:
            fsize = int(fsize / (mwid / 20))
            fsize = max( 55, fsize )
            print(f"D... makeing font smaller 80 ==> {fsize}")
        CMD =f'convert {IMG1}  -gravity NorthWest -pointsize {fsize} -annotate +{width}+50 "{nlabel}"  -gravity SouthWest -pointsize {fsize} -annotate +{width}+50   "{slabel}"  {OUTIMG}'

        print(CMD)
        runme(CMD)
    else:
        # Save the combined image
        combined_image.save(OUTIMG)
    return OUTIMG

# ***************************************************

def check_lpx():
    prs = glob.glob("/dev/usb/lp*")
    print(prs)
    return prs[0]





def main():
    print()



if __name__=="__main__":
    Fire(main)
