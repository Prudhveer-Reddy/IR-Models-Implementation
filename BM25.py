# -- coding: utf-8 --


import json
from nltk.corpus import stopwords
import urllib.request
from langdetect import detect


def post(encoded_args,lang):
    inurl = 'http://ec2-13-58-86-116.us-east-2.compute.amazonaws.com:8983/solr/BM25/select?q='+encoded_args+'&defType=edismax&qf=text_en+text_de+text_ru&fl=id%2Cscore&wt=json&indent=true&rows=20'
    outfn = str(iter)+'.txt'


    # change query id and IRModel name accordingly
    IRModel='BM25'
    outf = open(outfn, 'a+',encoding="utf8")
    print(inurl)
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']
    print(docs)
    # the ranking should start from 1 and increase
    rank = 0
    for doc in docs:
        outf.write(queryid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
        rank += 1
    outf.close()


iter=0


def queryprocessing (query):
    query=query[:-1]
    language = detect(query)
    query_args= {'q':query}
    en_args = urllib.parse.quote_plus(query)
    post(en_args,language)

def preprocess (l):
    global iter
    iter=iter+1
    query=''
    words=l.split(" ")
    global queryid
    queryid = words[0]
    for word in words[1:]:
        query= query+word+' '
    queryprocessing (query)
    


f = open(r'/Users/prudhveer/Desktop/Information_Retrieval /project3_data/test_queries.txt','r',encoding="utf8")


for l in f.readlines():
    preprocess(l)

