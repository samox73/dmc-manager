import pymongo


class store:
    # the scheme of the url is: PROTOCOL://USER:PW@HOST
    def __init__(self, url="mongodb://root:test@localhost", collection_name="store"):
        self.client = pymongo.MongoClient(url)
        self.selfenergydb = self.client["selfenergy"]
        self.collection = self.selfenergydb[collection_name]

    def add(self, object):
        self.collection.insert_one(object)
