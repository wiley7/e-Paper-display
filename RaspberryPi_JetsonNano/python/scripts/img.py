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

def output(img_path):
    try:
        logging.info("epd3in7 Demo")
        epd = epd3in7.EPD()
        logging.info("init and Clear")
        epd.init(0)
        epd.Clear(0xFF, 0)
        
        logging.info("read 4 Gray bmp file")
        Himage = Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), img_path))
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
    parser.add_argument('-f', '--img_file', required=True)      # option that takes a value
    args = parser.parse_args()
    result = []
    output(args["img_file"])
    
