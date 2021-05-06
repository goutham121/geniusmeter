#script for Combinatorial Optimization

import itertools
import json
from flask import Flask, make_response, request
# pip install flask
import datetime
device_list = {'Fan': 100, 'CFL': 15, 'Bulb' : 20, 'Laptop Charger': 65 ,'HAIR DRYER' : 800}
device = device_list.keys()
device_watt = device_list.values() 
device_comb = []  
for a in xrange(1,len(device)+1):
    els = [list(b) for b in itertools.combinations(device, a)]
    device_comb.extend(els)
dev_comb_string = [] 
for c in device_comb:
    d = '+'.join(c)
    dev_comb_string.append(d)
device_watt_comb = []   
for e in xrange(1,len(device_watt)+1):
    g = [list(f) for f in itertools.combinations(device_watt, e)]
    device_watt_comb.extend(g)
sum_dev_watt = [] 
for h in device_watt_comb:
    sum_dev_watt.append(sum(h))

dev_watt_comb_string = zip(dev_comb_string,sum_dev_watt)
# print dev_watt_comb_string

watt =int(input())
diff = float('inf')
for value in sum_dev_watt: 
    if diff > abs(watt-value):
        diff = abs(watt-value)
        index = sum_dev_watt.index(value)
        key = dev_comb_string[index]


app = Flask(__name__)

@app.route("/")
def hello():
	# Error Calculation
  output = {
		"watt": watt,
		"key": key
	}

  cur = datetime.datetime.now()
  output['time'] = str(cur)
  response = json.dumps(output)
  if 'callback' in request.args:
    callback =	request.args['callback']
    response = callback + "("+response+");"

  return response
if __name__ == "__main__":
    app.run()
