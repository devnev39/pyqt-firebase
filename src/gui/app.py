import time
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize
import pandas as pd
from src.database.app import db

exporter = {'.json' : pd.DataFrame.to_json,'.csv' : pd.DataFrame.to_csv}

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uploadBtn = QPushButton('Upload File')
        self.loadFromFireStoreBtn = QPushButton('Load from firestore')
        self.processBtn = QPushButton('Export')
        self.rowLabel = QLabel()
        self.pathLabel = QLabel()
        self.statusLabel = QLabel('idle')
        self.exportTypeComboBox = QComboBox()
        self.dataTable = QTableWidget()

        self.processBtn.setDisabled(True)
        self.uploadBtn.clicked.connect(self.uploadClicked)
        self.processBtn.clicked.connect(self.processClicked)

        self.loadFromFireStoreBtn.clicked.connect(self.loadDataFromFirestore)

        self.addExportTypes(['.JSON','.CSV'])
        # self.exportTypeComboBox.currentIndexChanged.connect(self.exportTypeChanged)

        mainLayout = QVBoxLayout()
        subBtnLayout = QHBoxLayout()
        midBtnLayout = QHBoxLayout()

        subBtnLayout.addWidget(self.uploadBtn)
        subBtnLayout.addWidget(self.pathLabel)
        
        mainLayout.addLayout(subBtnLayout)
        mainLayout.addWidget(self.loadFromFireStoreBtn)
        mainLayout.addWidget(self.dataTable)

        midBtnLayout.addWidget(self.processBtn)
        midBtnLayout.addWidget(self.exportTypeComboBox)

        mainLayout.addLayout(midBtnLayout)
        mainLayout.addWidget(self.rowLabel)
        mainLayout.addWidget(self.statusLabel)

        container = QWidget()
        container.setLayout(mainLayout)

        self.setCentralWidget(container)

        # self.setFixedSize(QSize(500,150))

        self.dataFrame = None
        self.filename = None
    
    def loadDataFromFirestore(self):
        docs = db.collection('data').stream()
        odocs = []
        for doc in docs:
            odocs.append(doc.to_dict())
        self.dataFrame = pd.DataFrame.from_records(odocs)
        if(len(odocs)):
            self.processBtn.setDisabled(False)
        self.addDataToTable()
        pass

    def addExportTypes(self,types : list):
        if not list:
            raise Exception('Types list not provided !')
        for type in types:
            self.exportTypeComboBox.addItem(type)
        self.exportTypeComboBox.setCurrentIndex(0)


    def uploadClicked(self):
        try:
            filename = QFileDialog.getOpenFileName(self,filter=('*.xlsx'))
            if filename[0].count('.xlsx'):
                self.statusLabel.setText('loading...')
                self.filename = filename[0]
                self.pathLabel.setText(self.filename)
                self.processBtn.setDisabled(False)
                t = time.perf_counter()
                self.dataFrame = pd.read_excel(filename[0])
                self.addDataToTable()
                self.rowLabel.setText(f'Total {self.dataFrame.shape[0]} rows | loaded in {round(time.perf_counter() - t,2)} sec !')
                self.statusLabel.setText("idle")
            else:
                raise Exception('Excel file not found !')
        except Exception as ex:
            print(ex)

    def addDataToTable(self):
        self.dataTable.setRowCount(self.dataFrame.shape[0])
        self.dataTable.setColumnCount(self.dataFrame.shape[1])
        self.dataTable.setHorizontalHeaderLabels(self.dataFrame.columns.to_list())
        
        for row in range(self.dataFrame.shape[0]):
            for col in range(self.dataFrame.shape[1]):
                self.dataTable.setItem(row,col,QTableWidgetItem(str(self.dataFrame.values[row,col])))

    def processClicked(self):
        t = time.perf_counter()
        if self.filename:
            export_filename = self.filename.replace('.xlsx',self.exportTypeComboBox.currentText().lower())
        else:
            export_filename = 'data'+self.exportTypeComboBox.currentText().lower()
        exporter.get(self.exportTypeComboBox.currentText().lower())(self.dataFrame,export_filename)
        self.statusLabel.setText(f'processed in {round(time.perf_counter() - t,2)} seconds')