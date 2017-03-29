
import cPickle
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.feature_extraction import DictVectorizer
from datetime import datetime
import csv

class PredictRevenue:
	def __init__(self,restraunt_type, Opening_date, country, Parking_space, AreaCode, city_group):
		global test_revenue
		
		Opening_date = str(Opening_date)
		reader = csv.reader(open('train.csv', 'rb'))
		writer = csv.writer(open('appended_output.csv', 'wb'))
		for row in reader:

			if row[0]==str(AreaCode):# or row[0]=='Id':
				print row
				
				row[1] =  Opening_date  #'02/21/1999'
				row[2] =  country
				row[3] = city_group
				row[4] = restraunt_type
				row[5] = '7'
				row[6] = '8'
				
			writer.writerow(row)

		train = pd.read_csv('train.csv')
		test = pd.read_csv('appended_output.csv')
		 
		vec = DictVectorizer()


		def diff_dates_2017(date_x):
		  date_format = "%m/%d/%Y"
		  x = datetime.strptime(date_x, date_format)
		  y = datetime.strptime('01/01/2017', date_format)
		  delta = y - x
		  return delta.days

		train['Open Date'] = train['Open Date'].apply(lambda x: diff_dates_2017(x))
		test['Open Date'] = test['Open Date'].apply(lambda x: diff_dates_2017(x))
		#test['Open Date'] = 
		#Extract Features.to
		
		train_new = vec.fit_transform(train[['City','City Group','Type']].T.to_dict().values()).todense()
		test_new = vec.transform(test[['City','City Group','Type']].T.to_dict().values()).todense()

		print test_new[AreaCode]
		train_new = train_new

		p = ['P' + str(i) for i in range(1,38)]
		test_p = test[p]

		#adding new columns to train_p
		test = np.hstack((test_new,test_p))

		#Setup Random Forest

		with open('model', 'rb') as f:
			clf = cPickle.load(f)

		#print clf.feature_importances_
		test_revenue = clf.predict(test)
		test_revenue = test_revenue[AreaCode]
		#print test_revenue		

	def revenue(slef):
			return test_revenue
		