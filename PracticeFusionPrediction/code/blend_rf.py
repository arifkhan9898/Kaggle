#!/usr/bin/env python

from sklearn.linear_model import LogisticRegression
import csv_io
import math

from math import log
import string

import stack_rf

import numpy as np
import datetime

import random

def Blend():
	
	
	trainBase = csv_io.read_data("PreProcessData/training_PreProcess2.csv", False)
	
	SEED = 448
	random.seed(SEED)
	random.shuffle(trainBase)
	
	target = [x[0] for x in trainBase]
	
	dataset_blend_train, dataset_blend_test = stack_rf.run_stack(SEED)

	clf = LogisticRegression()
	clf.fit(dataset_blend_train, target)
	submission = clf.predict_proba(dataset_blend_test)[:,1]
	
 	submission = ["%f" % x for x in submission]
	now = datetime.datetime.now()
	csv_io.write_delimited_file_GUID("../Submissions/stack" + now.strftime("%Y%m%d%H%M") + ".csv", "PreProcessData/test_PatientGuid.csv", submission)	
	
	# attempt to score the training set to predict score for blend...
	probSum = 0.0
	trainPrediction = clf.predict_proba(dataset_blend_train)[:,1]
	for i in range(0, len(trainPrediction)):
		probX = trainPrediction[i]
		if ( probX > 0.999):
			probX = 0.999;		
		if ( probX < 0.001):
			probX = 0.001;

		probSum += int(target[i])*log(probX)+(1-int(target[i]))*log(1-probX)
		 
	print "Train Score: ", (-probSum/len(trainPrediction))
	
	
	
		
	trainPredictionNew = stack_rf.SimpleScale(trainPrediction, floor = 0.001, ceiling = 0.999)
	probSum = 0.0
	for i in range(0, len(trainPredictionNew)):
		probX = trainPredictionNew[i]
		if ( probX > 0.999):
			probX = 0.999;		
		if ( probX < 0.001):
			probX = 0.001;

		probSum += int(target[i])*log(probX)+(1-int(target[i]))*log(1-probX)
		 
	print "Train Score for 0.999 and 0.001 with SimpleScale: ", (-probSum/len(trainPredictionNew))
	

	trainPredictionNew = stack_rf.SimpleScale(trainPrediction, floor = 0.01, ceiling = 0.99)
	probSum = 0.0
	for i in range(0, len(trainPredictionNew)):
		probX = trainPredictionNew[i]
		if ( probX > 0.999):
			probX = 0.999;		
		if ( probX < 0.001):
			probX = 0.001;

		probSum += int(target[i])*log(probX)+(1-int(target[i]))*log(1-probX)
		 
	print "Train Score for 0.99 and 0.01 with SimpleScale: ", (-probSum/len(trainPredictionNew))
	

	trainPredictionNew = stack_rf.SimpleScale(trainPrediction, floor = 0.05, ceiling = 0.95)
	probSum = 0.0
	for i in range(0, len(trainPredictionNew)):
		probX = trainPredictionNew[i]
		if ( probX > 0.999):
			probX = 0.999;		
		if ( probX < 0.001):
			probX = 0.001;

		probSum += int(target[i])*log(probX)+(1-int(target[i]))*log(1-probX)
		 
	print "Train Score for 0.95 and 0.05 with SimpleScale: ", (-probSum/len(trainPredictionNew))
	
	
	
	submissionNew = stack_rf.SimpleScale(submission, floor = 0.001, ceiling = 0.999)
	csv_io.write_delimited_file_GUID("../Submissions/stack" + now.strftime("%Y%m%d%H%M") + "_SimpleScale999.csv", "PreProcessData/test_PatientGuid.csv", submissionNew)	
		
		
	submissionNew = stack_rf.SimpleScale(submission, floor = 0.01, ceiling = 0.99)	
	csv_io.write_delimited_file_GUID("../Submissions/stack" + now.strftime("%Y%m%d%H%M") + "_SimpleScale99.csv", "PreProcessData/test_PatientGuid.csv", submissionNew)	

	submissionNew = stack_rf.SimpleScale(submission, floor = 0.05, ceiling = 0.95)	
	csv_io.write_delimited_file_GUID("../Submissions/stack" + now.strftime("%Y%m%d%H%M") + "_SimpleScale95.csv", "PreProcessData/test_PatientGuid.csv", submissionNew)	
	
	
	var = raw_input("Enter to terminate.")	
											
if __name__=="__main__":
	Blend()