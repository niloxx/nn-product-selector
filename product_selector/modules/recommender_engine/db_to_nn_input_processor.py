import logging
from itertools import islice
from ..settings_loader import SettingsLoader
from ..dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler
from ..dataset_processing.src.mapper.dbmapper import DBMapper
from ..dataset_processing.src.model.mappeduser import MappedUser
from ..dataset_processing.src.model.mappedproduct import MappedProduct
from ..keras_learning.io.nninputset import NNInputSet

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DBToNNInputProcesor(object):
    """"""
    MAX_NN_INPUT_SET_SIZE = SettingsLoader.getValue("MAX_NN_INPUT_SIZE")

    @staticmethod
    def generateNNInputSet(mUser, productCursor, maxSize=MAX_NN_INPUT_SET_SIZE):
        nnInputSet = NNInputSet()
        sentinel = object() # Guard for exhausted generator
        for i in range(0, maxSize):
            dbProduct = next(productCursor, sentinel)
            if dbProduct is sentinel:
                break
            product = DBMapper.fromDBResultToMappedProduct(dbProduct)
            if product and product.hasCategory():
                nnInputSet.add(mUser, product)
        return nnInputSet