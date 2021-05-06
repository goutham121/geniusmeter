 import csv
import time
import serial
import random
from decimal import *
import math
import json
from flask import Flask, make_response, request
import datetime


getcontext().prec = 10

uC = serial.Serial('/dev/ttyACM0',9600)
def loadCsv(filename):	
	lines = csv.reader(open(filename, "r"))
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset


def splitDataset(dataset, splitRatio):	
	trainSize = int(len(dataset) * splitRatio)
	trainSet = []
	copy = list(dataset)
	while len(trainSet) < trainSize:
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	return [trainSet, copy]


def separateByClass(dataset):
	separated = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if (vector[-1] not in separated):
			separated[vector[-1]] = []
		separated[vector[-1]].append(vector)
	return separated


def mean(numbers):
	return sum(numbers)/float(len(numbers))

def stdev(numbers):	
	avg = mean(numbers)
	variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)


def summarize(dataset):	
	summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
	del summaries[-1]	
	return summaries


def summarizeByClass(dataset): 
	separated = separateByClass(dataset)
	summaries = {}
	for classValue, instances in separated.items():
		summaries[classValue] = summarize(instances)
	return summaries


def calculateProbability(x, mean, stdev):	
	exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
	return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
def calculateClassProbabilities(summaries, inputVector):	
	probabilities = {}
	for classValue, classSummaries in summaries.items():
		probabilities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]
			x = inputVector[i]
			probabilities[classValue] *= calculateProbability(x, mean, stdev)
	return probabilities


def predict(summaries, inputVector):	
	probabilities = calculateClassProbabilities(summaries, inputVector)
	bestLabel, bestProb = None, -1
	for classValue, probability in probabilities.items():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel


def getPredictions(summaries, testSet):
	predictions = []
	for i in range(len(testSet)):
		result = predict(summaries, testSet[i])
		predictions.append(result)
	return predictions


def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

watthour = 0
ctemp = 0
noise = 0.03
def get_current():	
    global watthour,kwatthour
    voltage = 240
    line = uC.readline()
    string = float(line.replace('\r\n',''))
    if string == noise:
        power = abs(string-noise) * voltage
    else:
        power = abs(string) * voltage
    print("Power",power)
    watthour = watthour + power*10 
    kwh = watthour/3600000
    print("KWh",kwh)
    cost = round(50 + (7.74 * kwh),2)	
    print("Cost",cost)
    return string,kwh,cost,power
    #print(string)


def curr():	
    global ctemp
    current,kwh,cost,power = get_current()
    cdiff = current - ctemp
    ctemp = current
    return cdiff,kwh,cost,power


def tot():
    total = 0
	spike_limit = 5
    for x in xrange(0,spike_limit):
        current,kwh,cost,power = curr()
        total = total + current
        print ("Current",current)
    print ("Total",total)
    return total,kwh,cost,power
    total = 0

def listtotal():
    arr = []
    totalval,kwh,cost,power = tot()
    for i in xrange(0,5):
        arr.append([totalval])
    print arr
    return arr,kwh,cost,power

status1 = 0
status2 = 0
status3 = 0

def main():
	filename = 'Demo.csv'
	dataset = loadCsv(filename)
	summaries = summarizeByClass(dataset)          
	global status1
	global status2
	global status3
	while True:
		inputset,kwh,cost,power = listtotal()
		testSet=[]
		for x in range(0,4):
			testSet.append(inputset[x])
		print(testSet[0])
		predictions = getPredictions(summaries, testSet)

.if predictions[0]==1:
			status1 = status1 + 1
			string = 'CFL Bulb was switched ON'

		elif predictions[0]==2:
			status1 = status1 - 1
			string = 'CFL Bulb was switched OFF'

		elif predictions[0]==3:
			status2 = status2 + 1
			string = '20W Bulb was switched ON'

		elif predictions[0]==4:
			status2 = status2 - 1
			string = '20W Bulb was switched OFF'

		elif predictions[0]==5:
			status3 = status3 + 1
			string = 'HAIR DRYER was switched ON'

		elif predictions[0]==6:
			status3 = status3 - 1
			string = 'HAIR DRYER was switched OFF'

		time.sleep(0)
		return string,kwh,cost,status1,status2,status3,power
 output = {
		"current1": device,
		"killowatthour": kwh,
                "price": cost,
                "CFL": status1,
                "20": status2,
                "HAIR DRYER":status3,
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
