
# coding: utf-8

# In[87]:


import pandas as pd
import pymmh3 as mmh3
import numpy as np
import random

seed=1

def Mapping1(clientvalue,cohort,num_hashes,bfsize, allunique):
    inptomd=str(cohort)+clientvalue
    listofindx=[]
    
    i=0
    entries=0
    while(entries<num_hashes):
        digest = mmh3.hash(inptomd,i) % bfsize
        if(digest not in listofindx):
            listofindx.append(digest)
            entries=entries+1
        
        i=i+1
   
    return listofindx

# In[143]:


def FakeBloomFilter(bloom,f,bfsize):
    fakebloomfilter=np.zeros(bfsize)
    for i in range(0,bfsize):
        chc=np.random.choice(np.array([1,2,3]), p=[f/2,f/2,1-f])
        if(chc==1):
           fakebloomfilter[i]=0
        elif(chc==2):
            fakebloomfilter[i]=1
        else:
            fakebloomfilter[i]=bloom[i]
   
    return fakebloomfilter


# In[144]:

def ProcessEachString(word,cohort,f,bfsize,no_hashes, allunique):
    bloom_filter=np.zeros((len(word),bfsize))
    getindex=[Mapping1(word[i],cohort[i],no_hashes,bfsize, allunique) for i in range(0,len(word))]

    reports = []
    for i in range(len(word)):
        #print(getindex[i])
        for j in range(0,len(getindex[i])):
            bloom_filter[i][getindex[i][j]]=1
        report=FakeBloomFilter(bloom_filter[i],f,bfsize)
        reports.append(report.astype(int).tolist())

    return reports

def GetBloomBits(candidatestring,cohort,bfsize,no_hashes, allunique):
    bloom_filter_string_cohort=np.zeros(bfsize)
    getindex=Mapping1(candidatestring,cohort,no_hashes,bfsize, allunique)

    for i in range(0,len(getindex)):
        bloom_filter_string_cohort[getindex[i]]=1
    return bloom_filter_string_cohort

# In[145]:
def mapBloomFilter(clientvalue, icohort, nhashes, bfsize):

    inptomd=str(icohort)+clientvalue
    
    listofindx=[]

    i=0
    entries=0
    while(entries<nhashes):
        digest = mmh3.hash(inptomd,i) % bfsize
        if(digest not in listofindx):
            listofindx.append(digest)
            entries=entries+1
        
        i=i+1
        
    vec = np.zeros(bfsize)
    for ind in listofindx:
        vec[ind] = 1

    return vec

def mapCohortsBloomFilter(clientvalue,cohort,num_hashes,bfsize):
    for k in range(0,len(cohort)):
        inptomd=clientvalue+str(cohort[k])
        encoded=hashlib.md5(inptomd.encode('utf-8')).hexdigest()
        inds = [ord(encoded[i]) % bfsize for i in range(num_hashes)]
        print(inds)

def ProcessDataAndParameters(saminp,no_cohorts,f,bfsize,no_hash, allunique):

    matrix = []
    np.random.seed(seed)
    allcohorts=[]
    print(no_cohorts)
    for i in range(0,len(saminp)):
        stringval=saminp['word'].iloc[i]
       
        curlist=[stringval]*int(saminp['trueFrequency'].iloc[i])
        cohorts=np.array([np.random.randint(1,no_cohorts+1) for i in range(0,len(curlist))])
        allcohorts.extend(cohorts)
        reports = ProcessEachString(curlist,cohorts,f,bfsize,no_hash, allunique)
        matrix.extend(reports)

    return [matrix,np.array(allcohorts)]


# In[146]:
# infile = pd.read_csv('smallcorpus.csv')
# client = infile.sample(frac=0.1)
# print(client)
# print(ProcessDataAndParameters(saminp,4,0.3,32,2))
