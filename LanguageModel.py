import json
# if you are using python 3, you should
import urllib.request
#import urllib2
from nltk.corpus import stopwords
from langdetect import detect


def post(encoded_args,lang):
    en_inurl = 'http://ec2-13-58-86-116.us-east-2.compute.amazonaws.com:8983/solr/LanguageModel/select?q='+encoded_args+'&defType=edismax&qf=text_en^2+text_de+text_ru&fl=id%2Cscore&wt=json&indent=true&rows=20'
    de_inurl = 'http://ec2-13-58-86-116.us-east-2.compute.amazonaws.com:8983/solr/LanguageModel/select?q='+encoded_args+'&defType=edismax&qf=text_en+text_de^2+text_ru&fl=id%2Cscore&wt=json&indent=true&rows=20'
    ru_inurl = 'http://ec2-13-58-86-116.us-east-2.compute.amazonaws.com:8983/solr/LanguageModel/select?q='+encoded_args+'&defType=edismax&qf=text_en+text_de+text_ru^2&fl=id%2Cscore&wt=json&indent=true&rows=20'
    inurl = 'http://ec2-13-58-86-116.us-east-2.compute.amazonaws.com:8983/solr/LanguageModel/select?q='+encoded_args+'&defType=edismax&qf=text_en+text_de+text_ru&fl=id%2Cscore&wt=json&indent=true&rows=20'
    outfn =str(iter)+'.txt'


    # change query id and IRModel name accordingly
    IRModel='LM'
    outf = open(outfn, 'a+',encoding="utf8")
    print(inurl)
    if lang=='en':
        data = urllib.request.urlopen(en_inurl)
    elif lang=='de':
        data = urllib.request.urlopen(de_inurl)
    elif lang=='ru':
        data = urllib.request.urlopen(ru_inurl)
    else:
        data = urllib.request.urlopen(inurl)
    # if you're using python 3, you should use
    # data = urllib.request.urlopen(inurl)

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
    queryid =  words[0]
    for word in words[1:]:
        query= query+word+' '
    queryprocessing (query)
    


f = open(r'/Users/prudhveer/Desktop/Information_Retrieval /project3_data/test_queries.txt','r',encoding="utf8")


for l in f.readlines():
    preprocess(l)



