import os
import json
import backLogic as func

countriesSectorsDict = {}

equivalentInApp = {"inputFile": "input-output table", "outputName": "Result File Name",
                   "outputPath": "Path To Save Result", "imCountry": "Importer Country", "imSector": "Importer Sector",
                   "exCountry": "Exporter Country", "exSector": "Exporter Sector", "shockSrc": "Source Of Shock",
                   "shockSign": "Sign Of Shock Value", "shockAmount": "Shock Amount",
                   "shockTo": "Shock To", "shockStopAttribute": "Stop At", "shockItr": "Iteration",
                   "shockThr": "Threshold", "imScenario": "Importer Scenario", "exScenario": "Exporter Scenario",
                   "imAlter": "Alternative List For Importer", "exAlter": "Alternative List For Exporter"}

userInputDict = {"inputFile": "", "outputName": "", "outputPath": "", "imCountry": "", "imSector": "", "exCountry": "",
                 "exSector": "", "shockSrc": "", "shockSign": "", "shockAmount": "", "shockTo": "",
                 "shockStopAttribute": "", "shockItr": "", "shockThr": "", "imScenario": "", "exScenario": "",
                 "imAlter": "", "exAlter": ""}

imAlternatives = {}
exAlternatives = {}


def getConfigData(Path):
    configData = json.load(open(Path))
    return configData


def getUserInputDictFromSaved(configData):
    for key in configData:
        userInputDict[key] = configData[key]


def saveConfigFile(path):
    print(path)
    out_file = open(path, "w")
    json.dump(userInputDict, out_file, indent=6)
    out_file.close()


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


def getShockStopAttribute(attr):
    userInputDict["shockStopAttribute"] = attr


def getShockIteration(itr):
    userInputDict["shockItr"] = itr


def getShockThreshold(thr):
    userInputDict["shockThr"] = thr


# getAlternatives("1", "Country", "AUS")
# getAlternatives("1", "Sector", "T2910")
# getAlternatives("1", "Percent", "50")
# print(getImScenarioFromWindow())

def getImScenario(imScn):
    userInputDict["imScenario"] = imScn
    if imScn != "option 4":
        userInputDict["imAlter"] = "NONE"


def getImAlternatives(imAltr):
    userInputDict["imAlter"] = imAltr


def getAlternatives(tradingType, num, key, value):
    if tradingType == "Im":
        if num not in imAlternatives:
            imAlternatives[num] = {key: value}
        else:
            # if key not in imAlternatives[num]:
            imAlternatives[num][key] = value
    elif tradingType == "Ex":
        if num not in exAlternatives:
            exAlternatives[num] = {key: value}
        else:
            # if key not in imAlternatives[num]:
            exAlternatives[num][key] = value


def changeDataFromWindowToStr(tradeType):
    outStr = ""
    if tradeType == "Im":
        for key in imAlternatives:
            outStr += imAlternatives[key]['Country'] + "_" + imAlternatives[key]["Sector"] + " : " + \
                      imAlternatives[key]["Percent"] + ", "
        outStr = outStr[:len(outStr) - 2]
        userInputDict["imAlter"] = outStr
    elif tradeType == "Ex":
        for key in exAlternatives:
            outStr += exAlternatives[key]['Country'] + "_" + exAlternatives[key]["Sector"] + " : " + \
                      exAlternatives[key]["Percent"] + ", "
        outStr = outStr[:len(outStr) - 2]
        userInputDict["exAlter"] = outStr
    return outStr


def getExScenario(exScn):
    userInputDict["exScenario"] = exScn
    if exScn != "option 4":
        userInputDict["exAlter"] = "NONE"


def getExAlternatives(exAltr):
    userInputDict["exAlter"] = exAltr


def checkUserInput(dict):
    emptyParameters = []
    for key in dict:
        if not dict[key]:
            emptyParameters.append(key)
    return emptyParameters


def getWarningMessage():
    empties = checkUserInput(userInputDict)
    message = "Attention!!\n\n"
    for name in empties:
        message += "\"" + equivalentInApp[name] + "\" is empty.\n\n"
    return message


def checkAllInfo():
    empties = checkUserInput(userInputDict)
    if not empties:
        return True
    for name in empties:
        return False


def startProcessing(window):
    func.main(userInputDict, window, countriesSectorsDict)


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
        if elem[0] == "\"":
            elem = elem[1:]
        if elem[-1] == "\"":
            elem = elem[:-1]
        print(elem)
        divided = elem.split("_")
        if len(divided) == 2:
            if divided[1] == "HFCE":
                break
            if divided[0] not in countriesSectorsDict:
                countriesSectorsDict[divided[0]] = [divided[1]]
            else:
                if divided[1] not in countriesSectorsDict[divided[0]]:
                    countriesSectorsDict[divided[0]].append(divided[1])
        elif len(divided) == 1:
            if divided[0] not in countriesSectorsDict:
                countriesSectorsDict[divided[0]] = []
    return countriesSectorsDict


def getSectorsForCountry(country):
    return countriesSectorsDict[country]


def produceCountries(file):
    inDict = produceCountriesAndSectors(file)
    return list(inDict.keys())


def produceSectors(file):
    res = ["ALL"]
    inDict = produceCountriesAndSectors(file)
    for sector in list(inDict.values())[0]:
        res.append(sector)
    return res


def getItrCnt():
    return userInputDict["shockItr"]


# def getImporter():

# def getExporter():

def welcome():
    print("HELLO!!")
    print(userInputDict)
