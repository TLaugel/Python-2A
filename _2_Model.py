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
	model.fit(train.ix[:,explanatoryVariables],train[varPredicted])
	pred = model.predict(test.ix[:,explanatoryVariables])
	predProbs = model.predict_proba(test.ix[:,explanatoryVariables])
	
	predbis = pred.copy()
	predbis[predbis == 2] = 1
	true = test[varPredicted].copy()
	true[true == 2] = 1
	cm2 = confusion_matrix(true, predbis)
	cm2 = confusion_matrix(test[varPredicted], pred)
	np.savetxt("confMat/"+name+".csv", cm2, delimiter=";")
	
	cmtrain = confusion_matrix(train[varPredicted], model.predict(dfTrain.ix[:,explanatoryVariables]))
	np.savetxt("confMat/"+name+"_train.csv", cmtrain, delimiter=";")
	
	#~ print(predProbs)
	pr, tpr, thresholds = roc_curve(true, predProbs[:, 1])
	#~ pr, tpr, thresholds = roc_curve(dfTest[varPredicted], predProbs[:, 1])
	return pred,pr, tpr, thresholds
	
	
if __name__ == "__main__" :
	con = sqlite3.connect('../ReviewsDB.db3')
	#1998
	year = 2000
	try :
		year = int(sys.argv[1])
	except :
		pass
	cases = 1
	try :
		cases = int(sys.argv[2])
	except :
		pass
	#~ for year in [ i for i in range(2001,2004)] :
	for year in range(year,year+1):
		beginTrain = str(year)+"-01-01"
		endTrain = str(year+1)+"-12-31"
		beginTest = str(year+2)+"-01-01"
		endTest = str(year+2)+"-12-31"
		commandTrain = """SELECT * FROM RevSql where (date between date(\"%beginTrain%\") and date(\"%endTrain%\"))""".replace("%beginTrain%",beginTrain).replace("%endTrain%",endTrain)
		commandTest = """SELECT * FROM RevSql where (date between date(\"%beginTest%\") and date(\"%endTest%\"))""".replace("%beginTest%",beginTest).replace("%endTest%",endTest)
		print("Extract database for %d" % year)
		dfTrain = pandas.read_sql(commandTrain,con)
		dfTrain.set_index(['idCust', 'idProd'])
		dfTest = pandas.read_sql(commandTest,con)
		dfTest.set_index(['idCust', 'idProd'])
		dummies = pandas.get_dummies(dfTrain['catProd'])
		#~ print(dfTrain.shape)
		#~ print(dfTest.shape)
		
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
		#~ print(aux.index)
		#~ print(type(aux.ix[1,index]))
		#~ types = dfTrain.apply(lambda x : pandas.lib.infer_dtype(x.values))
		#~ print(types[types == type(u'')])
		varMerge = [name for name in dfTrain if name not in varMerge]+['idCust']
		aux.reset_index(inplace = True)
		dfTrain = pandas.merge(dfTrain.ix[:,varMerge],aux,left_on = 'idCust',right_on =  'idCust', how = 'left')
		dfTest = pandas.merge(dfTest.ix[:,varMerge],aux,left_on = 'idCust',right_on = 'idCust', how = 'left')
		
		varMerge = ['ratingReview']
		aux = dfTrain.groupby(['idProd'])
		aux = aux[varMerge].count()
		aux.rename(columns = {'ratingReview':'nbReview'},inplace = True)
		aux.reset_index(inplace = True)
		dfTrain = pandas.merge(dfTrain,aux,left_on = 'idProd',right_on = 'idProd', how = 'left')
		dfTest = pandas.merge(dfTest,aux,left_on = 'idProd',right_on = 'idProd', how = 'left')
		
		varMerge = ['ratingReview']
		aux = dfTrain.groupby(['idProd'])
		aux = aux[varMerge].mean()
		aux.rename(columns = {'ratingReview':'avgRating'},inplace = True)
		aux.reset_index(inplace = True)
		dfTrain = pandas.merge(dfTrain,aux,left_on = 'idProd',right_on = 'idProd', how = 'left')
		dfTest = pandas.merge(dfTest,aux,left_on = 'idProd',right_on = 'idProd', how = 'left')
		
		dfTestInfo = dfTest.copy()
		for var in selectedDummies :
			dfTest.ix[dfTest[var].isnull(),var] = 0
			dfTestInfo = dfTestInfo[dfTestInfo[var].notnull()]
		dfTest.ix[dfTest['nbReview'].isnull(),'nbReview'] = 0
		dfTestInfo = dfTestInfo[dfTestInfo['nbReview'].notnull()] 
		dfTest.ix[dfTest['avgRating'].isnull(),['avgRating']] = np.mean(dfTrain['ratingReview'])
		dfTestInfo = dfTestInfo.ix[dfTestInfo['avgRating'].notnull(),:] 
		
		aux.drop([name for name in aux], axis=1, inplace=True)
		del(aux,varMerge)
		print("info sur la taille des bases pour %d" %year)
		print(dfTrain.shape)
		print(dfTestInfo.shape)
		print(dfTest.shape)
		
		print("info sur les nb de produits pour %d"%year)
		print(len(pandas.Series(dfTrain["idProd"].values.ravel()).unique()))
		print(len(pandas.Series(dfTestInfo['idProd'].values.ravel()).unique()))
		print(len(pandas.Series(dfTest['idProd'].values.ravel()).unique()))		
		
		print("info sur les nb de customer pour %d"%year)
		print(len(pandas.Series(dfTrain['idCust'].values.ravel()).unique()))
		print(len(pandas.Series(dfTestInfo['idCust'].values.ravel()).unique()))
		print(len(pandas.Series(dfTest['idCust'].values.ravel()).unique()))
		
		print dfTrain.ix[dfTrain['idCust'] == 'AYPCUQS6ARWFH',:]
		break
		aux = dfTrain.groupby(["ratingReview"])
		aux = aux['avgRating'].count()
		print(aux)

		dfTrain.ix[dfTrain["ratingReview"] <= 3,["ratingReview"]] = 0
		dfTrain.ix[dfTrain["ratingReview"] == 4,["ratingReview"]] = 1
		dfTrain.ix[dfTrain["ratingReview"] == 5,["ratingReview"]] = cases
		dfTest.ix[dfTest["ratingReview"] <= 3,"ratingReview"] = 0		
		dfTest.ix[dfTest["ratingReview"] == 4,"ratingReview"] = 1
		dfTest.ix[dfTest["ratingReview"] == 5,"ratingReview"] = cases
		dfTestInfo.ix[dfTestInfo["ratingReview"] <= 3,"ratingReview"] = 0		
		dfTestInfo.ix[dfTestInfo["ratingReview"] == 4,"ratingReview"] = 1
		dfTestInfo.ix[dfTestInfo["ratingReview"] == 5,"ratingReview"] = cases
		dfTrain["ratingReview"].astype('int')
		dfTest["ratingReview"].astype('int')
		dfTestInfo["ratingReview"].astype('int')
		#~ cases = max(dfTrain["ratingReview"])
		
		varPredicted = "ratingReview"
		explanatoryVariables = [x for x in selectedDummies]+['nbReview','catProd','avgRating']
		
		variablesKept = explanatoryVariables +[varPredicted]
		dfTrain.drop([name for name in dfTrain if name not in variablesKept], axis=1, inplace=True)
		dfTest.drop([name for name in dfTest if name not in variablesKept], axis=1, inplace=True)
		dfTestInfo.drop([name for name in dfTest if name not in variablesKept], axis=1, inplace=True)

		#~ randomForest = RandomForestClassifier(n_estimators = 30,n_jobs = 4)
		#~ Logit = linear_model.LogisticRegression()
		#~ NaiveBayes = naive_bayes.MultinomialNB(alpha = 0.1)
		#~ print("Random Forest")
		#~ predRF,fprRF, tprRF, thresholdsRF = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTest,randomForest,'RF_%d_%d' % (year,cases)) 
		#~ print("Naive Bayes")
		#~ predLogit,fprLogit, tprLogit, thresholdsLogit = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTest,Logit,'Logit_%d_%d' % (year,cases)) 
		#~ print("Logit")
		#~ predNB,fprNB, tprNB, thresholdsNB = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTest,NaiveBayes,'NB_%d_%d' % (year,cases)) 		
		#~ roc_aucRF = auc(fprRF, tprRF)
		#~ roc_aucLogit = auc(fprLogit, tprLogit)
		#~ roc_aucNB = auc(fprNB, tprNB)
		#~ print("Area under the ROC curve (RF) : %f" % roc_aucRF)
		#~ print("Area under the ROC curve (Logit) : %f" % roc_aucLogit)
		#~ print("Area under the ROC curve (NaiveBayes) : %f" % roc_aucNB)
		#~ pl.clf()
		#~ pl.plot(fprRF, tprRF, label='ROC curve RF (area = %0.2f)' % roc_aucRF)
		#~ pl.plot(fprLogit, tprLogit, label='ROC curve Logit (area = %0.2f)' % roc_aucLogit)
		#~ pl.plot(fprNB, tprNB, label='ROC curve NaiveBayes (area = %0.2f)' % roc_aucNB)
		#~ pl.plot([0, 1], [0, 1], 'k--')
		#~ pl.xlim([0.0, 1.0])
		#~ pl.ylim([0.0, 1.0])
		#~ pl.xlabel('False Positive Rate')
		#~ pl.ylabel('True Positive Rate')
		#~ pl.title('Receiver operating characteristic example for %d' % year)
		#~ pl.legend(loc="lower right")
		#~ pl.savefig("img/Roc_Curve_%d_%d.pdf" % (year,cases),format = "pdf",figsize=(11.69,8.27)) 
		#~ pl.close()

		randomForest = RandomForestClassifier(n_estimators = 30,n_jobs = 4)
		Logit = linear_model.LogisticRegression()
		NaiveBayes = naive_bayes.MultinomialNB(alpha = 0.1)
		print("Random Forest")
		predRF,fprRF, tprRF, thresholdsRF = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTestInfo,randomForest,'RF_%d_%d_info' % (year,cases)) 
		print("Naive Bayes")
		predLogit,fprLogit, tprLogit, thresholdsLogit = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTestInfo,Logit,'Logit_%d_%d_info' % (year,cases)) 
		print("Logit")
		predNB,fprNB, tprNB, thresholdsNB = constructmodel(explanatoryVariables,varPredicted,dfTrain,dfTestInfo,NaiveBayes,'NB_%d_%d_info' % (year,cases)) 	
		roc_aucRF = auc(fprRF, tprRF)
		roc_aucLogit = auc(fprLogit, tprLogit)
		roc_aucNB = auc(fprNB, tprNB)
		print("Area under the ROC curve (RF) : %f" % roc_aucRF)
		print("Area under the ROC curve (Logit) : %f" % roc_aucLogit)
		print("Area under the ROC curve (NaiveBayes) : %f" % roc_aucNB)
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
		
		
		print(dfTestInfo[varPredicted].shape)
		print(len(predRF))
		selectCust = dfTestInfo.ix[predRF==dfTestInfo[varPredicted],:]
		#~ print selectCust
		#~ print dfTrain.ix[dfTrain['idCust'] == selectCust['idCust'],:]
		
		pl.clf()
		pl.plot(fprRF, tprRF, label='ROC curve RF (area = %0.2f)' % roc_aucRF)
		pl.plot([0, 1], [0, 1], 'k--')
		pl.xlim([0.0, 1.0])
		pl.ylim([0.0, 1.0])
		pl.xlabel('False Positive Rate')
		pl.ylabel('True Positive Rate')
		pl.title('Receiver operating characteristic example for %d' % year)
		pl.legend(loc="lower right")
		pl.savefig("img/Roc_Curve_%d_%d_info_RFOnly.pdf" % (year,cases),format = "pdf",figsize=(11.69,8.27)) 
		pl.close()
		
		
		np.savetxt("confMat/fpr_%d.csv" %year,np.array(fprRF),delimiter = ',')
		np.savetxt("confMat/tpr_%d.csv" %year,np.array(tprRF),delimiter = ',')
		
		del fprRF, tprRF, thresholdsRF
		del fprLogit, tprLogit, thresholdsLogit
		del fprNB, tprNB, thresholdsNB 
		del randomForest,Logit,NaiveBayes
		del predRF,predLogit,predNB
		dfTrain.drop([name for name in dfTrain], axis=1, inplace=True)
		dfTest.drop([name for name in dfTest], axis=1, inplace=True)
		dfTestInfo.drop([name for name in dfTest], axis=1, inplace=True)
		del dfTrain,dfTest,dfTestInfo
		print("end for year %d \n" % year)
		gc.collect()
		#~ break
	con.close()
	