import glob
import os
import pandas as pd
from collections import Counter
from string import digits
import re
import numpy
import en_core_web_lg
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from operator import itemgetter 
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

folders = ["onion-swift2"]


mass_text = []
n_steps = []
counter=  0


for folder in folders:
    path  = os.getcwd() + './Results/' + folder
    files = glob.glob(path + '/*.txt')
    # iterate over the list getting each file 
    for fle in files:
       # open the file and then call .read() to get the text 
      if 'db' in fle and counter <= 250:
          with open(fle, encoding="utf8") as f:
              text = f.read()
              mass_text.append(text.replace('\n',''))
              n_steps.append(text.count('.'))
      counter = counter + 1

corpus = "".join(mass_text)
# Let's get the vector coordinates for each step.
# Load the spacy NLP statistical models
nlp = en_core_web_lg.load()
doc = nlp(corpus)
#chunks = list(doc.noun_chunks)
sents = list(doc.sents)

# Initialize a vector storage space 
X_sents = np.zeros((len(sents), 300))

# Get the embeddings for each step
index = 0
for sent in sents:
    X_sents[index,:] = sent.vector
    index= index+1
    
# Do k-means clustering
kmeans = KMeans(n_clusters = 10, random_state = 1).fit(X_sents)
clusters = kmeans.labels_
centers = kmeans.cluster_centers_

#in_cluster = np.where(clusters == 1)[0]
#in_cluster.astype(int)


#steps_in_cluster = itemgetter(*in_cluster)(mass_text)

# For each cluster center, get the closest element
step_nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(X_sents)

# Return the index and distance of the closest neighbor
for center in centers:
    new_vec = center.reshape(1,-1)
    distances, indices = step_nbrs.kneighbors(new_vec)
    print(sents[indices[0][0]])
    print(sents[indices[0][1]])
    print(sents[indices[0][2]])
    print(sents[indices[0][3]])
    print(sents[indices[0][4]])
    print('-----------------Next---------------------')
    
# Do a PCA analysis to reduce dimensionality for plotting
pca = PCA(n_components=3)
pca.fit(X_sents)
sents2 = pca.transform(X_sents)
fig = plt.figure(1, figsize=(4, 3))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
ax.scatter(sents2[:,0],sents2[:,1],sents2[:,2], alpha=0.5, c=clusters, cmap=plt.cm.spectral,
           edgecolor='k')# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 15:28:05 2017

@author: andro
"""

