#-*- coding: utf-8 -*-
import pandas,sqlite3,os,csv,gc
import numpy as np
from sklearn import linear_model
from sklearn import naive_bayes
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn.metrics import roc_curve, auc,confusion_matrix
##from sklearn import svm too slow...
import matplotlib.pyplot as plt
import pylab as pl
import sys

#amelioration : faire une PCA par exemple :-) avant la Logit
#separer la classe '1' en classes '4' et classes '5' -> pb : on ne pourrait plus faire de courbe ROC : il faudrait reagreger les resultats


def constructmodel(explanatoryVariables,varPredicted,train,test,model,name) :
	model.fit(dfTrain.ix[:,explanatoryVariables],dfTrain[varPredicted])
	pred = model.predict(dfTest.ix[:,explanatoryVariables])
	predProbs = model.predict_proba(dfTest.ix[:,explanatoryVariables])
	
	predbis = pred.copy()
	predbis[predbis == 2] = 1
	true = dfTest[varPredicted].copy()
	true[true == 2] = 1
	cm2 = confusion_matrix(true, predbis)
	cm2 = confusion_matrix(dfTest[varPredicted], pred)
	#~ print type(cm2)
	np.savetxt("confMat/"+name+".csv", cm2, delimiter=";")
	
	pr, tpr, thresholds = roc_curve(true, predProbs[:, 1])
	#~ pr, tpr, thresholds = roc_curve(dfTest[varPredicted], predProbs[:, 1])
	return pred,pr, tpr, thresholds
	
	
