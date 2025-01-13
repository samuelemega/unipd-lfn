"""
  Author: Samuele Mega
"""

import html
from multiprocessing import Pool, Process, cpu_count
import time
import re
import pickle
import numpy as np

RESOLVE_MAX_DEPTH = 20
ARTICLE_NAMESPACE = "0"
CATEGORY_NAMESPACE = "14"

missed_articles = []
missed_categories = []

"""
  normalize_title
"""
def normalize_title(value):
  value = html.unescape(value)
  value = value.strip().strip("_")

  if len(value) == 0:
    return None

  value = value[0].upper() + value[1:]
  value = re.sub(r"\s+", " ", value)

  return value

"""
  normalize_category
"""
def normalize_category(value):
  return normalize_title(value[10:])

"""
  resolve_article
"""
def resolve_article(idx, title):
  count = 0

  original_title = title
  title = normalize_title(title)

  if title not in idx:
    return None

  while idx[title]["redirect"] is not None and count < RESOLVE_MAX_DEPTH:

    title = normalize_title(idx[title]["redirect"])
    count += 1

    if count == RESOLVE_MAX_DEPTH or title not in idx:
      missed_articles.append((original_title, title))
      return None

  return title

"""
  resolve_category
"""
def resolve_category(idx, title):
  count = 0

  original_title = title
  title = normalize_category(title)

  if title not in idx:
    return None

  while idx[title]["redirect"] is not None and count < RESOLVE_MAX_DEPTH:

    title = normalize_category(idx[title]["redirect"])
    count += 1

    if count == RESOLVE_MAX_DEPTH or title not in idx:
      missed_categories.append((original_title, title))
      return None

  return title

"""
  split_dict
"""
def split_dict(obj, num):
  result = [{} for index in range(num)]

  for index, (k, v) in enumerate(obj.items()):
    result[index % num][k] = v # round-robin split

  return result

"""
  task
"""
def task(articles, categories):

  print("Task")


"""
  main
"""
if __name__ == "__main__":

  cpu_count = cpu_count()

  with open("files/idx.pkl", "rb") as file:
    idx = pickle.load(file)

  articles = {
    normalize_title(k): v
    for k, v in idx.items()
    if v["namespace"] == ARTICLE_NAMESPACE
  }

  categories = {
    normalize_category(k): v
    for k, v in idx.items()
    if v["namespace"] == CATEGORY_NAMESPACE
  }

  nodes = {
    k: {
      "categories": list(set([
        resolve_category(categories, wikilink)
        for wikilink in v["wikilinks"]
        if wikilink[:10] == "Categoria:"
        and normalize_category(wikilink) in categories
      ])),
      "links": list(set([
        resolve_article(articles, wikilink)
        for wikilink in v["wikilinks"]
        if normalize_title(wikilink) in articles
      ]))
    } for k, v in articles.items()
  }

  with open("files/nodes.pkl", "wb") as file:
    pickle.dump(nodes, file)

  with open("files/missed_articles.pkl", "wb") as file:
    pickle.dump(missed_articles, file)

  with open("files/missed_categories.pkl", "wb") as file:
    pickle.dump(missed_categories, file)
