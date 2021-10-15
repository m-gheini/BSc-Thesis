# def gatherParameters():
import os


def getResultFileAttr(name, path):
    print("1")
    if not os.path.exists(path):
        os.makedirs(path)
    print("2")
    name = name + '.CSV'
    print("3")
    open(os.path.join(path, name), 'wb')
    print("4")


def welcome():
    print("HELLO!!")
