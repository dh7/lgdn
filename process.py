#!/usr/bin/env python
# coding: utf-8

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, help="the file to analyse")
parser.add_argument("--prefix", type=str, help="the prefix to save the data")
parser.add_argument("--q_id", type=int, help="the question id")
parser.add_argument("--limit", type=int, help="process only first contributions")
args = parser.parse_args()

source_file = args.filename
q_id = args.q_id
prefix = '{}_{:02d}'.format(args.prefix, q_id)
print (prefix)

import os
try:
    os.mkdir('./data')
except OSError:
    print ("Creation of the directory failed")
else:
    print ("Successfully created the directory")

try:
    os.mkdir('./data/'+prefix)
except OSError:
    print ("Creation of the directory failed")
else:
    print ("Successfully created the directory")

try:
    os.mkdir(prefix)
except OSError:
    print ("Creation of the directory failed")
else:
    print ("Successfully created the directory")

    
import hashlib

def md5(s):
    h = hashlib.new('md5')
    h.update(s.encode('utf-8'))
    return h.hexdigest()

print(md5("this is a test"))

def get_filename(string):
    h = md5(string)
    return '{}/{}.txt'.format(prefix,h)

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

# open the CSV file
import sys
import csv
csv.field_size_limit(sys.maxsize) 
header = []
answers = []

with open(source_file, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            header = row
        else:
            if row[6]=='false':
                answers.append(row[11:])
        line_count += 1
    print('Processed {} lines.'.format(line_count)) 

import json
import numpy as np

questions = []
questions_vector = []
for q in header[11:]:  # Remove utilitarian field
    q = q[20:]  # Remove 20 first char that are used for ID
    questions.append(q)
    result_q = encode(q)
    questions_vector.append(result_q)
    print('Q.:', q)  

with open('{}/questions.json'.format(prefix),'w') as file:
    data = json.dump(questions, file)

questions_array = np.stack(questions_vector, axis=0)
np.save('./data/{}/question_array.npy'.format(prefix), questions_array)

# Parse the file
import numpy as np
answers_list = []
answers_dict = {}

if args.limit == -1:
    answers_limited = answers[:]
else:
    answers_limited = answers[:args.limit]

for i, reply in enumerate(answers_limited):
    # for q_id, a in enumerate(reply):
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
            try:
                v = encode(a)
                answers_dict[h] = v
                answers_list.append((h,q_id,a,v))
            except:
                print ('error with line',i,a)
    if i%100 == 0:
        print(i, 'cache', len(cache_dict))        

# Write the results
import numpy as np
a_vector = []
a_list = []
q_id_list = []
h_list = []

for i, answer in enumerate(answers_list):
    h, q_id, a, v = answer
    
    with open('{}/{}.txt'.format(prefix, h),'w') as file:
        file.write(a) 
    a_list.append(a)
    q_id_list.append(q_id)
    a_vector.append(v)
    h_list.append(h)

import numpy as np
v_array = np.stack(a_vector, axis=0)
print("number of sentences", v_array.shape[0])

import json
np.save('./data/v_array.npy', v_array)

with open('./data/{}/a_list.npy'.format(prefix),'w') as file:
    json.dump(a_list, file)
with open('./data/{}/h_list.npy'.format(prefix),'w') as file:    
    json.dump(h_list, file)
with open('./data/{}/q_id_list.npy'.format(prefix),'w') as file:    
    json.dump(q_id_list, file)

# Create the map

from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

transformer = Normalizer(copy=True, norm='l2')
normalized = transformer.transform(v_array)
#X = PCA(n_components=50).fit_transform(normalized)
#X = StandardScaler().fit_transform(reduced_data)

import time
import umap

time_start = time.time()
umap_ = umap.UMAP(
        n_neighbors=100,
        verbose=True)
embedding = umap_.fit_transform(normalized)
print('umap done! Time elapsed: {} seconds'.format(time.time()-time_start))

np.save('./data/{}/lgd_umap.npy'.format(prefix), embedding)


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
    
with open('./{}/data.json'.format(prefix),'w') as file:
    json.dump(new_list, file)


with open('./data/{}/data.csv'.format(prefix),'w') as file:
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
