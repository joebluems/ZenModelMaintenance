import sys
import random
import string
import datetime
import time
import pandas
import pickle
from sklearn.metrics import f1_score

### connect to Elasticsearch ###
from elasticsearch import Elasticsearch
es = Elasticsearch( hosts=[{'host': 'localhost', 'port': 9200}])

### read iris data ###
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
iris = pandas.read_csv("iris.csv", names=names)

### load CART model & K-Means centroids ###
loaded_model = None
clusters = None
with open('./iris_cart.sav','rb') as f: loaded_model = pickle.load(f)
with open('./iris_kmeans.sav','rb') as g: clusters = pickle.load(g)


###################################################
#### scoring batches & writing results to index ###
###################################################
for i in range(1,10000):

  ### sample iris data and apply model & clustering ###
  df = iris.sample(frac=0.33,replace=False)
  batch = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
  array = df.values
  X = array[:,0:4]
  Y = array[:,4]
  r = random.random()

  ### if we are perturbing the data.... ###
  if r<0.008: 
    option = random.choice([0,1,2,3])
    option2 = random.choice([1,-1])
    X[:,option]=X[:,option]+option2
    doc = { 'ts': t0, 'batch': batch, 'result': option, }
    res = es.index(index="a2", doc_type='alert', id=i, body=doc)
    print(i,"perturb event for batch=",batch,"at",t0)

  predictions = loaded_model.predict(X)
  distance = clusters.transform(X)
  sse=0
  for row in distance:
    sse+=min(row)**2

  t0 = time.strftime("%Y-%m-%d %H:%M:%S")

  ### load F1 into index ###
  doc = { 'ts': t0, 'batch': batch, 'result': f1_score(Y, predictions,average='macro'), }
  res = es.index(index="a1", doc_type='AUC', id=i, body=doc)


  ### load MSE into index ###
  doc = { 'ts': t0, 'batch': batch, 'result': sse/len(distance), }
  res = es.index(index="b1", doc_type='mse', id=i, body=doc)

  ### load raw data into index ###
  doc1 = { 'ts': t0, 'batch': batch, 'result': df['sepal-length'].mean(), }
  doc2 = { 'ts': t0, 'batch': batch, 'result': df['sepal-width'].mean(), }
  doc3 = { 'ts': t0, 'batch': batch, 'result': df['petal-length'].mean(), }
  doc4 = { 'ts': t0, 'batch': batch, 'result': df['petal-width'].mean(), }
  res = es.index(index="c1", doc_type='raw', id=i, body=doc1)
  res = es.index(index="c2", doc_type='raw', id=i, body=doc2)
  res = es.index(index="c3", doc_type='raw', id=i, body=doc3)
  res = es.index(index="c4", doc_type='raw', id=i, body=doc4)

  print(i,"batch=",batch,res['result'],"at",t0)
  time.sleep(1) 
