import pymongo


class store:
    client = pymongo.MongoClient("mongodb://root:test@localhost")
    selfenergydb = client["selfenergy"]
    collection = selfenergydb["store"]

    def add(self, object):
        self.collection.insert_one(object)
