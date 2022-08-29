# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 18:50:20 2022

@author: Swarna S
"""
import math
import glob
import nltk
#nltk.download('popular');
from nltk.corpus import stopwords
from nltk import word_tokenize
import string
#import numpy as np
from collections import OrderedDict

def give_path(fld_path):                             #give path of the folder containing all documents
    dic = {}
    file_names = glob.glob(fld_path)
    
    for file in file_names:
        name = file.split('/')[-1]
        with open(file, 'r', errors='ignore') as f:
            data = f.read()
        dic[name] = data
    return dic

def wordList_removePuncs(doc_dict):
    stop = stopwords.words('english') + list(string.punctuation) + ['\n']
    wordList = []
    for doc in doc_dict.values():
        for word in word_tokenize(doc.lower().strip()): 
            if not word in stop:
                wordList.append(word)
    return wordList


def wordDocFre(vocab, doc_dict):
    
    word_doc_freq_dict = {}
    for doc_name, doc_value in doc_dict.items():
        tf = {}
        word_doc_list = word_tokenize(doc_value.lower().strip())
        
        max_freq = 0
        for word in vocab:
            freq = 0
            if word in word_doc_list:
                freq = word_doc_list.count(word)
            if freq > max_freq:
                max_freq = freq
            tf[word] = freq
            
        for word in vocab:
            tf[word] = tf[word] / max_freq
            
        word_doc_freq_dict[doc_name] = tf
    return word_doc_freq_dict


def inverseDocFre(vocab, doc_dict, M):
    inverse_doc_freq_dict = {}
    
    docs_count_dict = {}
    for word in vocab:
        docs_count_dict[word] = 0
        
    for doc_value in doc_dict.values():
        words = word_tokenize(doc_value.lower().strip())
        for word in vocab:
            if word in words:
                docs_count_dict[word] += 1
                
    for word in vocab:     
        inverse_doc_freq_dict[word] = math.log(M / docs_count_dict[word])
        
    return inverse_doc_freq_dict

def tfidf(vocab, tf_dict, idf_dict, doc_dict):
    tf_idf_dict = {}
    for doc_name in tf_dict.keys():
        tf_idf_score = {}
        for word in vocab:
            tf_idf_score[word] = 0
            if word in idf_dict.keys():
                tf_idf_score[word] = tf_dict[doc_name][word] * idf_dict[word]
        tf_idf_dict[doc_name] = tf_idf_score
    return tf_idf_dict

def cosineSimilarity(doc_vocab, doc_tf_idf, query_vocab, query_tf_idf):
    common_terms = list(set(doc_vocab).intersection(set(query_vocab)))
    numerator = 0
    term1 = 0
    term2 = 0
    for word in common_terms:
        numerator += (doc_tf_idf[word] * query_tf_idf[word])
        term1 += (doc_tf_idf[word] ** 2)
        term2 += (query_tf_idf[word] ** 2)
    denominator = math.sqrt(term1 * term2)
    score = numerator / denominator
    return score
    
if __name__  == "__main__":
   path = 'data/*'
   docs = give_path(path)                        #returns a dictionary of all docs
   
   M = len(docs)                                 #number of files in dataset
   doc_word_List = wordList_removePuncs(docs)           #returns a list of tokenized words
   doc_vocab = list(set(doc_word_List))                     #returns a list of unique words
   
   doc_tf_dict = wordDocFre(doc_vocab, docs)             #returns document frequencies
   
   idf_dict = inverseDocFre(doc_vocab, docs, M)     #returns idf scores
   
   doc_tf_idf = tfidf(doc_vocab, doc_tf_dict, idf_dict, docs)   #returns tf-idf socres
   
   path = 'test/*'
   query_doc = give_path(path)
   query_word_list = wordList_removePuncs(query_doc)
   query_vocab = list(set(query_word_list))
   query_tf_dict = wordDocFre(query_vocab, query_doc)
   query_tf_idf = tfidf(query_vocab, query_tf_dict, idf_dict, query_doc)
   
   for doc_name in doc_tf_idf.keys():
       cosine_sim_score = cosineSimilarity(doc_vocab, doc_tf_idf[doc_name], 
                                           query_vocab, query_tf_idf['test\one_fish_two_fish.txt'])
       print(doc_name, cosine_sim_score)