#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Copyright (C) 2018 Ethereal Machines Pvt. Ltd
# Distributed under terms of the MIT license. All rights reserved license.

__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__version__ = '1.18.05.04'

"""
Halo Postprocessor.
"""

import os
import sys
from tkinter.filedialog import askopenfilename
import re
import logging


logger = logging.getLogger(__name__)

file_path = askopenfilename()

if file_path is None or not file_path:
    logger.warning('File not selected.')
    sys.exit('Exiting..')

count = 1

parent_dir, filename = os.path.split(file_path)
name, ext = os.path.splitext(filename)

similar_files = []

regex = '(?s:square\-eth\-[0-9]+\.nc)\Z'
re_obj = re.compile(regex)

for file in os.listdir(parent_dir, ):
    if re_obj.match(file):
        similar_files.append(file)

output = None

if len(similar_files) > 0:
    logger.info('Similar output files found.')

    max_file_count = max(map(lambda f: int((f.rsplit('-eth-', 1)[1]).rsplit('.',1)[0]), similar_files))

    if not os.path.isfile(os.path.join(parent_dir, name) + f'-eth-{count}.nc'):
        output = os.path.join(parent_dir, name) + f'-eth-{count}.nc'
    else:
        count = max_file_count + 1
        output = os.path.join(parent_dir, name) + f'-eth-{count}.nc'

with open(file_path, 'r') as r_stream, open(output, 'w') as w_stream:
    w_stream.write("%\n")
    w_stream.write("M101 Q170")

    for datum in r_stream:
        if ';' not in datum and 'M' not in datum:
            w_stream.write(datum.replace('A', 'U'))

    w_stream.write("M9\n")
    w_stream.write("M30\n")
    w_stream.write("%\n")

logger.info(f'File {output} has been processed successfully..')
