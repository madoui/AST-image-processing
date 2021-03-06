# Copyright 2019 Fondation Medecins Sans Frontières https://fondation.msf.fr/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file is part of the ASTapp image processing library
# Author: Marco Pascucci

from contextlib import contextmanager
import astimp
import sys
import glob
import os
import time
from imageio import imread, imwrite
import matplotlib.pyplot as plt
import numpy as np
from importlib import reload
log = sys.stdout.write

##################
# import astimp

@contextmanager
def logged_action(before, after='done'):
    try:
        log(before + '...')
        yield
    finally:
        log(after+'\n')


img_path = "tests/images/test0.jpg"

# Test Exception
# astimp.throw_custom_exception("test")

with logged_action("read image"):
    im_np = np.array(imread(img_path))

with logged_action("crop Petri dish"):
    crop = astimp.cropPetriDish(im_np)

with logged_action("find pellets"):
    circles = astimp.find_atb_pellets(crop)
    pellets = [astimp.cutOnePelletInImage(crop, circle) for circle in circles]

with logged_action("standardize pellet"):
    astimp.standardizePelletImage(pellets[0][:, :, 0])

with logged_action("read labels"):
    labels = [astimp.getOnePelletText(pellet) for pellet in pellets]

with logged_action("preprocessing"):
    preproc = astimp.inhib_diam_preprocessing(crop, circles)

with logged_action("measure diameters"):
    disks = astimp.measureDiameters(preproc)

# print()
# for disk in disks:
#     print(disk.diameter, disk.confidence)