if __name__ == "__main__" :
	con = sqlite3.connect('../ReviewsDB.db3')
	#1998
	year = int(sys.argv[1])
	cases = int(sys.argv[2])
	#~ for year in [ i for i in range(2001,2004)] :
	for year in range(year,year+1):
		beginTrain = str(year)+"-01-01"
		endTrain = str(year+1)+"-12-31"
		beginTest = str(year+2)+"-01-01"
		endTest = str(year+2)+"-12-31"
		commandTrain = """SELECT * FROM RevSql where (date between date(\"%beginTrain%\") and date(\"%endTrain%\"))""".replace("%beginTrain%",beginTrain).replace("%endTrain%",endTrain)
		commandTest = """SELECT * FROM RevSql where (date between date(\"%beginTest%\") and date(\"%endTest%\"))""".replace("%beginTest%",beginTest).replace("%endTest%",endTest)
		print "Extract database for %d" % year
		dfTrain = pandas.read_sql(commandTrain,con)
		dfTrain.set_index(['idCust', 'idProd'])
		dfTest = pandas.read_sql(commandTest,con)
		dfTest.set_index(['idCust', 'idProd'])
		dummies = pandas.get_dummies(dfTrain['catProd'])
		#~ print dfTrain.shape
		#~ print dfTest.shape
		
		selectedDummies = [name for name in dummies] 
		for name in selectedDummies:
			dfTrain[name] = dummies[name]
		del dummies
		dummies = pandas.get_dummies(dfTest['catProd'])
		for name in selectedDummies :
			try :
				dfTest[name] = dummies[name]
			except :
				dfTest[name] = 0
		
		varMerge = selectedDummies+['idCust']
		aux = dfTrain.groupby(['idCust'])
		aux =  aux[varMerge].mean()		
		varMerge = [name for name in dfTrain if name not in varMerge]+['idCust']
		dfTrain = pandas.merge(dfTrain.ix[:,varMerge],aux,left_on = 'idCust',right_on =  aux.index, how = 'left')
		dfTest = pandas.merge(dfTest.ix[:,varMerge],aux,left_on = 'idCust',right_on = aux.index, how = 'left')
		
		varMerge = ['ratingReview']
		aux = dfTrain.groupby(['idProd'])
		aux = aux[varMerge].count()
		aux.rename(columns = {'ratingReview':'nbReview'},inplace = True)
		dfTrain = pandas.merge(dfTrain,aux,left_on = 'idProd',right_on = aux.index, how = 'left')
		dfTest = pandas.merge(dfTest,aux,left_on = 'idProd',right_on = aux.index, how = 'left')
		
		varMerge = ['ratingReview']
		aux = dfTrain.groupby(['idProd'])
		aux = aux[varMerge].mean()
		aux.rename(columns = {'ratingReview':'avgRating'},inplace = True)
		dfTrain = pandas.merge(dfTrain,aux,left_on = 'idProd',right_on = aux.index, how = 'left')
		dfTest = pandas.merge(dfTest,aux,left_on = 'idProd',right_on = aux.index, how = 'left')
		
		dfTestInfo = dfTest.copy()
		for var in selectedDummies :
			dfTest[var][dfTest[var].isnull()] = 0
			dfTestInfo = dfTestInfo[dfTestInfo[var].notnull()]
		dfTest['nbReview'][dfTest['nbReview'].isnull()] = 0
		dfTestInfo = dfTestInfo[dfTestInfo['nbReview'].notnull()] 
		dfTest['avgRating'][dfTest['avgRating'].isnull()] = np.mean(dfTrain['ratingReview'])
		dfTestInfo = dfTestInfo[dfTestInfo['avgRating'].notnull()] 
		
		aux.drop([name for name in aux], axis=1, inplace=True)
		del aux,varMerge
		#~ print dfTrain.shape
		print dfTestInfo.shape
		print dfTest.shape
		#~ break

		dfTrain["ratingReview"][dfTrain["ratingReview"] <= 3] = 0
		dfTrain["ratingReview"][dfTrain["ratingReview"] == 4] = 1
		dfTrain["ratingReview"][dfTrain["ratingReview"] == 5] = cases
		dfTest["ratingReview"][dfTest["ratingReview"] <= 3] = 0		
		dfTest["ratingReview"][dfTest["ratingReview"] == 4] = 1
		dfTest["ratingReview"][dfTest["ratingReview"] == 5] = cases
		dfTrain["ratingReview"].astype('int')
		dfTest["ratingReview"].astype('int')
		#~ cases = max(dfTrain["ratingReview"])
		
		varPredicted = "ratingReview"
		explanatoryVariables = [x for x in selectedDummies]+['nbReview','catProd','avgRating']
		
		variablesKept = explanatoryVariables +[varPredicted]
		dfTrain.drop([name for name in dfTrain if name not in variablesKept], axis=1, inplace=True)
		dfTest.drop([name for name in dfTest if name not in variablesKept], axis=1, inplace=True)
		

		randomForest = RandomForestClassifier(n_estimators = 30,n_jobs = 4)
		Logit = linear_model.LogisticRegression()
		NaiveBayes = naive_bayes.MultinomialNB(alpha = 0.1)
		print "Random Forest"
		predRF,fprRF, tprRF, thresholdsRF = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTest,randomForest,'RF_%d_%d' % (year,cases)) 
		print "Naive Bayes"
		predLogit,fprLogit, tprLogit, thresholdsLogit = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTest,Logit,'Logit_%d_%d' % (year,cases)) 
		print "Logit"
		predNB,fprNB, tprNB, thresholdsNB = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTest,NaiveBayes,'NB_%d_%d' % (year,cases)) 		
		roc_aucRF = auc(fprRF, tprRF)
		roc_aucLogit = auc(fprLogit, tprLogit)
		roc_aucNB = auc(fprNB, tprNB)
		#~ roc_aucSVM = auc(fprSVM, tprSVM)
		print "Area under the ROC curve (RF) : %f" % roc_aucRF
		print "Area under the ROC curve (Logit) : %f" % roc_aucLogit
		print "Area under the ROC curve (NaiveBayes) : %f" % roc_aucNB
		#~ print "Area under the ROC curve (Logit) : %f" % roc_aucSVM
		pl.clf()
		pl.plot(fprRF, tprRF, label='ROC curve RF (area = %0.2f)' % roc_aucRF)
		pl.plot(fprLogit, tprLogit, label='ROC curve Logit (area = %0.2f)' % roc_aucLogit)
		pl.plot(fprNB, tprNB, label='ROC curve NaiveBayes (area = %0.2f)' % roc_aucNB)
		#~ pl.plot(fprSVM, tprSVM, label='ROC curve Logit (area = %0.2f)' % roc_aucSVM)
		pl.plot([0, 1], [0, 1], 'k--')
		pl.xlim([0.0, 1.0])
		pl.ylim([0.0, 1.0])
		pl.xlabel('False Positive Rate')
		pl.ylabel('True Positive Rate')
		pl.title('Receiver operating characteristic example for %d' % year)
		pl.legend(loc="lower right")
		pl.savefig("img/Roc_Curve_%d_%d.pdf" % (year,cases),format = "pdf",figsize=(11.69,8.27)) 
		pl.close()

		randomForest = RandomForestClassifier(n_estimators = 30,n_jobs = 4)
		Logit = linear_model.LogisticRegression()
		NaiveBayes = naive_bayes.MultinomialNB(alpha = 0.1)
		print "Random Forest"
		predRF,fprRF, tprRF, thresholdsRF = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTestInfo,randomForest,'RF_%d_%d_info' % (year,cases)) 
		print "Naive Bayes"
		predLogit,fprLogit, tprLogit, thresholdsLogit = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTestInfo,Logit,'Logit_%d_%d_info' % (year,cases)) 
		print "Logit"
		predNB,fprNB, tprNB, thresholdsNB = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTestInfo,NaiveBayes,'NB_%d_%d_info' % (year,cases)) 	
		roc_aucRF = auc(fprRF, tprRF)
		roc_aucLogit = auc(fprLogit, tprLogit)
		roc_aucNB = auc(fprNB, tprNB)
		#~ roc_aucSVM = auc(fprSVM, tprSVM)
		print "Area under the ROC curve (RF) : %f" % roc_aucRF
		print "Area under the ROC curve (Logit) : %f" % roc_aucLogit
		print "Area under the ROC curve (NaiveBayes) : %f" % roc_aucNB
		pl.clf()
		pl.plot(fprRF, tprRF, label='ROC curve RF (area = %0.2f)' % roc_aucRF)
		pl.plot(fprLogit, tprLogit, label='ROC curve Logit (area = %0.2f)' % roc_aucLogit)
		pl.plot(fprNB, tprNB, label='ROC curve NaiveBayes (area = %0.2f)' % roc_aucNB)
		pl.plot([0, 1], [0, 1], 'k--')
		pl.xlim([0.0, 1.0])
		pl.ylim([0.0, 1.0])
		pl.xlabel('False Positive Rate')
		pl.ylabel('True Positive Rate')
		pl.title('Receiver operating characteristic example for %d' % year)
		pl.legend(loc="lower right")
		pl.savefig("img/Roc_Curve_%d_%d_info.pdf" % (year,cases),format = "pdf",figsize=(11.69,8.27)) 
		pl.close()
		
		del fprRF, tprRF, thresholdsRF
		del fprLogit, tprLogit, thresholdsLogit
		del fprNB, tprNB, thresholdsNB 
		del randomForest,Logit,NaiveBayes
		del predRF,predLogit,predNB
		dfTrain.drop([name for name in dfTrain], axis=1, inplace=True)
		dfTest.drop([name for name in dfTest], axis=1, inplace=True)
		dfTestInfo.drop([name for name in dfTest], axis=1, inplace=True)
		del dfTrain,dfTest,dfTestInfo
		gc.collect()
		#~ break
	con.close()
	