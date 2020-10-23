#!/usr/bin/env python3
 # -*- coding: utf-8 -*-

# ---------------------------- #
# Generic Imports
# ---------------------------- #
from __future__ import print_function
from __future__ import division

# Standard Library, plus some Third Party Libraries

import logging
from pprint import pprint
from PIL import Image
from tqdm import tqdm
from typing import Union, Tuple

import configargparse
from functools import partial

import collections
import copy
import datetime
import functools
import h5py
import math
import operator
import os
import random
import shutil
import sys
import re
import time
# import visdom

# Data Science and Machine Learning Libraries
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

import numpy as np
import pandas as pd
import sklearn

# ---------------------------- #
# Custom Imports
# ---------------------------- #
from utils.custom_argparser import get_cmd_line_opts
from utils.functions import check_dir_exists, create_dir