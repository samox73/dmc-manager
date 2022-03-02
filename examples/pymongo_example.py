import pymongo

client = pymongo.MongoClient("mongodb://root:test@localhost")

selfenergydb = client["selfenergy"]

pvse = selfenergydb["p_vs_e"]
# pvse.drop()

x = pvse.insert_one({
    "properties": {
        "alpha": 1,
        "max_tau": 20
    },
    "fft": {
        "taus": [0, 0.2, 0.4],
        "g_t": [1, 0.5, 0.25]
    }
})

x = pvse.find_one({
    "properties.alpha": 1
})

print(x["fft"])
