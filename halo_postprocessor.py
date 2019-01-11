#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Copyright (C) 2018 Ethereal Machines Pvt. Ltd. All rights reserved.
# Distributed under terms of the MIT license. 

__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__version__ = '1.18.06.11'

"""
Halo Postprocessor.
"""

# TODO: add publisher info in exe
# TODO: beautify window

import os
import sys
from tkinter.filedialog import askopenfilename
import re
import logging


logger = logging.getLogger(__name__)

file_path = askopenfilename(initialdir="./", title="Select file", filetypes=(("gcode files", "*.gcode"),("all files", "*.*")))
# file_path = "CFFFP_bridging_test.gcode"

if file_path is None or not file_path:
    logger.warning('File not selected.')
    sys.exit('Exiting..')
elif os.path.splitext(file_path)[1].lower() != '.gcode':
    logger.warning('Unsupported file.')
    sys.exit('Unsupported file. Exiting..')

count = 1

parent_dir, filename = os.path.split(file_path)
name, ext = os.path.splitext(filename)
similar_files = []

regex = re.escape(filename) + r'\-eth\-[0-9]+\.nc\Z'

regex = r'(?s:' + re.escape(name) + r'-eth\-[0-9]+\.nc)\Z'
re_obj = re.compile(regex)

for file in os.listdir(parent_dir, ):
    if re_obj.match(file):
        similar_files.append(file)

output = None

if len(similar_files) > 0:
    logger.info('Similar output files found.')
    max_file_count = max(map(lambda f: int((f.rsplit('-eth-', 1)[1]).rsplit('.',1)[0]), similar_files))
    count = max_file_count + 1
    output = os.path.join(parent_dir, name) + f'-eth-{count}.nc'
else:
    output = os.path.join(parent_dir, name) + f'-eth-{count}.nc'

with open(file_path, 'r') as r_stream, open(output, 'w') as w_stream:
    w_stream.write("%\n")
    # w_stream.write("M100 P170")

    for datum in r_stream:
        if ";" not in datum:
            datum = datum.replace('E', 'B').replace('M104 S', 'M100 P')
            if "M" in datum and all(i not in datum for i in ["M100", "M9", "M30"]):
                pass
            else:
                w_stream.write(datum)
            
    w_stream.write("M9\n")
    w_stream.write("M30\n")
    w_stream.write("%\n")

logger.info(f'File {output} has been processed successfully..')
