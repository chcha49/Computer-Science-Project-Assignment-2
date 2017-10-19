import pandas
from textblob.classifiers import DecisionTreeClassifier
from textblob.classifiers import NaiveBayesClassifier

def buildmodels():
    dataset = pandas.read_csv("comments.csv")
    keywords = ["suicidal","suicide","kill myself","my suicide note","my suicide letter","end my life",
                "never wake up","can't go on","not worth living","ready to jump","sleep forever",
                "want to die","be dead","better off without me","better off dead","suicide plan",
                "suicide pact","tired of living","don't want to be here","die alone","go to sleep forever"]
    array = []
    for m in dataset.message:
        c = 0
        for k in keywords:
            if type(m) is not str:
                c = 2
            elif k in m:
                c = 1
        if c == 0:
            array.append((m,"neg"))
        elif c == 1:
            array.append((m,"pos"))

    split = int(0.7 * (len(array)))
    train = array[0:split]
    cl1 = DecisionTreeClassifier(train)
    cl2 = NaiveBayesClassifier(train)
    if cl1 and cl2:
        message = True
    else:
        message = False
    return message

def accuracyCalculation():
    dataset = pandas.read_csv("comments.csv")
    keywords = ["suicidal", "suicide", "kill myself", "my suicide note", "my suicide letter", "end my life",
                "never wake up", "can't go on", "not worth living", "ready to jump", "sleep forever",
                "want to die", "be dead", "better off without me", "better off dead", "suicide plan",
                "suicide pact", "tired of living", "don't want to be here", "die alone", "go to sleep forever"]
    array = []
    for m in dataset.message:
        c = 0
        for k in keywords:
            if type(m) is not str:
                c = 2
            elif k in m:
                c = 1
        if c == 0:
            array.append((m, "neg"))
        elif c == 1:
            array.append((m, "pos"))

    split = int(0.7 * (len(array)))
    train = array[0:split]
    test = array[split:]
    cl1 = DecisionTreeClassifier(train)
    a1 = cl1.accuracy(test)
    cl2 = NaiveBayesClassifier(train)
    a2 = cl2.accuracy(test)
    if a1 and a2:
        message = True
    else:
        message = False
    return message

def test_buildmodels():
    assert buildmodels() is True
    print("successful")

def test_accuracyCalculation():
    assert accuracyCalculation() is True
    print("successful")





if __name__ == "__main__":
    test_buildmodels()
    test_accuracyCalculation()
