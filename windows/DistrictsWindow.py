
from typing import Type
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from model import Districts, Ragion

class DistrictsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.cbb()

        
    def initUI(self):
        self.setGeometry(200,200, 700, 600)
        self.resize(700, 600)

        self.ql_region = QLabel("Region", self)
        self.ql_region.move(30,30)
        
        self.cbb_region = QComboBox(self)
        self.cbb_region.move(80, 30)
        for reg in Ragion.objects():
            self.cbb_region.addItem(reg.name, reg.id)
        
        self.cbb_region.currentIndexChanged.connect(self.cbb) 
        
        self.ql_dis = QLabel("District Name", self)
        self.ql_dis.move(290, 30)
        self.le_dist = QLineEdit(self)
        self.le_dist.move(385, 30)

        self.btn_add = QPushButton("Add", self)
        self.btn_add.move(540, 40)
        self.btn_add.clicked.connect(self.onAdd)

        self.btn_update = QPushButton("Update", self)
        self.btn_update.move(540, 80)
        self.btn_update.clicked.connect(self.onUpdate)

        self.btn_delet = QPushButton("Delet", self)
        self.btn_delet.move(540, 120)
        self.btn_delet.clicked.connect(self.onDel)

        


        self.table = QTableWidget(self)
        self.table.setGeometry(30, 70, 480, 500)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Reg Id", "Region Name", "dist id", "District Name"])
        self.table.setRowCount(0)
        self.table.hideColumn(0)
        self.table.hideColumn(2)
        self.table.setSelectionBehavior(QTableWidget.SelectRows) # barcha yacheykani bir vaqtda tanlash uchun

        self.table.clicked.connect(self.onClicked)


    

    def onAdd(self):
        res = Districts(self.le_dist.text(),self.cbb_region.currentData())
        res.save()
        self.cbb()

    def onUpdate(self):
        dist_name = self.le_dist.text()
        reg_id = self.cbb_region.currentData()
        dist_id = int(self.table.item(self.sel_row, 2).text())
        print(type(reg_id), "   ", reg_id)
        dist = Districts(dist_name, reg_id, dist_id)
        dist.save()
        self.cbb()

    def onDel(self):
        dist_name = self.le_dist.text()
        reg_id = self.cbb_region.currentData()
        dist_id = int(self.table.item(self.sel_row, 2).text())
        res = Districts(dist_name, reg_id, dist_id)
        res.delet()
        self.cbb()
        
            
    def cbb(self):
        self.table.clear()
        currentId = self.cbb_region.currentData()
        
        self.table.setHorizontalHeaderLabels(["Reg Id", "Region Name", "dist id", "District Name"])
        self.table.setRowCount(0)
        print(self.table.setRowCount(0))
        self.table.hideColumn(0)
        self.table.hideColumn(2)
        self.table.setRowCount(0)
        for dist in Districts.objects():
            if currentId == dist.regionid:
                row_count = self.table.rowCount()
                
                self.table.setRowCount(row_count + 1)
                self.table.setItem(row_count, 0, QTableWidgetItem(str(currentId)))
                self.table.setItem(row_count, 1, QTableWidgetItem(str(Ragion.get_by_id(currentId).name)))
                self.table.setItem(row_count, 2, QTableWidgetItem(str(dist.id)))
                self.table.setItem(row_count, 3, QTableWidgetItem(str(dist.name)))
                
                
    

    
    def onClicked(self):
        self.sel_row = self.table.currentRow()
        dist_name = self.table.item(self.sel_row, 3).text()
        self.le_dist.setText(dist_name)
