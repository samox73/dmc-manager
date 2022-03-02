import pymongo


class store:
    client = pymongo.MongoClient("mongodb://root:test@localhost")
    selfenergydb = client["selfenergy"]
    collection = selfenergydb["store"]

    def add(self, run_properties, fft, checkpoints={}):
        self.collection.insert_one({
            "run_properties": run_properties,
            "fft": fft,
            # "checkpoints": checkpoints
        })
