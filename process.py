#!/usr/bin/env python
# coding: utf-8

# # Classify answers from le grand debat

# In[1]:


import sys
print(sys.version)
#Dict are ordered only after 3.6


# In[2]:


#https://granddebat.fr/pages/donnees-ouvertes
source_file = 'LA_TRANSITION_ECOLOGIQUE.csv'
q_id = 0
prefix = 'ECO_{:02d}'.format(q_id)
print (prefix)


# In[3]:


import hashlib

def md5(s):
    h = hashlib.new('md5')
    h.update(s.encode('utf-8'))
    return h.hexdigest()

print(md5("this is a test"))

def get_filename(string):
    h = md5(string)
    return 'html/{}/{}.txt'.format(prefix,h)


# In[4]:


import os.path
from bert_serving.client import BertClient
bc = BertClient()

cache_dict = {}
def encode(sentence):
    if sentence in cache_dict:
        return cache_dict[sentence]
    else:
        result = bc.encode([sentence])[0]
        cache_dict[sentence] = result
        return result


# In[5]:


import csv
header = []
answers = []

with open(source_file, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            header = row
        else:
            answers.append(row[11:])
        line_count += 1
        #if line_count >2:
        #    break
    print('Processed {} lines.'.format(line_count)) 


# In[6]:


import json
import numpy as np

questions = []
questions_vector = []
for q in header[11:]:
    q = q[20:]
    questions.append(q)
    result_q = encode(q)
    questions_vector.append(result_q)
    print('Q.:', q)  

with open('html/{}/questions.js'.format(prefix),'w') as file:
    data = json.dump(questions, file)

questions_array = np.stack(questions_vector, axis=0)
np.save('./data/{}/question_array.npy'.format(prefix), questions_array)


# In[7]:


import numpy as np
answers_list = []
answers_dict = {}

for i,reply in enumerate(answers[:]):
    #for q_id, a in enumerate(reply):
    a =  reply[q_id]
    if a and len(a)>0:
        a_clean = a.replace(' ','')
    else:
        a_clean = ''
    if a_clean and len(a_clean)>0:
        h = md5(a)
        if md5 in answers_dict:  
            v = answers_dict[h]
            answers_list.append((h,q_id,a,v))
        else:
            v = encode(a)
            answers_dict[h] = v
            answers_list.append((h,q_id,a,v))
    if i%100 == 0:
        print(i, 'cache', len(cache_dict))        


# In[8]:


import numpy as np
a_vector = []
a_list = []
q_id_list = []
h_list = []

for i, answer in enumerate(answers_list):
    h, q_id, a, v = answer
    
    with open('html/{}/{}.txt'.format(prefix, h),'w') as file:
        file.write(a) 
    a_list.append(a)
    q_id_list.append(q_id)
    a_vector.append(v)
    h_list.append(h)


# In[9]:


import numpy as np
v_array = np.stack(a_vector, axis=0)
print("number of sentences", v_array.shape[0])


# In[10]:


import json
np.save('./data/v_array.npy', v_array)

with open('./data/{}/a_list.npy'.format(prefix),'w') as file:
    json.dump(a_list, file)
with open('./data/{}/h_list.npy'.format(prefix),'w') as file:    
    json.dump(h_list, file)
with open('./data/{}/q_id_list.npy'.format(prefix),'w') as file:    
    json.dump(q_id_list, file)


# # LOAD data

# In[11]:


from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

transformer = Normalizer(copy=True, norm='l2')
normalized = transformer.transform(v_array)
#X = PCA(n_components=50).fit_transform(normalized)
#X = StandardScaler().fit_transform(reduced_data)


# In[12]:


import time
import umap

time_start = time.time()
umap_ = umap.UMAP(
        verbose=True)
embedding = umap_.fit_transform(normalized)
print('umap done! Time elapsed: {} seconds'.format(time.time()-time_start))


# In[13]:


np.save('./data/{}/lgd_umap.npy'.format(prefix), embedding)


# In[14]:


#get_ipython().run_line_magic('matplotlib', 'inline')
#
#import matplotlib
#import matplotlib.pyplot as plt
#
#plt.figure(figsize=(15,10))
#plt.scatter(embedding[:,0],embedding[:,1],)
#

# In[16]:


new_list = []
for i, md5 in enumerate(h_list):
    new_dot = {}
    new_dot['h']=md5
    new_dot['c']=len(a_list[i])
    new_dot['q']=q_id_list[i]
    new_dot['x']=float(embedding[i,0])
    new_dot['y']=float(embedding[i,1])
    new_list.append(new_dot)
    if i%10000 == 0:
        print(i, md5)
    
with open('./html/{}/lgd_ecologie_07.json'.format(prefix),'w') as file:
    json.dump(new_list, file)


# In[18]:


with open('./html/lgd_ecologie_07.csv','w') as file:
    file.write('md5,c,q_id,x,y\n')
    for i, md5 in enumerate(h_list):
        line = md5 + ','
        line += str(len(a_list[i])) + ','
        line += str(q_id_list[i])  + ','
        line += str(embedding[i,0]) + ','
        line += str(embedding[i,1]) + '\n'
        file.write(line)
        if i%10000 == 0:
            print(i, line)


# In[ ]:




