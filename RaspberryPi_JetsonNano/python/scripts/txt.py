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
import math
logging.basicConfig(level=logging.DEBUG)

threshold=[63, 126, 189]

def output(txt_path):
    try:
        logging.info("epd3in7 Demo")
        epd = epd3in7.EPD()
        logging.info("init and Clear")
        epd.init(0)
        epd.Clear(0xFF, 0)
        
        Himage = Image.new('L', (epd.height, epd.width), 0xFF)  # 0xFF: clear the frame
        draw = ImageDraw.Draw(Himage)
        txt_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), txt_path)
        txtFile = open(txt_file, "r")
        lines = txtFile.readlines()
        line_cnt = len(lines)
        font_size = math.floor(epd.width/line_cnt/12)*12
        font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), font_size)

        index = 0
        w_padding = 10
        h_padding = 10
        line_indent = 5
        for line in lines:
            # line = line.strip()
            line_start_x = w_padding
            line_start_y = h_padding + index * (font_size + line_indent)
            draw.text(xy=(line_start_x, line_start_y), text=line,font=font,align='left',fill=epd.GRAY4)
            index = index+1
        epd.display_4Gray(epd.getbuffer_4Gray(Himage))
        
        logging.info("Goto Sleep...")
        epd.sleep()
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd3in7.epdconfig.module_exit()
        exit()


if __name__ == '__main__':
    print('######################################')

    parser = argparse.ArgumentParser(
        description='output img to e-paper display',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-f', '--txt_file', required=True)      # option that takes a value
    args = parser.parse_args()
    output(args.txt_file)
    
