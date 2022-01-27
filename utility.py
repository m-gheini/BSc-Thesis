import csv


def getTechnicalCoefficients(Z, X):
    return Z.div(X.iloc[0] + 0.000000001)


def createShockLog(path, header):
    with open(path, 'w+', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)


def writeShockLog(path, data):
    with open(path, 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
