# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 2022

This code contains classes and essential backend code which will be used to generate entries in Solvent and Polymer collections for ofetdb

@author: Aaron Liu, Ron Volkovinsky, Rahul Venkatesh
"""

import numpy as np
import pylab as plt
import pandas as pd 
import csv 
import matplotlib.pyplot as plt
import os
from os.path import join


class Solvent:

    def __init__(self, cid):
        
        """
        A new solvent entry is uniquely identified by its PubChem CID
        """
        self.cid = cid