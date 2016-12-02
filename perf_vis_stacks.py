#!/usr/bin/python
import json
import os
import sys

from collections import deque
from datetime import date
from optparse import OptionParser
from sets import Set

class Node:
  def __init__(self, name, comp, time):
    self.name = name
    self.comp = comp
    self.time = time
    self.children = {}

  def total_time(self):
    return self.time

  def self_time(self):
    child_time = 0.0
    for c in self.children.values():
      child_time += c.total_time()
    return self.total_time() - child_time

def Process(options, args):
  def jsonCallTree(node, is_root = False):
    ret = {}
    ret['name'] = node.name
    ret['comp'] = node.comp

    if len(node.children) > 0 or is_root:
      ret['children'] = []
      for c in sorted(node.children.values(), key=lambda c: -c.total_time()):
        ret['children'].append(jsonCallTree(c))
      if node.self_time() > 0.0:
        ret['children'].append({'name': '<self>', 'comp': ret['comp'], 'size': node.self_time()})
    else:
      ret['size'] = node.self_time()
    return ret

  def getComponent(name):
    if name.startswith('blink::'):
      return 'blink'
    elif name.startswith('cc::'):
      return 'cc'
    elif name.startswith('Sk') or name.startswith('sk_') or name.startswith('Gr'):
      return 'skia'
    return 'chromium'

  root_node = Node('<All Threads>', 'root', 0)

  for l in open(args[0], 'r').readlines():
    tok = l.strip().rsplit(' ', 1)
    stack = tok[0].split(';')
    time = float(tok[1])

    curr_node = root_node
    seen_names = {}

    for i, name in enumerate(stack):
      # Flatten all recursion and unknown symbols
      if (not name.startswith('0x')) and (not name in seen_names):
        seen_names[name] = 0
        node = curr_node.children.get(name, None)
        if not node:
          comp = 'Thread' if i == 0 else getComponent(name)
          node = Node(name, comp, time)
          curr_node.children[name] = node
        curr_node = node

  threads_json = jsonCallTree(root_node, True)

  out_path = options.output
  if not out_path:
    out_base = os.path.basename(args[0])
    today = date.today()
    out_path = out_base + '_%02d%02d%02d.html' % (today.day, today.month, today.year)

  vis_path = os.path.abspath(os.path.dirname(__file__))
  # Load template
  with open(vis_path + '/templates/perf-vis-template.html', 'r') as template_file:
    html_temp = template_file.read()

  # Add title
  html_temp = html_temp.replace('<page-title>', os.path.basename(out_path))

  # Add perf data json
  html_temp = html_temp.replace('<data_json>', json.dumps(threads_json, indent=0))

  # Add jquery-1.11.0.min.js
  with open(vis_path + '/third_party/jquery-1.11.0.min.js', 'r') as js:
    html_temp = html_temp.replace('<jquery-1.11.0.min.js>', js.read())

  # Add sammy-latest.min.js script
  with open(vis_path + '/third_party//sammy-latest.min.js', 'r') as js:
    html_temp = html_temp.replace('<sammy-latest.min.js>', js.read())

  # Add d3.v3.min.js script
  with open(vis_path + '/third_party//d3.v3.min.js', 'r') as js:
    html_temp = html_temp.replace('<d3.v3.min.js>', js.read())

  # Add jquery.dataTables.min.js
  with open(vis_path + '/third_party//jquery.dataTables.min.js', 'r') as js:
    html_temp = html_temp.replace('<jquery.dataTables.min.js>', js.read())

  # Add jquery.dataTables.min.css
  with open(vis_path + '/third_party//jquery.dataTables.css', 'r') as css:
    html_temp = html_temp.replace('<jquery.dataTables.css>', css.read())

  # Add perf-vis.js script
  with open(vis_path + '/templates/perf-vis.js', 'r') as js:
    html_temp = html_temp.replace('<perf-vis.js>', js.read())

  # Write result
  print '### perf-vis output:', os.path.join(os.getcwd(), out_path)
  with open(out_path, 'w') as html_file:
    html_file.write(html_temp)

if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-o", dest="output", default=None,
      type="string", help="Output filename")
  
  (options, arguments) = parser.parse_args()
  Process(options, arguments)
