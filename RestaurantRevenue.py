import cPickle
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.feature_extraction import DictVectorizer
from datetime import datetime
#Load training data
class PredictRevenue:
	def __init__(self,Type, Date, ZipCode, COuntry, ParkingSpace):
	

	train = pd.read_csv('train.csv')
	test = pd.read_csv('test.csv')
	 
	vec = DictVectorizer()


	def diff_dates_2015(date_x):
	  date_format = "%m/%d/%Y"
	  x = datetime.strptime(date_x, date_format)
	  y = datetime.strptime('01/01/2015', date_format)
	  delta = y - x
	  return delta.days

	train['Open Date'] = train['Open Date'].apply(lambda x: diff_dates_2015(x))
	test['Open Date'] = test['Open Date'].apply(lambda x: diff_dates_2015(x))

	#Extract Features.to
	train_new = vec.fit_transform(train[['City','City Group','Type']].T.to_dict().values()).todense()
	test_new = vec.transform(test[['City','City Group','Type']].T.to_dict().values()).todense()

	print train_new
	print test_new

	target = train['revenue']
	train = train.drop('revenue',axis=1)

	p = ['P' + str(i) for i in range(1,38)]
	train_p = train[p]
	test_p = test[p]

	#adding new columns to train_p
	train = np.hstack((train_new,train_p))
	test = np.hstack((test_new,test_p))

	#Setup Random Forest
	clf = RandomForestRegressor(n_estimators=200)
	clf.fit(train,target)

	with open('model', 'wb') as f:
	    cPickle.dump(clf, f)

	print clf.feature_importances_
	test_revenue = clf.predict(test)
	print 'test_revenue' + str(test_revenue)
	sub = pd.read_csv('ssub.csv')
	sub['Prediction'] = test_revenue
	sub.to_csv('RandomForest.csv', index = False)


'''
A random forest is a meta estimator that fits a number of decision tree classifiers on various sub-samples of the dataset and use averaging to improve the predictive accuracy and control over-fitting. The sub-sample size is always the same as the original input sample size but the samples are drawn with replacement if bootstrap=True (default
'''