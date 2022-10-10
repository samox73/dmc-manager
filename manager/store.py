import pymongo
import gridfs


class store:
    # the scheme of the url is: PROTOCOL://USER:PW@HOST
    def __init__(self, url="mongodb://root:test@localhost", collection_name="store"):
        self.client = pymongo.MongoClient(url)
        self.selfenergydb = self.client["selfenergy"]
        self.collection = self.selfenergydb[collection_name]
        self.gridfs = gridfs.GridFS(self.selfenergydb, collection=collection_name)
        # self.gridfs.put(tset, filename=)
