class Metrics:
  
    accuracy = []
    f1score = []
    FAR = []
    FRR = []
    ROC = []
    falseAccept = []
    falseReject= []
    trueAccept = []
    trueReject= []
    sizeTest = []

    def __init__(self):
        self.accuracy = []
        self.f1score = []
        self.FAR = []
        self.FRR = []
        self.ROC = []
        self.falseAccept = []
        self.falseReject= []
        self.trueAccept = []
        self.trueReject= []
        self.sizeTest = []

    # Set Methods
    def setAccuracy(self, value):
        self.accuracy.append(value)

    def setf1score(self, value):
        self.f1score.append(value)

    def setFAR(self, value):
        self.FAR.append(value)

    def setFRR(self, value):
        self.FRR.append(value)

    def setfalseAccept(self, value):
        self.falseAccept.append(value)
    
    def setfalseReject(self, value):
        self.falseReject.append(value)

    def settrueAccept(self, value):
        self.trueAccept.append(value)

    def settrueReject(self, value):
        self.trueReject.append(value)

    def setsizeTest(self, value):
        self.sizeTest.append(value)

    # Get Methods
    def getAccuracy(self):
        return self.accuracy

    def getf1score(self):
        return self.f1score

    def getFAR(self):
        return self.FAR

    def getFRR(self):
        return self.FRR

    def getfalseAccept(self):
        return self.falseAccept
    
    def getfalseReject(self):
        return self.falseReject

    def gettrueAccept(self):
        return self.trueAccept

    def gettrueReject(self):
        return self.trueReject

    def getsizeTest(self):
        return self.sizeTest
    
    