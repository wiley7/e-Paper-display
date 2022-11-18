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
import string
logging.basicConfig(level=logging.INFO)

threshold=[63, 126, 189]

def stringLength(str):
    # count a hanzi as two letters
    count_yw = count_num = count_zw = count_fh = 0
    for s in str:
        if s in string.ascii_letters:
            count_yw += 1
        elif s.isdigit():
            count_num += 1
        elif s.isalpha():
            count_zw += 1
        else:
            count_fh += 1
    logging.debug("%s : yw:%d, num:%d, zw:%d, oth:%d", str, count_yw, count_num, count_zw, count_fh)
    return math.ceil((count_yw + count_num + count_fh + count_zw *2)/2)

def output(txt_path):
    try:
        logging.info("epd3in7")
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
        w_padding = 5
        h_padding = 5

        # calc font height
        line_height = math.floor((epd.width - (h_padding *2))/line_cnt)
        if line_height > 10:
            font_size = math.floor(line_height / 1.05)
            line_indent = line_height - font_size

        # calc font width
        max_line_size = 0
        for line in lines:
            line_l = stringLength(line)
            if max_line_size < line_l:
                max_line_size = line_l
        
        font_width = math.floor((epd.height - (w_padding *2))/max_line_size)
        logging.debug("font_width:%d = math.floor((%d - (%d *2))/%d)", font_width, epd.height, w_padding, max_line_size)

        logging.debug("font height %d, width %d", font_size, font_width)
        if font_size > font_width:
            font_size = font_width

        if font_size < 16:
            font_size = 16
            line_indent = 1
        logging.info("line height %d, font size %d, line indet %d", line_height, font_size, line_indent)
        font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), font_size)

        index = 0
        for line in lines:
            # line = line.strip()
            line_start_x = w_padding
            line_start_y = h_padding + index * (font_size + line_indent)
            draw.text(xy=(line_start_x, line_start_y), text=line,font=font,align='left',fill=epd.GRAY4)
            index = index+1
        # 翻转一下，树莓派电源位置比较尴尬，干脆倒过来看
        epd.display_4Gray(epd.getbuffer_4Gray(Himage.rotate(180)))
        
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
    
