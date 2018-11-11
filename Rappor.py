
# coding: utf-8

# In[87]:


import pandas as pd
import hashlib
import numpy as np
import random


# In[138]:


def Mapping1(clientvalue,cohort,num_hashes,bfsize):
    inptomd=clientvalue+str(cohort)
    encoded=hashlib.md5(inptomd.encode('utf-8')).hexdigest()
    return [ord(encoded[i]) % bfsize for i in range(num_hashes)]


# In[143]:


def FakeBloomFilter(bloom,f,bfsize):
    fakebloomfilter=np.zeros(bfsize)
    for i in range(0,bfsize):
        fakebloomfilter[i]=np.random.choice(np.array([0,1,bloom[i]]), p=[f/2,f/2,1-f])
    return fakebloomfilter


# In[144]:


def ProcessEachString(word,cohort,f,bfsize,no_hashes):
    bloom_filter=np.zeros((len(word),bfsize))
    getindex=[Mapping1(word[i],cohort[i],no_hashes,bfsize) for i in range(0,len(word))]
    for i in range(len(word)):
        #print(getindex[i])
        for j in range(0,len(getindex[i])):
            bloom_filter[i][getindex[i][j]]=1
        #print(bloom_filter[i])
        report=FakeBloomFilter(bloom_filter[i],f,bfsize)
        print(report)


# In[145]:


def ProcessDataAndParameters(saminp,no_cohorts,f,bfsize,no_hash):
    
    for i in range(0,1):
        stringval=saminp['word'].iloc[i]
        curlist=[stringval]*int(saminp['trueFrequency'].iloc[i])
        cohorts=[random.randint(1,no_cohorts+1) for i in range(0,len(curlist))]
        ProcessEachString(curlist,cohorts,f,bfsize,no_hash)
      


# In[146]:


inpfile=pd.read_csv('C:\\Users\\barna\\Documents\\data mining\\corpus.csv')
saminp=inpfile.sample(frac=0.1)
ProcessDataAndParameters(saminp,4,0.3,32,2)

