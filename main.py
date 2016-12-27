#!/usr/bin/python2.7
from dataset_processing.modules.src.io.mongoconnector.mongohandler import MongoHandler
from dataset_processing.modules.src.model.product import Product
from dataset_processing.modules.src.model.user import User
from dataset_processing.modules.src.model.mappeduser import MappedUser
from dataset_processing.modules.src.model.mappedproduct import MappedProduct
from keras_learning.nn import NN, NNInput, NNOutput
from datetime import date, datetime
from random import randint

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

dMAX = 20

def getUsersFromDBResult(db_users):
	""" Receives the dictionary result of the query against
	 	the DB and returns an array of mapped User objects
	"""
	logger.info('Processing users from data base results')
	retrievedUsers = []
	i = 0
	for db_user in db_users:
		if (i == dMAX):
			break
		# Retrieve username, gender, age and nationality
		username = db_user['login']['username']
		gender = db_user['gender']
		dateOfBirth = db_user['dob'] #yyyy-mm-dd
		nationality = db_user['nat']
		# Transform string date to date object
		dateOfBirth = datetime.strptime(dateOfBirth.split(' ')[0], '%Y-%m-%d')
		#logger.debug("{};{};{};{}".format(username, gender, dateOfBirth.year, nationality))
		user = User(username, gender, dateOfBirth, nationality)
		retrievedUsers.append(user)
		i+=1
	logger.info('Users processed')

	return retrievedUsers

def getProductsFromDBResult(db_products):
	""" Receives the dictionary result of the query against
	 	the DB and returns an array of mapped Product objects
	"""
	logger.info('Processing products from data base results')
	retrievedProducts = []
	i = 0
	for db_product in db_products:
		if (i == dMAX):
			break
		idP = db_product['_id']
		name = db_product['name']
		categories = db_product['sections']
		imageUrl = db_product['image_url']
		if (categories):
			product = Product(idP, name, categories, imageUrl)
			retrievedProducts.append(product)
		i+=1

		#logger.debug("{};{};{}".format(product._id, product._name, product._mainCategory))


	logger.info('Products processed')
	return retrievedProducts

if __name__ == '__main__':
	logger.info('Executing Neural Input Generator')

	logger.info('Loading Neural Network')
	network = NN.getInstance()

	logger.info('Establishing connection with DB')
	mongoHandler = MongoHandler()
	logger.info('Retrieving users from DB')
	db_users = mongoHandler.getUsersFromDB()
	users = getUsersFromDBResult(db_users)
	mappedUsers = []
	logger.info('Mapping users')
	for user in users:
		mUser = MappedUser(user)
		mappedUsers.append(mUser)
		logger.debug("Gender={};Nationality={};Age={}".format(user._gender, user._nationality, user._age))
		logger.debug("\033[32mGenderM={};NationalityM={};AgeM={}\033[0m".format(mUser._gender, mUser._nationality, mUser._age))
	logger.info('Users mapped')

	logger.info('Retrieving products from DB')
	db_products = mongoHandler.getProductsFromDB()
	products = getProductsFromDBResult(db_products)
	mappedProducts = []

	logger.info('Mapping products')
	for product in products:
		#logger.debug("{} --> {}".format(product._mainCategory, MappedProduct(product)._mainCategory))
		mProduct = MappedProduct(product)
		mProduct._avgRating = float(randint(0,5))
		mappedProducts.append(mProduct)
		logger.debug("Main Category={};Avg Rating={};No. Purchases={}".format(product._mainCategory, product._avgRating, product._noPurchases))
		logger.debug("\033[32mMain CategoryM={};Avg RatingM={};No. PurchasesM={}\033[0m".format(mProduct._mainCategory, mProduct._avgRating, mProduct._noPurchases))
	logger.info('Products mapped')

	
	logger.info('zipping lists')
	mapped_user_product_list = zip(mappedUsers, mappedProducts)
	logger.info('Creating NNInput list')
	inputSet = NNInput.getNNInputList(mapped_user_product_list)
	logger.info('Getting predictions')
	predictions = network.predict(inputSet)
	i = 0
	for user, product in mapped_user_product_list:
		logger.debug("User: Nationality={};Gender={};Age={} Product: Category={};Avg Rating={}".format(user._nationality, user._gender, user._age, product._mainCategory, product._avgRating))
		logger.info("\033[32m Like: %.6f%%\033[0m" % (NNOutput.translatePredictionToDecimal(predictions[i]) * 100))
		i = i + 1



