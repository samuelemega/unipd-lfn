import pickle
import requests
from multiprocessing import Pool, Process, cpu_count
import bz2
import re
import numpy as np

TIMESTAMP = "2024-12-31T23:59:59Z"

pattern_wikilink = r"\[\[([^\|\]]+)(?:\|[^\]]*)?\]\]"
wikilink_regex = re.compile(pattern_wikilink)

"""
  match_wikilinks
"""
def match_wikilinks(value):
  return wikilink_regex.findall(value)

"""
  expand_body
"""
def expand_body(body):
  return body

"""
  Parser
"""
class Parser:
  def __init__(self):
    self.idx = {}
    """
      expand_body
    """
    self.reset()

  def reset(self):
    self.title = None
    self.namespace = None
    self.redirect = None
    self.timestamp = None
    self.body = ""
    self.wikilinks = []
    self.is_reading_body = False

  def parse_offset(self, xml_file, offset):
    xml_file.seek(int(offset))
    unzipper = bz2.BZ2Decompressor()
    uncompressed_data = b"";

    while True:
      compressed_data = xml_file.read(262144)

      try:
        uncompressed_data += unzipper.decompress(compressed_data)
      except EOFError:
        break

      if compressed_data == "" and unzipper.need_input:
          break

    lines = uncompressed_data.decode("utf-8").split("\n")

    for line in lines:

      if self.is_reading_body and self.timestamp < TIMESTAMP:
        self.body += line

      if line.startswith("  <page>"):
        self.reset()

      if line.startswith("    <title>"):
        self.title = line[11:-8]

      if line.startswith("    <ns>"):
        self.namespace = line[8:-5]

      if line.startswith("    <redirect "):
        self.redirect = line[21:-4]

      if line.startswith("      <timestamp>"):
        self.timestamp = line[17:-12]

      if line.startswith("      <text ") and self.timestamp < TIMESTAMP:
        self.body += line
        self.is_reading_body = True

      if "</text>" in line and self.timestamp < TIMESTAMP:
        self.body += line
        self.is_reading_body = False

      if line.startswith("  </page>"):
        self.idx[self.title] = {
          "namespace": self.namespace,
          "redirect": self.redirect,
          "wikilinks": match_wikilinks(self.body)
        }

"""
  task
"""
def task(offsets):
  parser = Parser()
  print("Task")

  with open("files/dump.bz2", "br") as xml_file:
    for offset in offsets:
      parser.parse_offset(xml_file, offset)

  return parser.idx

"""
  main
"""
if __name__ == "__main__":
  with open("files/toc.pkl", "br") as file:
    toc = pickle.load(file)

  cpu_count = cpu_count()

  offsets = list(set(toc.values()))
  offsets = np.array_split(offsets, cpu_count)

  with Pool(processes=cpu_count) as pool:
    results = pool.map(task, offsets)

  idx = {}

  for result in results:
    idx = idx | result

  with open("files/idx.pkl", "wb") as file:
    pickle.dump(idx, file)
