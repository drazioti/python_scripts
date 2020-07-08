#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 15:15:34 2020

@author: drazioti@gmail.com
GPL v.2
"""

from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import os

curdir = os.path.dirname(__file__)

def create_wordcloud(text):
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white",max_words=200,
                   stopwords=stopwords)
    wc.generate(text)
    wc.to_file(os.path.join(curdir,"wc.png"))
    
text = "blockchain, software, software, hardware,hardware,\
        security,\
        edgecomputing, \
        bitcoin,                \
        mooc, mooc, mooc\
        optimization\
        python\
        e-Learning\
        HCI,HCI,HCI\
        Ledger\
        cyberphysical,cyberphysical\
        analytics\
        seriousgames,seriousgames\
        IOT,IOT\
        Interactive,Interactive\
        opensource,opensource"
create_wordcloud(text)
