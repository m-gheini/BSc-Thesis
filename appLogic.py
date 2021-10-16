import os

countriesSectorsDict = {}


def getResultFileAttr(name, path):
    print("1")
    if not os.path.exists(path):
        os.makedirs(path)
    print("2")
    name = name + '.CSV'
    print("3")
    print(os.path.join(path, name))
    print("4")


def getFirstRow(file):
    for line in open(file, "r"):
        return line.split()


def getCountriesAndSectors(file):
    allElements = getFirstRow(file)
    allElements = allElements[0].split(",")
    # print(all)
    for elem in allElements[1:]:
        elem = elem[1:-1]
        divided = elem.split("_")
        if len(divided) == 2:
            if divided[1] == "HFCE":
                break
            if divided[0] not in countriesSectorsDict:
                countriesSectorsDict[divided[0]] = [divided[1]]
            else:
                countriesSectorsDict[divided[0]].append(divided[1])
        elif len(divided) == 1:
            if divided[0] not in countriesSectorsDict:
                countriesSectorsDict[divided[0]] = []
    return countriesSectorsDict


def getCountries(file):
    inDict = getCountriesAndSectors(file)
    return list(inDict.keys())


def getSectors(file):
    inDict = getCountriesAndSectors(file)
    return list(inDict.values())[0]


def welcome():
    print("HELLO!!")
