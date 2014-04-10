#!/usr/bin/env python

import csv_io
import math

from math import log
import string
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsRegressor

import shutil

def toFloat(str):
	return float(str)

def myFunc(arr):
	#print "myFunc: ", arr
	arr1 = arr[0]
	
	newArr = []
	for index, data in enumerate(arr1):
		if index == 0 and data == 0.0:
			newArr.append(0.0)
		else:
			#newArr.append(1.0/data)
			newArr.append(1.0)
	#print newArr
	return [newArr]
	
	
def PreProcess3():


	trainBase = csv_io.read_data("PreProcessData/training_PreProcess2.csv", split="\t" ,skipFirstLine = False)
	test = csv_io.read_data("PreProcessData/test_PreProcess2.csv", split="\t" ,skipFirstLine = False)
	#weights = csv_io.read_data("PreProcessData/Weights.csv", skipFirstLine = False)
	
	print "Train Size: ", len(trainBase[0]), "Test Size: ", len(test[0])

	
	shutil.copy2("PreProcessData/DataClassList2.csv", "PreProcessData/DataClassList3.csv")
	
	lat = len(trainBase[0]) - 2
	long = len(trainBase[0]) - 1

	
	#target = [x[0] for x in trainBase]
	train = [x[lat:long + 1] for x in trainBase]

	
	n_neighborsArr = [4]
	leaf_sizeArr = [30]
	featuresArr = [8]	
	featuresArr = range(8, len(trainBase[0]) - 2)

	for feature in featuresArr:
		for n_neighbor in n_neighborsArr:
			for leaf_s in leaf_sizeArr:	
			
				targetNew = []
				trainNew = []
			
				print "Feature", feature
				print "Training neighbors: ", n_neighbor, "leaf_size: ", leaf_s
				
				target = [x[feature] for x in trainBase]
				
				for index,targ in enumerate(target):
					if ( targ != "" and targ != "NA" and targ != "0" and targ != "0.0" and targ != 0 and targ != 0.0):
						targetNew.append(target[index])
						trainNew.append(train[index])
						#print "Data", target[index], train[index]
						#print "IN", targ
					#else:
						#print "OUT", targ
				
				# append test set for more powerful training.
				target = [x[feature - 1] for x in test]
				
				for index,targ in enumerate(target):
					if ( targ != "" and targ != "NA" and targ != "0" and targ != "0.0" and targ != 0 and targ != 0.0):
						targetNew.append(target[index])
						trainNew.append(train[index])
						#print "Data", target[index], train[index]
						#print "IN", targ
					#else:
						#print "OUT", targ
				
				neigh = KNeighborsRegressor(n_neighbors=n_neighbor,warn_on_equidistant=False, leaf_size=leaf_s, algorithm="ball_tree", weights=myFunc) 
				neigh.fit(trainNew, targetNew) 
							

				
				for index, data in enumerate(trainBase):
					if ( data[feature] == "" or data[feature] == "NA" or data[feature] == "0" or data[feature] == "0.0" or data[feature] == 0 or data[feature] == 0.0):
						pred = neigh.predict([data[lat], data[long]])
						#print "PRED", data[lat], data[long], "Prediction: ", pred[0],data[feature]
						trainBase[index][feature] = pred[0]
					#else:
						#print "DATA" ,data[feature]
					
				
				for index, data in enumerate(test):
					if ( data[feature - 1] == "" or data[feature - 1] == "NA" or data[feature - 1] == "0" or data[feature - 1] == "0.0" or data[feature - 1] == 0 or data[feature - 1] == 0.0):
						pred = neigh.predict([data[lat - 1], data[long - 1]])
						#print data[lat - 1], data[long - 1], "Prediction: ", pred[0]
						test[index][feature - 1] = pred[0]
				
		
	
	if ( len(n_neighborsArr) > 1 ):	
		return

	

	print "Writing Data"
	csv_io.write_delimited_file("PreProcessData/training_PreProcess3.csv", trainBase, delimiter="\t")		
	csv_io.write_delimited_file("PreProcessData/test_PreProcess3.csv", test, delimiter="\t")
	print "Done."	


		
if __name__=="__main__":


	


	print "Creating Missing Data predictors."
	PreProcess3()
