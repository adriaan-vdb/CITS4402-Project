from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget

import sys

from sklearn import svm
import pickle
import os
import numpy as np



window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on earth',
    'What on earth',
    'This is surprising',
    'This is surprising',
    'Something went wrong'
]

class MainWindow(QMainWindow):
    def __init__(self):
        ##Guis stuff
        super().__init__()

        self.setWindowTitle("project")

        button = QPushButton("HOG window")
        button.clicked.connect(self.swapWindow)

        self.setCentralWidget(button)
        self.show()

        ##Model stuff
        self.model=svm.SVC()

    def swapWindow(self):
        w = HOGWindow()
        w.show()

    def loadModel(self,filename):
        with open(filename, 'rb') as f:
            self.model = pickle.load(f)

    def loadTrainingData(self):
        data=[]
        label=[]
        for entry in os.scandir("people"):
            if entry.name.endswith(".txt"):
                data.append(np.loadtxt(entry.path, delimiter=',').flatten())
                label.append(1)
        for entry in os.scandir("notpeople"):
            if entry.name.endswith(".txt"):
                data.append(np.loadtxt(entry.path, delimiter=',').flatten())
                label.append(0)
        return label, data
    
    def loadTestData(self, numTrue=100,TFratio=1):
        testdata=[]
        results=[]
        Tnum=0
        Fnum=0
        for entry in os.scandir("trainHOG"):
            if entry.name.endswith("T.txt") and Tnum<numTrue:
                testdata.append(np.loadtxt(entry.path, delimiter=',').flatten())
                Tnum=Tnum+1 
                results.append(1)
            elif entry.name.endswith("F.txt") and Fnum<numTrue*TFratio:
                testdata.append(np.loadtxt(entry.path, delimiter=',').flatten())
                Fnum=Fnum+1
                results.append(0)
        return results,testdata
    
    def fitModel(self,label,data):
        self.model.fit(data,label)

    def evaluate(self,result,testdata):
        q=self.model.predict(testdata)
        score=len(result)
        for guess in range(0,100):
            score=score-(q[guess]+result[guess])%2
        return 100*(score/len(result))

class HOGWindow(QWidget):
     def __init__(self):
        ##Guis stuff
        super().__init__()

        self.setWindowTitle("HOG")

        button = QPushButton("close")
        button.pressed.connect(self.close)

        # self.setCentralWidget(button)


app = QApplication(sys.argv)
w = MainWindow()
app.exec()