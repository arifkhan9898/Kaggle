#!/usr/bin/env python

from sklearn import svm
import csv_io
import math
from math import log
from sklearn import cross_validation
from sklearn.ensemble import GradientBoostingClassifier


def mean(numberList):
    if len(numberList) == 0:
        return float('nan')
 
    floatNums = [float(x) for x in numberList]
    return sum(floatNums) / len(numberList)

def getMedian(numericValues):

    theValues = sorted(numericValues)
    if len(theValues) % 2 == 1:
        return theValues[(len(theValues)+1)/2-1]
    else:
        lower = theValues[len(theValues)/2-1]
        upper = theValues[len(theValues)/2]
		
    return (float(lower + upper)) / 2  
	
def main():

    #random.seed(5)
    #random.random()
	
    startCol = 0
    endCol = 1775  # max = 1775

    trainBase = csv_io.read_data("../Data/train.csv")
	
    result = 100
    avg = 0
    bootstraps = 1 # should be ood for median
	
    rnd_start = 456
	

    predicted_list = []

    for n_est in [160,320,640,1280,4000,8000,16000]:
        for learn_r in [0.5, 0.2, 0.1, 0.05, 0.01, 0.005, 0.001]:
            bs = cross_validation.Bootstrap(len(trainBase) - 1, n_bootstraps=bootstraps, train_size=0.6, random_state=0)
            for train_index, test_index in bs:
	
                print n_est,learn_r
                #trainBaseTemp = [trainBase[i+1] for i in train_index]
                trainBaseTemp = trainBase
                target = [x[0] for x in trainBaseTemp][1001:3700]
                train = [x[1:] for x in trainBaseTemp][1001:3700]
	
                #testBaseTemp = [trainBase[i+1] for i in test_index]
                testBaseTemp = trainBase
                targetTest = [x[0] for x in testBaseTemp][1:1000]
                trainTest = [x[1:] for x in testBaseTemp][1:1000]
	
	
                test = csv_io.read_data("../Data/test.csv")
                test = [x[0:] for x in test]
	
	
                fo = open("gb_stats.txt", "a+")
    
                #learn_rate=0.1, n_estimators=200
                rf = GradientBoostingClassifier(loss='deviance', learn_rate=learn_r, n_estimators=n_est, subsample=1.0, min_samples_split=1, min_samples_leaf=1, max_depth=3, init=None, random_state=rnd_start) # , max_features=None

                rf.fit(train, target)
                prob = rf.predict_proba(trainTest)  # was test
	
                probSum = 0
                totalOffByHalf = 0
	
                for i in range(0, len(prob)):
                    probX = prob[i][1] # [1]
                    if ( probX > 0.999999999999):
                        probX = 0.999999999999;		
                    if ( probX < 0.000000000001):
                        probX = 0.000000000001;
                    #print i, probSum, probX, target[i]
                    #print target[i]*log(probX), (1-target[i])*log(1-probX)
                    probSum += targetTest[i]*log(probX)+(1-targetTest[i])*log(1-probX)
                    if ( math.fabs(probX - targetTest[i]) > 0.5 ):
                        totalOffByHalf = totalOffByHalf + 1		
			
                print "Total Off By > 0.5 ", totalOffByHalf
                print -probSum/len(prob)
	
                #fo.write(str(C) + "," + str(g) + "," + str(-probSum/len(prob)));
	
                avg += 	(-probSum/len(prob))/bootstraps
	
                #if ( -probSum/len(prob) < result ):
                #    result = -probSum/len(prob)
                #    predicted_probs = rf.predict_proba(test)  # was test
                #    predicted_probs = ["%f" % x[1] for x in predicted_probs]
                #    csv_io.write_delimited_file("../Submissions/svm_benchmark.csv", predicted_probs)
                #    print "Generated Data!!"
	
                predicted_probs = rf.predict_proba(test)  # was test
                predicted_list.append([x[1] for x in predicted_probs])
	
	
                fo.close()


    avg_list = []
    med_list = []
	
	
    for p in range(0, len(predicted_list[0])):
        temp_list =[]	
        for q in range(0, len(predicted_list)):		
		    temp_list.append(  predicted_list[q][p]) 
			
        avg_list.append( mean(temp_list) )
        med_list.append( getMedian(temp_list) )
		
        #print p, q, temp_list, mean(temp_list), getMedian(temp_list)
		
    med_values = ["%f" % x for x in med_list]
    csv_io.write_delimited_file("../Submissions/gb_med_benchmark.csv", med_values)	

    avg_values = ["%f" % x for x in avg_list]
    csv_io.write_delimited_file("../Submissions/gb_avg_benchmark.csv", avg_values)	
	
	
    print "Average: ", avg
		
    var = raw_input("Enter to terminate.")								
								
if __name__=="__main__":
    main()