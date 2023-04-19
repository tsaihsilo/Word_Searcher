# Author: Selena Lo
# Email: tsaihsilo@umass.edu
# Spire ID: 33702452

import urllib.request
import string
import sys
import re

def read_article_file(url):
    req = urllib.request.urlopen(url)
    text = req.read()
    text = text.decode('UTF-8')
    return text

def text_to_article_list(text):
    list_result = re.split('<NEW ARTICLE>', text)
    new_list = list(filter(lambda x: x != '', list_result))
    return new_list

def split_words(text):
    l1 = text.splitlines()
    lis=[]
    for i in l1:
        lis += i.split()
        continue
    return lis

def scrub_word(text):
    text1 = text.strip(string.punctuation)
    text2 = list(filter(lambda x: x != '', text1))
    x = ''
    return x.join(text2)

def scrub_words(words):
    lis = []
    for i in words:
        no_non_alpha = re.sub(r"[^a-zA-Z]", "", i)
        no_non_alpha = no_non_alpha.lower()
        lis.append(no_non_alpha)
    return lis

article_index = {}
def build_article_index(article_list):
    for (index, article) in enumerate(article_list):
        tmp1 = split_words(article)
        tmp2 = scrub_words(tmp1)
        seen = set()
        no_dup_tmp2 = []
        
        for item in tmp2:
            if item not in seen:
                seen.add(item)
                no_dup_tmp2.append(item)

        for item in no_dup_tmp2:
            if item in article_index.keys():
                article_index[item] = article_index.get(item, set())
                article_index[item].add(index)
            else:
                article_index[item] = {index}
    return article_index

def find_words(keywords, key_dict):
    intersect_docs = set()
    gather_map = {} 
    keyword_len = len(keywords)

    for key in keywords:
        if key in key_dict.keys():
            key_dict[key] = key_dict.get(key, set())

            for idx in key_dict[key]:
                if idx in gather_map.keys():
                    times = gather_map.get(idx)
                    gather_map[idx] = times+ 1
                else:
                    gather_map[idx] = gather_map.get(idx, 0) + 1

                if gather_map[idx] == keyword_len:
                    intersect_docs.add(idx)
    return intersect_docs