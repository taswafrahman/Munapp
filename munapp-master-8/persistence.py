
#persistence module
#methods using pickle, when called implements binary protocols for serializing and deserializing python objecs


import pickle

def backup(object1, fileN):
    with open(fileN, 'wb') as outfile:
        pickle.dump(object1, outfile, pickle.HIGHEST_PROTOCOL)

    return (object1)

def load(fileN):
    with open(fileN, 'rb') as infile:
        new1 = pickle.load(infile)
    return (new1)