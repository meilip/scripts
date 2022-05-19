#!/usr/bin/env python
# coding: utf-8

# In[21]:


import numpy as np
import requests
import urllib.request
from bs4 import BeautifulSoup
import os, glob

def mylistdir(directory):
    
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]

os.chdir("/home/grandma/Data")

basedir = 'TCA'

filelist = mylistdir(basedir)
print(filelist)

with open("listeGRB.txt", "w") as file:
    for i,img in enumerate(mylistdir(basedir)):
        file.write(img+ "\n")
        
URL = "http://tca4.tarotnet.org/ros/alert_fermi/"

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

# FIND GRBs (names)
text = soup.find('pre').text
    
text = text.replace(text[:94],"")
text = text.split('\n')
text.pop()

tab = np.empty((0,6))

for i in range(len(text)):
    tab = np.append(tab, np.array([text[i].split()]), axis=0)
    
grbs = []

for i in range(len(tab)):
    if "GRB" in tab[i][5]:
        grbs.append(tab[i][0])

# LISTE DES URL format complet
allurl = soup.find_all('a')

# LISTE DES URL 
urls = []

for i in range(len(grbs)):
    for k in range (len(allurl)): 
        if grbs[i] in allurl[k]:
            urls.append(allurl[k].get('href'))   
            
for i in range(len(urls)):
    os.chdir("/home/grandma/Data")
    if urls[i] not in mylistdir(basedir):
    
        # Define url 
        remote_url = urls[i]
        local_file = grbs[i]
    
        # Download the file into chosen directory
        os.chdir("/home/grandma/Data/TCA")
        urllib.request.urlretrieve(remote_url, local_file)

