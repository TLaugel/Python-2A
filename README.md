Python-2A
=========

The name of the scripts start with numbers : first we need to execute _1_* then _2_* etc.
Everything should work smoothly, except maybe for the creation of the .db3 file.

Concerning the modeling part :
-3 models have been implemented : Naive Bayes, Logit and Random Forest
-For each, the ROC curve has been computed in the img/ folder

For its improvement :
-Compute a PCA before doing the models : to avoid the correlation probably to high (maybe)
-When computing the models : try to do 3 classes : rating 1-2-3; rating 4 and rating 5, then reagregate it before the computation of the ROC curve. The underlying idea is trying to equilibrate the classes.
