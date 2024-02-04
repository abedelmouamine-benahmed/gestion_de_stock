#
#
#
#
import os
import mysql.connector 
from dotenv import load_dotenv

#Load ".env"
load_dotenv()


class connection:

    def __init__(self):
        
        #Database Connection 
        self.__host = os.getenv('host') 
        self.__user = os.getenv('user') 
        self.__password = os.getenv('passwd')
        self.__database = os.getenv('database')
        
    
    def _inventory_(self):
        try: 
            self.mydb = mysql.connector.connect(
                
                host = self.__host ,
                user = self.__user ,
                password = self.__password ,
                database = self.__database
            )
            print("Connection ok")
            self.cursor = self.mydb.cursor()
        
        except mysql.connector.Error as e:
                print(e)    
    
    #Turn off the cursor and database
    def _close_(self):
        self.cursor.close()
        self.mydb.close()


Connect = connection()
