#-*- coding: utf-8 -*-
import pandas,sqlite3,os,csv,gc
import numpy as np
from sklearn import linear_model
from sklearn import naive_bayes
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn.metrics import roc_curve, auc
##from sklearn import svm too slow...
import matplotlib.pyplot as plt
import pylab as pl

explanatoryVariables = ["avgRating", "wAvgRating", "nbReview", "nbHelpful", "salesrank", "catCust1", "catCust2" ,"catCust3" ,"catCust4" ,"catCust5" ,"catCust6" ,"catCust7" ,"catCust8" ,"catCust9" ,"catCust10" ,"catCust11" ,"catCust12" ,"catCust13" ,"catCust14"]
explanatoryVariables = ["avgRating", "wAvgRating", "nbReview", "salesrank", "catCust1", "catCust2" ,"catCust3" ,"catCust4" ,"catCust5" ,"catCust6" ,"catCust7" ,"catCust8" ,"catCust9" ,"catCust10" ,"catCust11" ,"catCust12" ,"catCust13" ,"catCust14"]
#amelioration : faire une PCA par exemple :-) avant la Logit
#separer la classe '1' en classes '4' et classes '5' -> pb : on ne pourrait plus faire de courbe ROC : il faudrait reagreger les resultats

from _3_ExtractProperInfo import finalSep
from _2_CleanDataBase import primaryCat

if __name__ == "__main__" :
	con = sqlite3.connect('../FinalDataBase.db3')
	#~ commandGen = """CREATE INDEX indDate ON DbSql(date);"""
	#~ con.execute(commandGen)
	#1998
	for year in [ i for i in range(1998,2004)] :
		#~ regr = linear_model.LinearRegression()
		#~ regrLasso = linear_model.Lasso(alpha = 10.,max_iter = 1e6,tol = 1e-3)
		randomForest = RandomForestClassifier(n_estimators = 30,n_jobs = 4)
		Logit = linear_model.LogisticRegression()
		#~ SVM =  svm.SVC(kernel='linear', probability=True)
		NaiveBayes = naive_bayes.MultinomialNB(alpha = 0.1)
		
		beginTrain = str(year)+"-01-01"
		endTrain = str(year+1)+"-12-31"
		beginTest = str(year+2)+"-01-01"
		endTest = str(year+2)+"-12-31"
		commandTrain = """SELECT * FROM DbSql where (date between date(\"%beginTrain%\") and date(\"%endTrain%\"))""".replace("%beginTrain%",beginTrain).replace("%endTrain%",endTrain)
		commandTest = """SELECT * FROM DbSql where (date between date(\"%beginTest%\") and date(\"%endTest%\"))""".replace("%beginTest%",beginTest).replace("%endTest%",endTest)
		print "Extract database"
		dfTrain = pandas.read_sql(commandTrain,con)
		dfTest = pandas.read_sql(commandTest,con)
		dfTrain["Apetance"] = (dfTrain["ratingReview"]/4).astype('int')
		dfTest["Apetance"] = (dfTest["ratingReview"]/4).astype('int')
		varPredicted = "Apetance"
		
		variablesKept = explanatoryVariables+[varPredicted]
		dfTrain.drop([name for name in dfTrain if name not in variablesKept], axis=1, inplace=True)
		dfTest.drop([name for name in dfTest if name not in variablesKept], axis=1, inplace=True)
		
		
		print "Training Models"
		#~ regr.fit(dfTrain.ix[:,explanatoryVariables],dfTrain["ratingReview"])
		randomForest.fit(dfTrain.ix[:,explanatoryVariables],dfTrain[varPredicted])
		#~ regrLasso.fit(dfTrain.ix[:,explanatoryVariables],dfTrain["ratingReview"])
		Logit.fit(dfTrain.ix[:,explanatoryVariables],dfTrain[varPredicted])
		NaiveBayes.fit(dfTrain.ix[:,explanatoryVariables],dfTrain[varPredicted])
		#~ SVM.fit(dfTrain.ix[:,explanatoryVariables],dfTrain[varPredicted])
		print "Predict Result"
		#~ predLin = regr.predict(dfTest.ix[:,explanatoryVariables])
		predRF = randomForest.predict(dfTest.ix[:,explanatoryVariables])
		predLogit = Logit.predict(dfTest.ix[:,explanatoryVariables])
		predNB = NaiveBayes.predict(dfTest.ix[:,explanatoryVariables])
		#~ predSVM = SVM.predict(dfTest.ix[:,explanatoryVariables])
		#~ predLasso = regrLasso.predict(dfTest.ix[:,explanatoryVariables])
		
		
		#~ print("Error linear model for %d : %f" % (year,np.sqrt(np.mean((predLin - dfTest[varPredicted])*(predLin - dfTest[varPredicted])))))
		#~ print("Error random forest for %d : %f" % (year,np.sqrt(np.mean((predRF - dfTest[varPredicted])*(predRF - dfTest[varPredicted])))))
		#~ print("Error Lasso for %d : %f" % (year,np.sqrt(np.mean((predLasso - dfTest[varPredicted])*(predLasso - dfTest[varPredicted])))))
		#~ predLin = predLin.astype('int')
		#~ predRF = predRF.astype('int')
		#~ predLogit = predLogit.astype('int')
		#~ predNB= predNB.astype('int')
		###predSVM = predSVM.astype('int') too slow
		#~ predLasso = predLasso.astype('int')
		
		#~ print pandas.crosstab(dfTest[varPredicted],predLin)
		#~ print pandas.crosstab(dfTest[varPredicted],predRF)
		#~ print pandas.crosstab(dfTest[varPredicted],predLogit)
		
		print "Computing the ROC Curve for %d" % year
		##ROC CURVE
		probas_RF = randomForest.predict_proba(dfTest.ix[:,explanatoryVariables])
		probas_Logit = Logit.predict_proba(dfTest.ix[:,explanatoryVariables])
		probas_NB= NaiveBayes.predict_proba(dfTest.ix[:,explanatoryVariables])
		#~ probas_SVM = SVM.predict_proba(dfTest.ix[:,explanatoryVariables])
		
		fprRF, tprRF, thresholdsRF = roc_curve(dfTest[varPredicted], probas_RF[:, 1])
		fprLogit, tprLogit, thresholdsLogit = roc_curve(dfTest[varPredicted], probas_Logit[:, 1])
		fprNB, tprNB, thresholdsNB = roc_curve(dfTest[varPredicted], probas_NB[:, 1])
		#~ fprSVM, tprSVM, thresholdsSVM = roc_curve(dfTest[varPredicted], probas_SVM[:, 1])
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
		pl.savefig("img/Roc_Curve_%d" % year,format = "pdf",figsize=(11.69,8.27)) 
		pl.close()
		
		del fprRF, tprRF, thresholdsRF
		del fprLogit, tprLogit, thresholdsLogit
		del fprNB, tprNB, thresholdsNB 
		del randomForest
		del Logit
		del NaiveBayes
		del predRF
		del predLogit
		del predNB
		del probas_RF
		del probas_Logit
		del probas_NB
		dfTrain.drop([name for name in dfTrain], axis=1, inplace=True)
		dfTest.drop([name for name in dfTest], axis=1, inplace=True)
		break
	con.close()
	