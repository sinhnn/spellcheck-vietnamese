# vim: set et sw=2 ts=2 tw=79 : # 
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# File              : 
# Author            : sinhnn <sinhnn.92@gmail.com>
# Date              : 18.01.2019
# Last Modified Date: 18.01.2019
# Last Modified By  : sinhnn <sinhnn.92@gmail.com>

import json
import dpath.util
from fuzzywuzzy import process
#from string_distance import StringDistance
import itertools
import logging
import re
import sys

__END_WORD_SYMBOL__ = '_'
logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

__VN_chars__='aáàăắằẵẳặâấầẫẩậãảạbcdđeéèêếềễểệẽẻẹfghiíìĩỉịjklmnoóòôốồỗổộõỏọơớờỡởợpqrstuúùũủụưứừữửựvwxyýỳỹỷỵz'
__VN_CHARS__='AÁÀĂẮẰẴẲẶÂẤẦẪẨẬÃẢẠBCDĐEÉÈÊẾỀỄỂỆẼẺẸFGHIÍÌĨỈỊJKLMNOÓÒÔỐỒỖỔỘÕỎỌƠỚỜỠỞỢPQRSTUÚÙŨỦỤƯỨỪỮỬỰVWXYÝỲỸỶỴZ'
__VN_WORD_REGEX__ =  r'^[{}]+$'.format(__VN_chars__) # Match regex does not mean, it's regular word
__NOT_VN_CHAR_REGEX__ = r'[^{}]'.format(__VN_chars__)


__WORD_NOT_IN_DICT__ = {}
__VN_REPLS = {u"[àảãáạ]": u"a",     u"[ÀẢÃÁẠ]": u"A",
              u"[ăằẳẵắặ]": u"ă",    u"[ĂẰẲẴẮẶ]": u"Ă",
              u"[âầẩẫấậ]": u"â",    u"[ÂẦẨẪẤẬ]": u"Â",
              u"[èẻẽéẹ]": u"e",     u"[ÈẺẼÉẸ]": u"E",
              u"[êềểễếệ]": u"ê",    u"[ÊỀỂỄẾỆ]": u"Ê",
              u"[ìỉĩíị]": u"i",     u"[ÌỈĨÍỊ]": u"I",
              u"[òỏõóọ]": u"o",     u"[ÒỎÕÓỌ]": u"O",
              u"[ôồổỗốộ]": u"ô",    u"[ÔỒỔỖỐỘ]": u"Ô",
              u"[ơờởỡớợ]": u"ơ",    u"[ƠỜỞỠỚỢ]": u"Ơ",
              u"[ùủũúụ]": u"u",     u"[ÙỦŨÚỤ]": u"U",
              u"[ưừửữứự]": u"ư",    u"[ƯỪỬỮỨỰ]": u"Ư",
              u"[ỳỷỹýỵ]": u"y",     u"[ỲỶỸÝỴ]": u"Y"}

# Extra methods for dicitonary ------------------------------
def get_dict_depth(d, level=1):
  if not isinstance(d, dict) or not d: return level
  return max(get_dict_depth(d[k], level + 1) for k in d)

# All key at n-th level of dict
def get_nth_level(_dict, n, _list = []):
  depth = get_dict_depth(_dict,level=1)
  if n <= 0:
    print("Invalid depth")
    return None
  if n > depth : n = depth;
  # 1 is root
  if n == 1:
    if isinstance(_dict, dict): _list += list(_dict.keys())
    elif isinstance(_dict, list):  _list += _dict
    return None
  else: 
    for k, v in _dict.iteritems():
      get_nth_level(v, n - 1, _list)

# Convert all keys, values from utf8 to str
def utf8_to_str(d, nd):
  for k, v in d.iteritems():
    nk = str(k.encode('utf-8'));
    if isinstance(v, dict):
      nd[nk] = {};
      utf8_to_str(v, nd[nk])
    elif isinstance(v, list):
      nd[nk] = [];
      for vv in v: nd[nk].append(str(vv.encode('utf-8')));
    else: nd[nk] = str(v.encode('utf-8'));

# Get full path to all leaves
def get_full_path_to_all_leaves(_dict, prefix, _list,separator='|'):
  level = 1;
  level = get_dict_depth(_dict, level);
  if level == 1:
    _list.append(prefix + str(_dict));
    return True
  for key in _dict.keys():
    _prefix = prefix + str(key) + separator
    get_full_path_to_all_leaves(_dict[key], _prefix,  _list,separator)

# Convert dict path to list
def to_list(d,prefix=[]):
  for k, v in d.iteritems():
    if prefix: prefix += [str(k)];
    else: prefix += [str(k)];
    if isinstance(v, dict): return to_list(v,prefix)
    else: return prefix


