from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5

from model import Ragion

class RagionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(PyQt5.QtCore.Qt.Window)
        self.setWindowTitle("Ragion")
        
        self.row_count = 0
        self.initUi()
        self.sel_ragion = None

    def initUi(self):
        self.setGeometry(200, 200, 600, 500)

        self.ql_ragion_name = QLabel(self)
        self.ql_ragion_name.setText("Ragion Name : ")
        self.ql_ragion_name.move(30, 30)

        self.qle_ragion_name = QLineEdit(self)
        self.qle_ragion_name.move(120, 30)

        self.btn_add = QPushButton("Add", self)
        self.btn_add.move(450, 30)
        self.btn_add.clicked.connect(self.onAdd)

        self.btn_update = QPushButton("Update",self)
        self.btn_update.move(450, 60)
        self.btn_update.clicked.connect(self.onUpdate)

        self.btn_del = QPushButton("Delete", self)
        self.btn_del.move(450, 90)
        self.btn_del.clicked.connect(self.onDel)
       
        self.table = QTableWidget(self)
        
        self.table.setGeometry(30, 60, 400, 400)
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(["Id", "Ragion Name"])
        self.table.horizontalHeaderItem(1).setToolTip("This is Ragion Name") # birinchi ustunga shu yozuvni chiqaradi
        self.table.hideColumn(0)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignRight) # ustunni ong yoki chpdan joylashtrish

        for item in Ragion.objects():
            self.table.setRowCount(self.row_count + 1)
            self.table.setItem(self.row_count, 0, QTableWidgetItem(str(item.id)))
            self.table.setItem(self.row_count, 1, QTableWidgetItem(str(item.name)))
            self.row_count += 1

        self.table.resizeColumnsToContents() # Agar Region tablega sig`masa avtomatik tarzda Table Regionga nisbatan o`zgaradi`
        self.table.clicked.connect(self.onClicked)

    
    def onAdd(self):
        reg = Ragion(self.qle_ragion_name.text())
        reg.save()
        self.table.setRowCount(self.row_count + 1)
        self.table.setItem(self.row_count, 0, QTableWidgetItem(str(reg.id)))
        self.table.setItem(self.row_count, 1, QTableWidgetItem(str(reg.name)))
        self.row_count += 1
    
    def onUpdate(self):
        if self.sel_ragion is not None:
            self.sel_ragion.name = self.qle_ragion_name.text()
            self.sel_ragion.save()
            self.table.setItem(self.sel_row, 1, QTableWidgetItem(str(self.sel_ragion.name)))
            
            

    def onClicked(self, items):
        self.sel_row = self.table.currentRow()
        self.qle_ragion_name.setText(self.table.item(self.sel_row, 1).text())
        self.sel_ragion = Ragion(self.table.item(self.sel_row, 1).text(), self.table.item(self.sel_row, 0).text())
        print(self.sel_row)

    def onDel(self):
        if self.sel_ragion is not None:
            self.sel_ragion.delet()
            self.sel_ragion = None  
            self.table.removeRow(self.sel_row)
            self.row_count -= 1
