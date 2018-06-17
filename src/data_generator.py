from collections import defaultdict

import lxml.html
from lxml import etree

import json
import sys
import math
import csv
import os
import pickle

def round_down(num, divisor):
  if (num > 0 and num < 10): return int(num)
  if (num%divisor == 0): return int(num)
  return int(num + divisor - num%divisor)

def get_len(text):
  return len((text and text.strip()) or [])

def get_text_influence(text_count):
  num = round_down(text_count, 10)
  if num > 100:
    num = 100
  return float(num)

def get_features(h):
  text_inside = h.xpath('text()[normalize-space()]')
  text_inside_str = ' '.join([text.strip() for text in text_inside])

  attr_tag = h.tag                    
  attr_parent_tag = '_'

  if h.getparent() is not None:
    attr_parent_tag = h.getparent().tag
  
  txt_all = ' '.join([text.strip() for text in h.xpath('//text()[normalize-space()]')])

  attr_text_inside_before_class = get_text_influence(get_len(h.text))
  attr_text_after_class = get_text_influence(get_len(h.tail))
  attr_text_len_inside_class = get_text_influence(len(text_inside_str))
  attr_text_word_count_class = get_text_influence(text_inside_str.count(' '))

  return { "tag": attr_tag, 
    "ptag": attr_parent_tag, 
    "chain_tag": '%s|%s' % (attr_tag, attr_parent_tag), 
    "txt_ib": attr_text_inside_before_class, 
    "txt_a": attr_text_after_class, 
    "txt_li": attr_text_len_inside_class, 
    "word_count": attr_text_word_count_class,
    "txt_inside": text_inside }

def sanitize_html(html_file):
  html = lxml.html.fromstring(html_file)

  for element in html.xpath("//script|//style|//meta|//link|//option|//iframe"):
    element.getparent().remove(element) 

  return (h for h in html.iter() if h.tag != etree.Comment)  

def main():
  dataset = ['train', 'validation', 'test']
  feature = defaultdict(lambda: [])
  label = defaultdict(lambda: [])

  for settype in dataset:
    for root, dirs, files in os.walk('data/'+ settype +'/html'):
      for filename in files:
        tsv_filepath = (root + '/' + filename).replace('html', 'tsv')
        print(filename)

        with open(os.path.join(root, filename)) as html_file, open(tsv_filepath) as tsv_file:
          tsv_label = list(csv.reader(tsv_file, delimiter='\t'))
          curr_node = -1

          X = []
          y = []

          html_data = sanitize_html(html_file.read())          
          for h in html_data:
            curr_node += 1            
            f = get_features(h)

            if (tsv_label[curr_node][2] == f['tag']):
              attr_target_class = tsv_label[curr_node][0]
            else:
              print("Invalid mapping of label. Got: " + f[0] + " | Expected: " + tsv_label[curr_node][2])
              sys.exit(0)
            
            X.append({ k:v for k,v in f.items() if k != 'txt_inside' })
            y.append(attr_target_class)

          feature[settype].append(X)
          label[settype].append(y)

    pickle.dump(feature[settype], open('pickle/{0}.x.p'.format(settype), 'wb'))
    pickle.dump(label[settype], open('pickle/{0}.y.p'.format(settype), 'wb'))

if __name__ == "__main__":
  main()
