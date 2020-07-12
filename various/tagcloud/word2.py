#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 15:15:34 2020

@author: drazioti@gmail.com
GPL v.2



"""

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt


x, y = np.ogrid[:300, :300]
mask = (x - 150) ** 2 + (y - 150) ** 2 >130 ** 2
mask = 255 * mask.astype(int)
curdir = os.path.dirname(__file__)

def create_wordcloud(text):
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white",max_words=200,
                   stopwords=stopwords, mask=mask, repeat =True)
    wc.generate(text)
    wc.to_file(os.path.join(curdir,"wc2.png"))
    
text = "blockchain, blockchain,distributedledger,\
        Decentralized, Decentralized,\
        bitcoin,bitcoin,\
        opensource,opensource,\
        MerkleTree,MerkleTree,\
        snakeoil,cryptography,ByzantineFaultTolerance,\
        smartcontracts"
create_wordcloud(text)

#wc = WordCloud(background_color="white", repeat=True, mask=mask)
#wc.generate(text)

#plt.axis("off")
#plt.imshow(wc, interpolation="bilinear")
#plt.show()
