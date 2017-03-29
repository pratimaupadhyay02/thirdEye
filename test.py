from finalmodel import PredictRevenue
from cnnCars import CarsCount
from cnnHouse  import HouseCount

threshold  =300 
'''cars_count = CarsCount(1,21) 
house_count = HouseCount(2,15)
if house_count.return_House_Count()>threshold:
	city_group = 'Big Cities'
else:
	city_group = 'Others'
'''
var = PredictRevenue('MB', '02/21/1999', 'Trabzon', '2', 21, 'Others')

print str(var.revenue())# +' no. of cars ' + str(cars_count.CarCountsVal())+ ' no. of houses '+str(house_count.return_House_Count())

