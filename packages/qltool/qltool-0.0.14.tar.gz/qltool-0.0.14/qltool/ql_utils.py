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







def make_triple(fname, nlabel=None, slabel=None, destination='/tmp/qr_tripled.png'):

    OUTIMG = destination
    # Load the QR image
    qr_image = Image.open( fname )

    # Create blank white images
    width, height = qr_image.size
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




def make_double(fname, nlabel=None, slabel=None, destination='/tmp/qr_tripled.png'):

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
