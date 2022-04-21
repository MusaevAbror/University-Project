
from datetime import datetime
import sqlite3

from settings import db_path
from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self, id= None) -> None:
        self.id = id
        self.__isValid = True
    
    @property
    def isValid(self):
        return self.__isValid
    @isValid.setter
    def isValid(self, isValid):
        self.__isValid = isValid

    

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def get_by_id(id):
        pass
    @abstractmethod
    def delet(self):
        pass
    @abstractmethod
    def objects():
        pass
    
    def __str__(self) -> str:
        return f"{self.id}|"

class Ragion(BaseModel):
    table = 'Region'
    def __init__(self, name, id= None) -> None:
        super().__init__(id)
        self.name = name
        

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else :
            self.__name = ""
            self.__isValid = False

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    if self.id is None:
                        cursor.execute(f'''INSERT INTO {Ragion.table} ('Name')
                        VALUES ('{self.name}')''')
                        self.id = cursor.lastrowid
                    else:
                        
                        print("Update qilindi")
                        conn.execute(f'''
                        UPDATE {Ragion.table} set Name = '{self.name}' where ID = {self.id}
                        ''')
                    conn.commit()
            except:
                print("Bog`lanishda hatolik bo`ldi ")
            return True
        else :
            return False     
    
    

    
    def delet(self):
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE from {Ragion.table} where ID = {self.id}")
                conn.commit()
               
        except:
            print("ochirishda hatolik") 
            
    def objects():
        with sqlite3.connect(db_path) as conn:
            res = conn.execute(f''' SELECT *From {Ragion.table}''')
            for item in res:
                yield Ragion(item[1], item[0])
    def for_id(name_r):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            res = cursor.execute(f'''SELECT *from {Ragion.table} Where Name = "{name_r}" ''')
            for items in res:
                return items[0]



    def get_by_id(id):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            res = cursor.execute(f'''SELECT *from {Ragion.table} Where ID = {id}''')
            for item in res :
                return Ragion(item[1], item[0])
                
    def __str__(self) -> str:
        return super().__str__() + f"{self.name}"




class Districts(BaseModel):
    table = "Districts"
    def __init__(self, name, regionid, id=None) -> None:
        super().__init__(id)
        self.regionid = regionid
        self.name = name
    
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else :
            self.__name = ""
            self.isValid = False
    @property
    def regionid(self):
        return self.__regionid
    @regionid.setter
    def regionid(self, regionid):
        if isinstance(regionid, int) and Ragion.get_by_id(regionid) is not None:
            self.__regionid = regionid
        else :
            self.__regionid = 1
            self.isValid = False

    @property
    def ragion(self):
        return Ragion.get_by_id(self.regionid)

    
    def get_dis_id(reg_id):
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            res = cursor.execute(f'''Select *From {Districts.table} where RegionId = {reg_id}''')
            for items in res:
                return Districts(items[1], items[2], items[0])
            

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    if self.id is None:
                        cursor.execute(f'''INSERT INTO {Districts.table} (Name, Regionid)
                        VALUES ('{self.name}', {self.regionid})''')
                        self.id = cursor.lastrowid
                    else:
                        
                        conn.execute(f'''UPDATE {Districts.table} set Name = '{self.name}' , RegionId = {self.regionid} where ID = {self.id}''')
                    conn.commit()
                return True
            except:
                print("Boglanishda hatolik")
        else :
            return False
    def delet(self):
        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute(f'''DELETE from {Districts.table} where ID = {self.id}''')
                conn.commit()
                print(f"{self.id} - delet qilindi")
        except:
            print("Delet qilishda hatolik berdi ")
    
    
    def get_by_id(id):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                res = cursor.execute(f'''SELECT *From {Districts.table} where ID = {id}''')
                for item in res:
                    return Districts(item[1], item[2], item[0])
        except:
            print("saqlashda hatolik berildi ....")
    
    def objects():
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                res = cursor.execute(f'''SELECT *From {Districts.table}''')
                for item in res:
                    yield Districts(item[1], item[2], item[0])
        except:
            print("obectlarni qaytarishda hatolik boldi")
        

    def __str__(self) -> str:
        return super().__str__() + f"{self.name} | {self.regionid}"





class University(BaseModel):
    table = "University"
    def __init__(self, univer, rating, number_of_students, number_of_faculty, districtsid, id=None) -> None:
        super().__init__(id)
        self.univer = univer
        self.rating = rating 
        self.number_of_students = number_of_students
        self.number_of_faculty = number_of_faculty
        self.districtsid = districtsid

    @property
    def district(self):
        return Districts.get_by_id(self.districtsid)

    @property
    def univer(self):
        return self.__univer
    
    @univer.setter
    def univer(self, univer):
        if isinstance(univer, str):
            self.__univer = univer
        else :
            self.__univer = ""
            self.isValid = False
    @property
    def rating(self):
        return self.__rating
    
    @rating.setter
    def rating(self, rating):
        if isinstance(rating, int):
            self.__rating = rating
        else :
            self.__rating = 0
            self.isValid = False

    @property
    def number_of_students(self):
        return self.__number_of_students
    
    @number_of_students.setter
    def number_of_students(self, number_of_students):
            if isinstance(number_of_students, int) and number_of_students > 0:
                self.__number_of_students = number_of_students
            else:
                self.__number_of_students = 0
                self.isValid = False
    @property
    def number_of_faculty(self):
        return self.__number_of_faculty
    
    @number_of_faculty.setter
    def number_of_faculty(self, number_of_faculty):
        if isinstance(number_of_faculty, int) and number_of_faculty > 0:
            self.__number_of_faculty = number_of_faculty
        else:
            self.__number_of_faculty = 0
            self.isValid = False
    @property
    def districtsid(self):
        return self.__districtsid
    
    @districtsid.setter
    def districtsid(self, districtsid):
        if isinstance(districtsid, int) and districtsid > 0:
            self.__districtsid = districtsid
        else :
            self.districtsid = 0
            self.isValid = False
        
    def save(self):
        if self.isValid:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                if self.id is None:
                    cursor.execute(f'''INSERT INTO {University.table} (University, Rating, Number_of_Students, Number_of_Faculty, DistrictsId)
                    VALUES ('{self.univer}', {self.rating}, {self.number_of_students}, {self.number_of_faculty}, {self.districtsid})''')
                    self.id = cursor.lastrowid
                else :
                    cursor.execute(f'''UPDATE {University.table} set University = '{self.univer}', Rating = {self.rating}, Number_of_Students = {self.number_of_students},
                    Number_of_Faculty = {self.number_of_faculty}, Districtsid = {self.districtsid} where ID = {self.id}''')
                conn.commit()
            return True
        else :
            return False

    def get_by_id(id):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            res = cursor.execute(f'''SELECT *From {University.table} where ID = {id}''')
            for item in res:
                return University(item[1], item[2], item[3], item[4], item[5], item[0])
            conn.commit()

    def delet(self):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''DELETE from {University.table} where ID = {self.id}''')
            conn.commit()

    def objects():
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            res = cursor.execute(f'''SELECT *From {University.table}''')
            for items in res:
                yield University(items[1], items[2], items[3], items[4], items[5], items[0])
            conn.commit()
    def len_objects():
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            red = cursor.execute(f'''SELECT *From {University.table}''')
            len_objects = []
            for items in red:
                len_objects.append(items[1])
            return len(len_objects)

    
    def __str__(self) -> str:
        return super().__str__() + f"{self.univer} | {self.rating} | {self.number_of_students} | {self.number_of_faculty} | {self.districtsid}"


# Ragion.get_by_id(86).delet()
# Districts("chilonzor", 117).save()

