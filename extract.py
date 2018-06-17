try: #python3
  import urllib.request as pyurllib
except: #python2
  import urllib2 as pyurllib

import pycrfsuite
import pickle
import sys
import argparse
import lxml.html

from lxml import etree
from train_set_generator import get_features, sanitize_html

def parse_arguments(argv):
  parser = argparse.ArgumentParser(description='Content Extractor')
  parser.add_argument('--url')
  return parser.parse_args(argv)

def main(argv):
  args = parse_arguments(argv)

  if args.url == None:
    print('Give the url of news that you want to be extracted using --url <URL>')
    return

  url = args.url
  if url[:4] != 'http':
    url = 'http://' + url
  html_file = pyurllib.urlopen(url).read()

  curr_node = -1

  X = []
  text_data = []

  html_data = sanitize_html(html_file)
  for h in html_data:
    curr_node += 1  
    f = get_features(h)
    X.append({ k:v for k,v in f.items() if k != 'txt_inside' })
    text_data.append(f['txt_inside'])

  tagger = pycrfsuite.Tagger()
  tagger.open('model/html-content-extractor.crfsuite')

  y_pred = [tagger.tag(xseq) for xseq in [X]]

  i = 0
  for y in y_pred[0]:
    #print(str(y) + '|' + str(X[i]) + str(text_data[i]))
    if y == 'content':
      print(X[i])
      print(text_data[i])
    i += 1  

if __name__ == "__main__":
  main(sys.argv[1:])
