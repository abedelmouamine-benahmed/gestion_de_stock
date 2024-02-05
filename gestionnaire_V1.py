from flet import *
import flet as ft

from dotenv import load_dotenv
import os
import mysql.connector 

#Load ".env"
load_dotenv()

mydb = mysql.connector.connect(       
        host = os.getenv('host'),
        user = os.getenv('user'),
        password = os.getenv('passwd'),
        database = os.getenv('database')
    )

cursor = mydb.cursor()   
 

def main(page:Page):
    page.title = 'Inventory'
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    id:TextField = TextField(label='id',width=400)
    name: TextField = TextField(label='name',width=400)
    description: TextField = TextField(label='description',width=400 )
    price: TextField = TextField(label='price',width=400 )
    quantity: TextField = TextField(label='quantity',width=400 )
    id_category: TextField = TextField(label='id_category Électronique:1 Vêtements:2 Meubles:3',width=400 )
    # button_submit: ElevatedButton = ElevatedButton(text='Save',width=400,disabled=True)
    
    edit_id: TextField = TextField(label='id')
    edit_name: TextField = TextField(label='name')
    edit_description: TextField = TextField(label='description' )
    edit_price: TextField = TextField(label='price' )
    edit_quantity: TextField = TextField(label='quantity' )
    # edit_id_category: TextField = TextField(label='id_category Électronique:1 Vêtements:2 Meubles:3')
    page.update()
    
    Database = DataTable(
        columns=[
            DataColumn(Text("id")),
            DataColumn(Text("name")),
            DataColumn(Text("description")),
            DataColumn(Text("price")),
            DataColumn(Text("quantity")),
            DataColumn(Text("actions"))
        ],
        rows=[]
    )
    page.update()

    def deletebtn(e):
        '''Method How Delete the row in the database and refesh the page'''
       
        try:
            sql = "DELETE FROM Product WHERE id = %s"
            val = (e.control.data['id'],)
            cursor.execute(sql,val)
            mydb.commit()
            
            Database.rows.clear()
            load_data()   
        
        except Exception as e:
            print(e)
    

    def save_data(e):
        '''Method how Update the Database and refesh the page '''
       
        try:
            sql = "UPDATE product SET id = %s, name = %s, description = %s, price = %s, quantity = %s WHERE id = %s"
            
            values = (edit_id.value,edit_name.value,edit_description.value,edit_price.value,edit_quantity.value,edit_id.value)
            cursor.execute(sql,values)
            dialog.open = False 
            mydb.commit()
            page.update()

            edit_id.value = ""
            edit_name.value = ""
            edit_description.value = ""
            edit_price.value = ""
            edit_quantity.value = ""
            
            
            Database.rows.clear()
            load_data()   

            page.update()
        
        except mysql.connector.Error as e:
                print(f"Error: {e}")
                mydb.rollback()
    
    
    def editebtn(e):
        '''bottom how modify the data '''
        
        edit_id.value = e.control.data["id"]
        edit_name.value = e.control.data["name"]
        edit_description.value = e.control.data["description"]
        edit_price.value = e.control.data["price"]
        edit_quantity.value = e.control.data["quantity"]
        # edit_id_category.value = e.control.data["id_category"]
        page.dialog = dialog
        dialog.open = True
        
        page.update()
    
    
    dialog = AlertDialog(
        title = Text("Edit"),
        content=Column([
            edit_id,
            edit_name,
            edit_description,
            edit_price,
            edit_quantity,           
        ]),
        actions=[
            TextButton("Save",
                on_click=save_data
                )
        ])
    
    
    def load_data():
        '''Method how can read the '''
       
        cursor.execute("SELECT * FROM product")
        results = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in results]

        for row in rows:
            Database.rows.append(
                DataRow(cells=[
                    DataCell(Text(row['id'])),
                    DataCell(Text(row['name'])),
                    DataCell(Text(row['description'])),
                    DataCell(Text(row['price'])),
                    DataCell(Text(row['quantity'])),
                    DataCell(
                        Row([
                        IconButton("Delete",icon_color="red",
                            data=row,
                            on_click=deletebtn,
                            ),
                        IconButton("Create",icon_color="green",
                            data=row,
                            on_click=editebtn,
                            ),
                             
                            ]))
                ])    
            )
            page.update()
    
    # load_data()
    def add_data(e):
        try:    
            sql = "INSERT INTO product (name,description,price,quantity,id_category) VALUES (%s,%s,%s,%s,%s) "
            values = (name.value,description.value,price.value,quantity.value,id_category.value)
            
            cursor.execute(sql,values)
            print(f"{name.value} Added successfully !")
            mydb.commit()

            Database.rows.clear()
            load_data()
        except Exception as e:
            print(e)

    page.add(Column([
        name,
        description,
        price,
        quantity,
        id_category,
        ElevatedButton('add to Database',
            on_click=add_data
            ),
        Database
        ]
    ))
    Database.rows.clear()
    load_data()
    page.update()

ft.app(target=main)