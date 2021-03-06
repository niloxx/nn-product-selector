import time
from .product_selector.modules.dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler

if __name__ == '__main__':
    handler = MongoHandler.getInstance()
    productBefore = handler._productDB.products_collection.find_one()
    print(productBefore)
    print(handler._productDB.products_collection.find().count())
    print("#################################################")
    print(handler._userDB.users_collection.find_one())
    print(handler._userDB.users_collection.find().count())
    print("#################################################")
    print(handler._analysisDB.rules_collection_mock.find_one())
    print(handler._analysisDB.rules_collection_mock.find().count())
    print("--------------------------------------------------")
    print(handler._analysisDB.ratings_collection_mock.find_one())
    print(handler._analysisDB.ratings_collection_mock.find().count())
    print("#########################################################")
    print("#########################################################")
    print(handler._analysisDB.predictions_collection.find_one())
    print("#########################################################")
    print("#########################################################")
    pipeline = [
        {"$group":
            {
            "_id": {"user": "$_userId", "product": "$_productId"},
            "totalSum": {"$sum": "$_productRating"},
            "avgSum": {"$avg": "$_productRating"},
            "count": {"$sum": 1}
            }
        }
    ]
    ini = time.time()
    i = 0
    for product_rating in handler._analysisDB.ratings_collection_mock.aggregate(pipeline):
        _id = product_rating['_id']['product']
        username = product_rating['_id']['user']
        avgSum = product_rating['avgSum']
        handler._productDB.products_collection.find_one({"_id": _id})
        handler._userDB.users_collection.find_one({"login.username": username})
        handler._productDB.products_collection.update_one({
          '_id': _id
        },{
          '$set': {
            'rate': avgSum
          }
        }, upsert=False)
        i += 1
        if(i%1000==0):
            print(i)
    fini = time.time()
    print(i)
    print(fini - ini)
    #ini = time.time()
    #db_ratings = MongoHandler.getInstance().getRatingsForProduct(product._id)
    #product.setRating([db_rating['_rating'] for db_rating in db_ratings])
    #fini = time.time()
    #print(fini - ini)
    print(handler._productDB.products_collection.find_one())
    print(handler._productDB.products_collection.find_one()['rate'])
