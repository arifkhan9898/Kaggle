#!/usr/bin/env python

from sklearn import svm
import csv_io
import math
from math import log
from sklearn import cross_validation

#http://www2005.org/cdrom/docs/p1072.pdf
#We have experimentally compared five types of data partitioning 
#ensemble of SVMs on two well-accepted benchmark collections, 
#i.e. Reuters-21578 and 20-Newsgroup, and found that disjunct 
#partitioning ensembles of SVMs with stacking performed best and 
#consistently outperformed the single SVM. We also found 
#bagging and cluster partitioning ensembles are not effective to 
#combine strong classifiers like SVM, and boosting always 
#achieves worse results on all of the collections

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
	
	# this method does not seem to benefit from using less than all columns of data.
    startCol = 0
    endCol = 1775  # max = 1775

    trainBase = csv_io.read_data("../Data/train.csv")
	
    result = 100
    avg = 0
    avg_sum = 0
    avg_counter = 0
    bootstraps = 9
	
    predicted_list = []
	
    bs = cross_validation.Bootstrap(len(trainBase) - 1, n_bootstraps=bootstraps, train_size=0.7, random_state=0)
    for train_index, test_index in bs:
	
        trainBaseTemp = [trainBase[i+1] for i in train_index]
        #trainBaseTemp = trainBase
        target = [x[0] for x in trainBaseTemp]#[1001:3700]
        train = [x[startCol+1:endCol+1] for x in trainBaseTemp]#[1001:3700]
	
        testBaseTemp = [trainBase[i+1] for i in test_index]
        #testBaseTemp = trainBase
        targetTest = [x[0] for x in testBaseTemp]#[1:1000]
        trainTest = [x[startCol+1:endCol+1] for x in testBaseTemp]#[1:1000]
	
	
        test = csv_io.read_data("../Data/test.csv")
        test = [x[startCol:endCol] for x in test]
	
	
        fo = open("svm_stats.txt", "a+")
    
		# good for rbf method
        CC=[0.0]
        gg = [-5.5]
	
        for g in gg:	
            for C in CC:			
                svc = svm.SVC(probability=True, C=10**C, gamma=2**g,cache_size=800, coef0=0.0, degree=3, kernel='rbf', shrinking=True, tol=0.01)
                svc.fit(train, target)
                prob = svc.predict_proba(trainTest)  # was test
	
                probSum = 0
                totalOffByHalf = 0
				
                for i in range(0, len(prob)):
                    #print i, probSum, prob[i][1], target[i]
                    #print target[i]*log(prob[i][1]), (1-target[i])*log(1-prob[i][1])
                    probSum += targetTest[i]*log(prob[i][1])+(1-targetTest[i])*log(1-prob[i][1])
                    if ( math.fabs(prob[i][1] - targetTest[i]) > 0.5 ):
                        totalOffByHalf = totalOffByHalf + 1		
	
                #print probSum	
                #print len(prob)	
                print "Total Off By > 0.5 ", totalOffByHalf
                print "C: ", 10**C, " gamma: " ,2**g
                #print "C: ", 10**C[y], " gamma: " ,2**g[y]
                print -probSum/len(prob)
	
                #fo.write(str(C[y]) + "," + str(g[y]) + "," + str(-probSum/len(prob)));
                fo.write(str(C) + "," + str(g) + "," + str(-probSum/len(prob)));
				
                avg_sum += 	(-probSum/len(prob))
                avg_counter = avg_counter + 1 
				
                #if ( -probSum/len(prob) < result ):
                #    result = -probSum/len(prob)
                #    predicted_probs = svc.predict_proba(test)  # was test
                #    predicted_probs = ["%f" % x[1] for x in predicted_probs]
                #    csv_io.write_delimited_file("../Submissions/svm_benchmark.csv", predicted_probs)
                #    print "Generated Data!!"
	
	
                predicted_probs = svc.predict_proba(test)  # was test
                predicted_list.append([x[1] for x in predicted_probs])
	
        fo.close()

		
    avg_list = []
    med_list = []
	
	
    for p in range(0, len(test)):
        temp_list =[]	
        for q in range(0, len(predicted_list)):		
		    temp_list.append(  predicted_list[q][p]) 
			
        avg_list.append( mean(temp_list) )
        med_list.append( getMedian(temp_list) )
		
        print p, q, temp_list, mean(temp_list), getMedian(temp_list)
		
    med_values = ["%f" % x for x in med_list]
    csv_io.write_delimited_file("../Submissions/svm-rbf_med_benchmark.csv", med_values)	

    avg_values = ["%f" % x for x in avg_list]
    csv_io.write_delimited_file("../Submissions/svm-rbf_avg_benchmark.csv", avg_values)	
	
	
    print "Average: ", (avg_sum/avg_counter)
		
		
    var = raw_input("Enter to terminate.")								
								
if __name__=="__main__":
    main()