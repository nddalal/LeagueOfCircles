# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:04:12 2019

@author: nihar
"""

from pathing import *

class AllyMinion(object):
    def __init__(self,app):
        self.app = app
        self.pos = (1,0)
        endPos = (9,18)
        self.path = aStar(self.app, self.pos, endPos) 

class EnemyMinion(object):
    def __init__(self,app):
        self.app = app
        self.pos = (8,19)
        endPos = (0,1)
        self.path = aStar(self.app, self.pos, endPos) 