#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd3in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import argparse
from pathlib import Path
logging.basicConfig(level=logging.DEBUG)

threshold=[63, 126, 189]

def output(img_path):
    try:
        logging.info("epd3in7 Demo")
        epd = epd3in7.EPD()
        logging.info("init and Clear")
        epd.init(0)
        epd.Clear(0xFF, 0)
        
        logging.info("read 4 Gray bmp file")

        img_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), img_path)
        filename = os.path.basename(img_file)
        target_file = os.path.join(os.path.dirname(img_file), "target."+filename)
        targetImg=convert(mode="L2", source=img_file, target=target_file, width=epd.width, height=epd.height,dither=True)
        epd.display_4Gray(epd.getbuffer_4Gray(targetImg))
        
        logging.info("Goto Sleep...")
        epd.sleep()
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd3in7.epdconfig.module_exit()
        exit()

def thr(px):
    if px < threshold[0]:
        return 0
    elif threshold[0] <= px < threshold[1]:
        return 85
    elif threshold[1] <= px < threshold[2]:
        return 170
    else:
        return 255

def convert(mode, source, target, width, height, dither):
    data_bw = None
    data_red = None

    img = Image.open(source)

    # Get rid of alpha and change it to white.
    if img.mode == "RGBA":
        tmp = Image.new("RGBA", img.size, "WHITE")
        tmp.paste(img, mask=img)
        img = tmp.convert("RGB")

    # Scale image according to provided arguments.
    if width is not None and height is not None:
        img = img.resize((width, height))
        print(f"Scaled to {width}x{height}")
    elif width is not None:
        w, h = img.size
        ratio = h / w
        img = img.resize((width, int(width * ratio)))
        print(f"Scaled uniformly to: {width}x{int(width * ratio)}")
    elif height is not None:
        w, h = img.size
        ratio = w / h
        img = img.resize((int(height * ratio), height))
        print(f"Scaled uniformly to: {int(height * ratio)}x{height}")
    else:
        pass

    # Pad image to make width divisible by 8.
    w, h = img.size
    if w % 8 != 0:
        w = w + 8 - w % 8
        print(f"Image width not divisible by 8. Padded to width: {w}")
        tmp = Image.new(img.mode, (w, h), (255, 255, 255))
        tmp.paste(img)
        img = tmp

    # BW image conversion.
    if mode == "L1":
        if dither:
            # Using "1" mode with dithering gives better results.
            img = img.convert("1").point(lambda p: p > threshold[0] and 255)
            # # In this mode data match FrameBuffer HLSB format, no need for further processing.
            # data_bw = bytearray(img.tobytes())
        else:
            # Using "L" mode makes thresholding easier.
            img = img.convert("L").point(lambda p: p > threshold[0] and 255)

            # Convert pixel data to HLSB format.
            # img_data = img.tobytes()
            # data_bw = bytearray(w * h // 8)
            # for byte in range(w * h // 8):
            #     pixels = img_data[byte * 8:(byte + 1) * 8]
            #     tmp = 0
            #     for i, v in enumerate(pixels):
            #         tmp |= (v & 0x1) << (7 - i)
            #     data_bw[byte] = tmp

    # 4 level grayscale conversion.
    else:
        # Converting to "P" mode first allows dithering.
        img = img.convert("P", dither=Image.FLOYDSTEINBERG if dither else Image.NONE).convert("L").point(thr)

        # # Convert pixel data to bytearrays for BW and RED RAMs in HLSB format.
        # data_bw = bytearray(w * h // 8)
        # data_red = bytearray(w * h // 8)
        # img_data = img.tobytes()
        # for byte in range(w * h // 8):
        #     pixels = img_data[byte * 8:(byte + 1) * 8]
        #     tmp_bw = 0
        #     tmp_red = 0
        #     for i, v in enumerate(pixels):
        #         tmp_bw |= (v & 0x1) << (7 - i)
        #         tmp_red |= ((v >> 1) & 0x1) << (7 - i)
        #     data_bw[byte] = tmp_bw
        #     data_red[byte] = tmp_red
    return img

if __name__ == '__main__':
    print('######################################')

    parser = argparse.ArgumentParser(
        description='output img to e-paper display',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-f', '--img_file', required=True)      # option that takes a value
    args = parser.parse_args()
    result = []
    output(args.img_file)
    
