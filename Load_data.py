import mysql.connector 
from Connection import Connection



class Load_data(Connection):
        def __init__(self):
            super().__init__()
            super()._inventory_()
            # super()._close_()

        def create(self,name,description,price,quantity,id_category):
                try:
                    sql = "INSERT INTO product (name,description,price,quantity,id_category) VALUES (%s,%s,%s,%s,%s) "
                    values = (name,description,price,quantity,id_category)
                    
                    self.cursor.execute(sql,values)
                    print(f"{name} Added successfully !")
                    self.mydb.commit()
                    super()._close_()

                except mysql.connector.Error as e:
                    print(f"Error: {e}")
                    self.mydb.rollback()

        def read(self):
            try:
                sql = "SELECT * FROM product"
                self.cursor.execute(sql)
                self.show_table = self.cursor.fetchall()
                for i in self.show_table:
                    print (i)
                self.mydb.commit()
                super()._close_()
                        
            except mysql.connector.Error as e:
                print(f"Error: {e}")
                self.mydb.rollback()

    
            
        def update(self,colonne,new_name,id):
            try:
                match(colonne):
                    case 'name':
                        sql = "UPDATE product SET name = %s WHERE id = %s"
                    case 'description':
                        sql = "UPDATE product SET description = %s WHERE id = %s"
                    case 'quantity':
                        sql = "UPDATE product SET quantity = %s WHERE id = %s"
                    case 'price':
                        sql = "UPDATE product SET price = %s WHERE id = %s"
                    case 'id_category':
                        sql = "UPDATE product SET id_category = %s WHERE id = %s"
                    case _:
                        print('Column name no found')
                
                values = (new_name,id)
                self.cursor.execute(sql,values)
                self.mydb.commit()
                print("Product updated successfully")
                super()._close_()
            
            except mysql.connector.Error as e:
                print(f"Error: {e}")
                self.mydb.rollback()
        
        
        def delete(self,id):
            try:    
                sql = "DELETE FROM product WHERE id = %s"
                self.cursor.execute(sql,(id,))
                self.mydb.commit()
                print("Product deleted successfully")
                super()._close_()

            except mysql.connector.Error as e:
                print(f"Error: {e}")
                self.mydb.rollback()

if __name__ == '__name__':
    Load_data().run()

