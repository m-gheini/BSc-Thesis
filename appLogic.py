import os

countriesSectorsDict = {}

equivalentInApp = {"inputFile": "input-output table", "outputName": "Result File Name",
                   "outputPath": "Path To Save Result", "imCountry": "Importer Country", "imSector": "Importer Sector",
                   "exCountry": "Exporter Country", "exSector": "Exporter Sector", "shockSrc": "Source Of Shock",
                   "shockSign": "Sign Of Shock Value", "shockAmount": "Shock Amount",
                   "shockTo": "Shock To", "shockItr": "Iteration",
                   "shockThr": "Threshold", "imScenario": "Importer Scenario", "exScenario": "Exporter Scenario",
                   "imAlter": "Alternative List For Importer", "exAlter": "Alternative List For Exporter"}

userInputDict = {"inputFile": "", "outputName": "", "outputPath": "", "imCountry": "", "imSector": "", "exCountry": "",
                 "exSector": "", "shockSrc": "", "shockSign": "", "shockAmount": "", "shockTo": "", "shockItr": "",
                 "shockThr": "", "imScenario": "", "exScenario": "", "imAlter": [], "exAlter": []}


def getInput(file):
    userInputDict["inputFile"] = file


def getOutName(name):
    userInputDict["outputName"] = name


def getOutPath(path):
    userInputDict["outputPath"] = path


def getImCountry(imCountry):
    userInputDict["imCountry"] = imCountry


def getImSector(imSector):
    userInputDict["imSector"] = imSector


def getExCountry(exCountry):
    userInputDict["exCountry"] = exCountry


def getExSector(exSector):
    userInputDict["exSector"] = exSector


def getShockSrc(src):
    userInputDict["shockSrc"] = src


def getShockSign(sign):
    userInputDict["shockSign"] = sign


def getShockAmount(amount):
    userInputDict["shockAmount"] = amount


def getShockTo(attr):
    userInputDict["shockTo"] = attr


def getShockIteration(itr):
    userInputDict["shockItr"] = itr


def getShockThreshold(thr):
    userInputDict["shockThr"] = thr


def getImScenario(imScn):
    userInputDict["imScenario"] = imScn
    if imScn != "option 4":
        userInputDict["imAlter"].append("NONE")


def getImAlternatives(imAltr):
    userInputDict["imAlter"] = [imAltr]


def getExScenario(exScn):
    userInputDict["exScenario"] = exScn
    if exScn != "option 4":
        userInputDict["exAlter"].append("NONE")


def getExAlternatives(exAltr):
    userInputDict["exAlter"] = [exAltr]


def checkUserInput(dict):
    emptyParameters = []
    for key in dict:
        if not dict[key]:
            emptyParameters.append(key)
    return emptyParameters


def getStartMessage():
    empties = checkUserInput(userInputDict)
    message = "Attention!!\n\n"
    if not empties:
        return "Successful"
    for name in empties:
        message += "\"" + equivalentInApp[name] + "\" is empty.\n\n"
    return message


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


def produceCountriesAndSectors(file):
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


def produceCountries(file):
    inDict = produceCountriesAndSectors(file)
    return list(inDict.keys())


def produceSectors(file):
    inDict = produceCountriesAndSectors(file)
    return list(inDict.values())[0]


# def getImporter():

# def getExporter():

def welcome():
    print("HELLO!!")
    print(userInputDict)
