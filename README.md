# ZenModelMaintenance
An open-source stack of python, elasticseach &amp; grafana using a decision tree based on iris data to show how you can detect events that affect performance sooner rather than later.

# Environment
Install python, elasticsearch and grafana - see below for the versions I'm running. Note: make sure the elasicsearch & grafana services are running

$ python --version
Python 3.6.3 :: Anaconda custom (64-bit)

$ elasticsearch --version
Version: 6.2.4, Build: ccec39f/2018-04-12T20:37:28.497551Z, JVM: 1.8.0_91

$ grafana-server -v
Version 5.2.2 (commit: unknown-dev)

# Create the indexes
Assuming your elasticsearch server is running on port 9200, create the index & mappings...

$ ./create
{"acknowledged":true}
{"acknowledged":true,"shards_acknowledged":true,"index":"a1"}
...
{"acknowledged":true}

# Build the model (optional)
$ python model.py 
Note, this creates saved model (iris_cart.sav) and centroids (iris_kmeans.sav) which are already in the repository

# Post data to the indexes
$ python post.py
1 batch= PFROVNXM created at 2018-09-15 11:52:06
2 batch= 5YHP8LZ4 created at 2018-09-15 11:52:07
3 batch= 0QBDSTIC created at 2018-09-15 11:52:08
4 batch= CYH3JSPP created at 2018-09-15 11:52:09
5 batch= NI0719X0 created at 2018-09-15 11:52:10
...

# Import the json into grafana to see the dashboard
In Grafana, Choose Create -> Import -> and upload the file ZEN-1537036892661.json
