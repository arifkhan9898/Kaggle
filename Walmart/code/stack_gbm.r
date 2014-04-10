require(gbm)
require(caret)

Xtrain <- as.matrix(read.table("train.csv",
                   header=TRUE,
                   sep= ","       
                   ))
Xtest <- as.matrix(read.table("test.csv",
                   header=TRUE,
                   sep= ","       
                   ))
				   
				   
print("Loaded Data")


#names(Xtrain)
#summary(Xtrain)
#dim(Xtrain)
#dim(Xtest)






bestScore = 500000.0

CVFolds = 4
Repeats <- 3
targetCOlumn = 5
weightColumn = 17
features = "all"
algorithm = "gbm"

trainPredictions <- matrix(data=0,nrow=nrow(Xtrain),ncol=Repeats)
testPredictions <- matrix(data=0,nrow=nrow(Xtest),ncol=Repeats*CVFolds) 

ntrees = 10000


finalScore = 0.0
for(repeats in 1:Repeats) {

  
  folds <- createFolds(Xtrain[,targetCOlumn], k = CVFolds)
  setScore = 0.0
  for(cvFolds in 1:CVFolds) {

    print(paste("Repeat: ", as.character(repeats)))
    print(paste("CVFold: ", as.character(cvFolds)))

    
    
		YY <- Xtrain[-folds[[cvFolds]],targetCOlumn]	
		XX <- Xtrain[-folds[[cvFolds]],-targetCOlumn]
    
    
		print(Sys.time())

		#SVMmodel <- svm(x=XX, y=as.numeric(YY),type="eps-regression", kernel="polynomial", degree=3, coef0=0, cost=1, nu=0.5, class.weights=NULL,cachesize=40, tolerance=0.001, epsilon=0.1, shrinking=TRUE, cross=0, fitted=TRUE, seed=5) # , gamma=1/dim(x)[2]
		
		gbm1 <-
		  gbm.fit(x=XX, y=as.numeric(YY),
		      #var.monotone=c(0,0,0,0,0,0), # -1: monotone decrease, # +1: monotone increase,# 0: no monotone restrictions
		      distribution="gaussian", # see the help for other choices
		      n.trees=ntrees, # number of trees
		      shrinkage=0.05, # shrinkage or learning rate,   # 0.001 to 0.1 usually work
		      interaction.depth=3, # 1: additive model, 2: two-way interactions, etc.
		      bag.fraction = 0.5, # subsampling fraction, 0.5 is probably best
		      #train.fraction = 1.0, # fraction of data for training,12 gbm
		      # first train.fraction*N used for training
		      n.minobsinnode = 10, # minimum total weight needed in each node
		      #cv.folds = 1, # do 3-fold cross-validation
		      keep.data=TRUE, # keep a copy of the dataset with the object
		      verbose=FALSE, # don't print out progress
		      #n.cores=1
          w=Xtrain[-folds[[cvFolds]],weightColumn]
          ) # use only a single core (detecting
    
    
		#best.iter <- gbm.perf(gbm1,method="OOB")
		#print(best.iter)
		
    
		YY <- Xtrain[folds[[cvFolds]],targetCOlumn]
		XX <- Xtrain[folds[[cvFolds]],-targetCOlumn]
		pred <-predict(gbm1,XX,n.trees=ntrees)
  
    
		trainPredictions[folds[[cvFolds]],repeats] <- as.matrix(pred)

    
		currScore = sum(abs(pred - YY) * Xtrain[folds[[cvFolds]],weightColumn]) / sum(Xtrain[folds[[cvFolds]],weightColumn])
		print (currScore)  
		setScore = setScore + currScore/as.double(CVFolds)
    
    
    

		pred <-predict(gbm1,Xtest,n.trees=ntrees) 	
		testPredictions[,(repeats-1)*Repeats + cvFolds] = as.matrix(pred)
    
    

	 }
  
	 print("Set Score")
   print(setScore)

   finalScore =  finalScore + setScore/as.double(Repeats)
	 
}
	 
print("Final Score")
print(finalScore)	


filename <- paste("..\\predictions\\Target_Stack_", format(Sys.time(), '%Y%m%d%H%M%S'), "_", as.character(finalScore), "_", algorithm, ".csv", sep = "")
write.table(rowMeans(trainPredictions), file=filename, row.names = FALSE, col.names = FALSE) #, row.names = FALSE, col.names = FALSE

filename <- paste("..\\predictions\\Stack_", format(Sys.time(), '%Y%m%d%H%M%S'), "_", as.character(finalScore), "_", algorithm, ".csv", sep = "")
write.table(rowMeans(testPredictions), file=filename, row.names = FALSE, col.names = FALSE)   




cat(algorithm ,"\r\n", file = "..\\predictions\\RunLog.csv",sep="\r\n") 
cat("Features:", as.character(features) ,"\r\n", file = "..\\predictions\\RunLog.csv",sep="\r\n") 			
cat("CV:", as.character(CVFolds) ,"\r\n", file = "..\\predictions\\RunLog.csv",sep="\r\n") 	
cat("Repeats:", as.character(Repeats) ,"\r\n", file = "..\\predictions\\RunLog.csv",sep="\r\n")   
cat("Score:", as.character(finalScore) ,"\r\n", file = "..\\predictions\\RunLog.csv",sep="\r\n") 	
cat("DateTime:", format(Sys.time(), '%Y %m %d %H:%M:%S') ,"\r\n", file = "..\\predictions\\RunLog.csv",sep="\r\n") 				
cat("\r\n", file = "..\\predictions\\RunLog.csv",sep="\r\n") 