def valid_path(d, validpath=[], *path):
    if (len(path) == 0): 
        return valid_path
    try: 
        return valid_path(d[path[0]], validpath = valid_path + [path[0]], list(path[1:]))
    except KeyError:
        print("Invalid key: '{}'".format(path[0]))
        return valid_path[0:-1]

def get_path(d, *path):
    if len(path) == 0: return d
    try:
        return get_path(d[path[0]], path[1:])
    except KeyError:
        print("Invalid key: '{}'".format(path[0]))
        return False


# ----------------------------------------------------------------------------
class SpellCheck():
  _dict = {};

  def __init__(self, dictf=''):
    if dictf == '':
      self._dict = {}
    else: self.load_vocab_dict(dictf)

  def load_vocab_dict(self, inf):
    with open(inf, 'r') as f:
      self._dict = json.load(f)

  def word_exist(self, word):
    logger.debug('Validating {}'.format(word))
    _path = '/'.join(list(word))
    logger.debug(dpath.util.search(self._dict, _path, yielded=False))
    if dpath.util.search(self._dict, _path, yielded=False) == __WORD_NOT_IN_DICT__:
      logger.debug("{} not in dictionary".format(word))
      logger.info("`{}` not in dictionary".format(word))
      return False
    x = dpath.util.get(self._dict, _path);
    if not isinstance(x, dict): 
      logger.debug("`{}` found, but result is not dictionary, result is {}".format(word, x))
      return False
    if __END_WORD_SYMBOL__ in x.keys():
      return True

    maybes = []
    get_full_path_to_all_leaves(x, prefix=word, _list=maybes,separator='')
    for i, maybe in enumerate(maybes): maybes[i] = maybe[:-1]
    logger.info("`{}` not found, but maybe {} !".format(word, '|'.join(maybes)))
    return False

  def path_exist(self, word):
    ls = list(word)
    if dpath.util.get(self._dict, '/'.join(ls)): return True
    else: False

  def add_word_to_dict(self, word):
    if self.word_exist(word):
      logger.debug("{} existed".format(word))
      return False
    ls = list(word)
    logger.info("Adding `{}` to dict".format(word))
    dpath.util.new(self._dict, '/'.join(ls), {__END_WORD_SYMBOL__:''})
    return True

  def update_dict_from_file(self, vocab_file):
    f = open(vocab_file, 'r')
    contents = f.read() 
    words = re.split(__NOT_VN_CHAR_REGEX__, contents, flags=re.IGNORECASE)
    for w in words:
      word = w.lower()
      if  re.search(__VN_WORD_REGEX__, word):
        self.add_word_to_dict(word) 

  def write_dict(self, of):
    with open(of, 'w') as f:
      json.dump(self._dict, f,ensure_ascii=False)
    return True

  # def check_str(self, _str):
  def check_word(self, word):
    x = self.word_exist(word)
    # if not x: return 

  def check_file_v1(self, infile):
    f = open(infile, 'r')
    contents = f.read() 
    words = re.split(r'[^{}0-9]'.format(__VN_CHARS__), contents, flags=re.IGNORECASE)
    for word in words:
      if word: 
        if re.search(r'[{}]'.format(__VN_chars__), word, flags=re.IGNORECASE):
          self.check_word(word.lower())

  def check_file(self, infile):
    f = open(infile, 'r')
    contents = f.readlines() 
    for i, line in enumerate(contents, 1):
      content = line.strip()
      logger.info("{}:{} -- {}".format(infile, i, content))
      words = re.split(r'[^{}0-9]'.format(__VN_CHARS__), content, flags=re.IGNORECASE)
      for word in words:
        if word: 
          if re.search(r'[{}]'.format(__VN_chars__), word, flags=re.IGNORECASE):
            self.check_word(word.lower())


  def show_vocab(self,of):
    _list = []
    get_full_path_to_all_leaves(self._dict, '', _list, separator='')
    with open(of, 'w') as f:
      for l in _list:
        f.write(re.sub(r'_','', l) + '\n')

if __name__ == "__main__":

  import os
  import sys
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('--infile', help='Input file, for checking spell or update dictionary')
  parser.add_argument('--dict-file', help='A dictionary file, json format', default='')
  parser.add_argument('--update-dict', help='Update dict-file from loading infile:True or False', default=False)
  parser.add_argument('--odfile', help='Output dictionary file')
  parser.add_argument('--ovfile', help='Output vocabulary file')
  parser.add_argument('--debug', help='Debug flags', default=False)
  args = parser.parse_args()

  a = SpellCheck(args.dict_file)
  if args.update_dict :
    a = SpellCheck()
    a.update_dict_from_file(args.infile)
    a.write_dict(args.odfile)
    try:
      a.show_vocab(args.ovfile)
    except:
      pass
  else:
    if args.dict_file == '':
      print("Required a dictionary file by --dict-file")
    else: 
      a.check_file(args.infile)
