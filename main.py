import sys
import traceback
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from openpyxl import Workbook
from windows.RagionWindow import RagionWindow
from windows.DistrictsWindow import DistrictsWindow 
from model import University, Districts
from windows.help import *




class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.initActions()
        self.initMenu()
        self.initTable()
        self.filTable()
        self.qmsg = QMessageBox()

    
        
       

    def initUi(self):

        self.btn_add = QPushButton("Add", self)
        self.btn_add.move(30,30)
        self.btn_add.clicked.connect(self.onAdd)

        self.btn_up = QPushButton("Update", self)
        self.btn_up.move(130, 30)
        self.btn_up.clicked.connect(self.onUp)

        self.btn_del = QPushButton("Delete", self)
        self.btn_del.move(230, 30)
        self.btn_del.clicked.connect(self.onDel)

        self.btn_report = QPushButton("Report", self)
        self.btn_report.move(330, 30)
        self.btn_report.clicked.connect(self.onReport)

        self.s_box = QSpinBox(self)
        self.s_box.move(500, 900)
        
        self.box_val = self.s_box.value()

        
       

        self.btn_search = QPushButton("Поиск", self)
        self.btn_search.move(930, 100)

        self.ql = QLabel("University : ", self)
        self.ql.move(1050, 160)
        self.ql = QLabel("Rating : ", self)
        self.ql.move(1050, 200)
        self.ql = QLabel("Number of Students : ", self)
        self.ql.move(1050, 240)
        self.ql = QLabel("Number of faculty : ", self)
        self.ql.move(1050, 280)
        self.ql = QLabel("Viloyat", self)
        self.ql.move(1050, 320)

        un_list = []
        ra_list = []
        num_s_list = []
        num_f_list = []
        for item in University.objects():
            un_list.append(item.univer)
            ra_list.append(str(item.rating))
            num_f_list.append(str(item.number_of_faculty))
            num_s_list.append(str(item.number_of_students))
            

        self.qle_search = QLineEdit(self)
        self.qle_search.move(30, 100)
        self.qle_search.setMinimumWidth(880)
        self.qle_search.setCompleter(QCompleter(un_list, self.qle_search))
        self.qle_search.textEdited.connect(self.onSearch)
        
        self.qle_un = QLineEdit(self)
        self.qle_un.move(1200, 160)
        self.qle_un.setCompleter(QCompleter(un_list, self.qle_un))
    
        self.qle_ra = QLineEdit(self)
        self.qle_ra.move(1200, 200)
        self.qle_ra.setCompleter(QCompleter(ra_list, self.qle_ra))

        self.qle_num_s = QLineEdit(self)
        self.qle_num_s.move(1200, 240)
        self.qle_num_s.setCompleter(QCompleter(num_s_list, self.qle_num_s))

        self.qle_num_f = QLineEdit(self)
        self.qle_num_f.move(1200, 280)
        self.qle_num_f.setCompleter(QCompleter(num_f_list, self.qle_num_f))

        self.cbb_dist = QComboBox(self)
        self.cbb_dist.move(1200, 320)
        for items in Districts.objects():
            self.cbb_dist.addItem(items.name, items.id)

        

    def initActions(self):
        self.newAction = QAction("&New...", self)
        self.openAction = QAction("&Open...", self)
 
        self.ragionActions = QAction("&Ragions", self)
        self.ragionActions.triggered.connect(self.onRagionWindow)
        self.districtsActions = QAction("&Districts", self)
        self.districtsActions.triggered.connect(self.onDistrictsWindow)
        self.helpActions = QAction("&help", self)
        self.helpActions.triggered.connect(self.helpactions)

        
    def initMenu(self):
        menubar = self.menuBar()
        self.setMenuBar(menubar)

        filemenu = menubar.addMenu("&File")
        filemenu.addAction(self.newAction)
        filemenu.addAction(self.openAction)

        serviceMenu = menubar.addMenu("&Service")
        serviceMenu.addAction(self.ragionActions)
        serviceMenu.addAction(self.districtsActions)

        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(self.helpActions)

    def helpactions(self):
        self.help = helpSender()
        self.help.show()
        

    def onRagionWindow(self):
        self.reg = RagionWindow()
        self.reg.show()

    def onDistrictsWindow(self):
        self.dis = DistrictsWindow()
        self.dis.show()

    def initTable(self):
        self.table = QTableWidget(self)
        self.table.move(30, 150)
        self.table.setMinimumSize(1000, 800)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "University", "Rating", "Number of Students", "Number of faculty", "Viloyati" , "tuman id", "Tumani"])
        self.table.hideColumn(0)
        self.table.hideColumn(6)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.table.resizeColumnsToContents()    
        self.table.clicked.connect(self.onclicked)

    def filTable(self):
        self.table.setRowCount(0)
        self.table.clear()
        self.table.setHorizontalHeaderLabels(["ID", "University", "Rating", "Number of Students", "Number of faculty", "Viloyati" , "tuman id", "Tumani"])
        self.table.hideColumn(0)
        self.table.hideColumn(6)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        for item in University.objects():
            dist = item.district
            reg = dist.ragion
            row_count = self.table.rowCount()
            self.table.setRowCount(row_count + 1)
            self.table.setItem(row_count, 0, QTableWidgetItem(str(item.id)))
            self.table.setItem(row_count, 1, QTableWidgetItem(item.univer))
            self.table.setItem(row_count, 2, QTableWidgetItem(str(item.rating)))
            self.table.setItem(row_count, 3, QTableWidgetItem(str(item.number_of_students)))
            self.table.setItem(row_count, 4, QTableWidgetItem(str(item.number_of_faculty)))
            self.table.setItem(row_count, 5, QTableWidgetItem(reg.name))
            self.table.setItem(row_count, 6, QTableWidgetItem(str(reg.id)))
            self.table.setItem(row_count, 7, QTableWidgetItem(dist.name))     
            self.table.resizeColumnsToContents()       

    def onclicked(self):
        self.sel_row = self.table.currentRow()

        self.un_name = self.table.item(self.sel_row, 1).text()
        self.un_rating = self.table.item(self.sel_row, 2).text()
        self.un_num_s = self.table.item(self.sel_row, 3).text()
        self.un_num_f = self.table.item(self.sel_row, 4).text()
        self.un_reg = self.table.item(self.sel_row, 5).text()
        self.un_reg_id = self.table.item(self.sel_row, 6).text()
        self.un_dist = self.table.item(self.sel_row, 7).text()
        self.qle_un.setText(self.un_name)
        self.qle_ra.setText(self.un_rating)
        self.qle_num_s.setText(self.un_num_s)
        self.qle_num_f.setText(self.un_num_f)
        self.cbb_dist.setCurrentText(self.un_dist)
        
    def onAdd(self):
        try:
            dist_id = self.cbb_dist.currentData()
            univer = University(self.qle_un.text(), int(self.qle_ra.text()), int(self.qle_num_s.text()), int(self.qle_num_f.text()), dist_id)
            univer.save()
            self.filTable()
            self.qmsg.setIcon(QMessageBox.Information)
            self.qmsg.setWindowTitle("Bajarildi")
            self.qmsg.setText("Universitet Saqlandi")
            self.qmsg.show()
        except Exception as exp:
            self.qmsg.setIcon(QMessageBox.Critical)
            self.qmsg.setWindowTitle("Bajarilmadi")
            self.qmsg.setText(str(exp))
            self.qmsg.show()
            traceback.print_exc()
            
    def onUp(self):
        try:
            dist_id = self.cbb_dist.currentData()
            un_id = int(self.table.item(self.sel_row, 0).text())
            univer = University(self.qle_un.text(), int(self.qle_ra.text()), int(self.qle_num_s.text()), int(self.qle_num_f.text()), dist_id, un_id)
            univer.save()
            self.filTable()
            self.qmsg.setIcon(QMessageBox.Information)
            self.qmsg.setWindowTitle("Bajarildi")
            self.qmsg.setText("Universitet Yangilandi")
            self.qmsg.show()
        except Exception as exp:
            self.qmsg.setIcon(QMessageBox.Critical)
            self.qmsg.setWindowTitle("Xatolik ?")
            self.qmsg.setText(str(exp))
            self.qmsg.show()
            traceback.print_exc()
            

    def onDel(self):
        try:
            un_id = self.table.item(self.sel_row, 0).text()
            un = self.table.item(self.sel_row, 1).text()
            
            un_rating = self.table.item(self.sel_row, 2).text()
            un_num_stu = self.table.item(self.sel_row, 3).text()
            un_num_fac = self.table.item(self.sel_row, 4).text()
            dist_id = self.cbb_dist.currentData()
            univer_del = University(str(un), int(un_rating), int(un_num_stu), int(un_num_fac), int(dist_id), int(un_id))
            univer_del.delet()
            self.filTable()
            self.qmsg.setIcon(QMessageBox.Information)
            self.qmsg.setWindowTitle("Bajarildi")
            self.qmsg.setText("Universitet o`chirildi")
            self.qmsg.show()
        except Exception as exp:
            self.qmsg.setIcon(QMessageBox.Critical)
            self.qmsg.setWindowTitle("Bajarilmadi")
            self.qmsg.setText(str(exp))
            self.qmsg.show()
    
    def onReport(self):
        wb = Workbook()
        try:
             
            we = wb.active
            we[f'A{1}'] = "University"
            we[f'B{1}'] = "Rating"
            we[f'C{1}'] = "Talabalar soni"
            we[f'D{1}'] = "Facultetlar soni"
            we[f'E{1}'] = "Viloyat"
            we[f'F{1}'] = "Tuman"

            for n_row in range(self.table.rowCount()):
                university = self.table.item(n_row, 1).text()
                rating = self.table.item(n_row, 2).text()
                num_student = self.table.item(n_row, 3).text()
                num_faculty = self.table.item(n_row, 4).text()
                viloyat = self.table.item(n_row, 5).text()
                tuman = self.table.item(n_row, 6).text()

                we[f'A{n_row + 2}'] = university
                we[f'B{n_row + 2}'] = rating
                we[f'C{n_row + 2}'] = num_student
                we[f'D{n_row + 2}'] = num_faculty
                we[f'E{n_row + 2}'] = viloyat
                we[f'F{n_row + 2}'] = tuman
           
            file , check = QFileDialog.getSaveFileName(self, f"QFileDialog.getSaveFileName()", "", "Excel File(.xlsx)")
            if not check:
                return
            wb.save(file)
            self.qmsg.setIcon(QMessageBox.Information)
            self.qmsg.setWindowTitle("Bajarildi")
            self.qmsg.setText("Universitetlar royhati saqlandi")
            self.qmsg.show()
            wb.close()

        except Exception as exp:
            self.qmsg.setIcon(QMessageBox.Critical)
            self.qmsg.setWindowTitle("Xatolik")
            self.qmsg.setText(str(exp))
            self.qmsg.show()
            wb.close()

    def onSearch(self, text):
        self.search_text = str(text)
        self.table.clear()
        self.table.setRowCount(0)
       
        
        for items in University.objects():
            dist = items.district
            reg = dist.ragion
            self.table.setHorizontalHeaderLabels(["ID", "University", "Rating", "Number of Students", "Number of faculty", "Viloyati" , "tuman id", "Tumani"])
            self.table.hideColumn(0)
            self.table.hideColumn(6)
            self.table.setSelectionBehavior(QTableWidget.SelectRows)
            row_count = self.table.rowCount()
            if (self.search_text).upper() in str(items.univer).upper():
                self.table.setRowCount(row_count + 1)
                
                self.table.setItem(row_count, 0, QTableWidgetItem(str(items.id)))
                self.table.setItem(row_count, 1, QTableWidgetItem(items.univer))
                self.table.setItem(row_count, 2, QTableWidgetItem(str(items.rating)))
                self.table.setItem(row_count, 3, QTableWidgetItem(str(items.number_of_students)))
                self.table.setItem(row_count, 4, QTableWidgetItem(str(items.number_of_faculty)))
                self.table.setItem(row_count, 5, QTableWidgetItem(reg.name))
                self.table.setItem(row_count, 6, QTableWidgetItem(str(reg.id)))
                self.table.setItem(row_count, 7, QTableWidgetItem(dist.name))
                self.table.resizeColumnsToContents()


        

app = QApplication(sys.argv)
win = Window() 
win.showMaximized()
app.exec()

