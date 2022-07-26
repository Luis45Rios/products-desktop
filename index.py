from multiprocessing.sharedctypes import Value
from tkinter import ttk
from tkinter import *

import sqlite3

class Product:
    db_name = "database.db"
    
    def __init__(self, window):
        self.wind = window
        self.wind.title("Products Application")

        #Create a Frame contain 
        frame = LabelFrame(self.wind, text = ("Register a new product"))
        frame.grid(row = 0, column = 3, columnspan = 3, pady =20)



        #Name input
        Label(frame, text = "Nombre: ").grid(row = 2, column = 0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row = 2, column = 1)
        
        #Price input
        Label(frame, text = "Price: ").grid(row = 3, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 3, column = 1)

        #Cantidad Input
        Label(frame, text = "Cantidad: ").grid(row = 4, column = 0)
        self.cantidad = Entry(frame)
        self.cantidad.grid(row = 4, column = 1)


        #Create Add Botton
        ttk.Button(frame, text = "Save Product", command = self.add_product).grid(row = 5, column = 0, columnspan = 3, sticky = W + E)

        #Output Messages 
        self.message = Label(text = "", fg = "red")
        self.message.grid(row = 5, column = 3, columnspan = 2, sticky = W + E)

        #Table
        self.tree = ttk.Treeview(window, height= 10, columns = ("Nombre", "Price"))
        self.tree.grid(row = 7, column = 3, columnspan = 3)
        self.tree.heading("#0", text = "Name")
        self.tree.heading("#1", text = "Price")
        self.tree.heading("#2", text= "Cantidad")

        #Buttons
        ttk.Button(text = "Eliminar", command = self.delete_product).grid(row = 6, column = 4, sticky = W + W)


  # Filling the Rows
        self.get_products()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
        

    # Get Products from Database
    def get_products(self):
        # cleaning Table
        query = ""
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = "SELECT * FROM product ORDER BY id DESC"
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 'end', text = row[1], values =  row[2], open = [3])
            
    # User Input Validation
    def validation(self):
        return len(self.nombre.get()) != 0 and len(self.price.get()) != 0 and len(self.cantidad.get()) != 0 

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters =  (self.nombre.get(), self.price.get(), self.cantidad.get())
            self.run_query(query, parameters)
            self.message['text'] = '{} añadido'.format(self.name.get())
            self.name.delete(0, END)
            self.code.delete(0, END)
            #self.cantidad.delete(0, END)
        else:
            self.message['text'] = 'Por favor ingrese nombre, código y cantidad'
            self.get_products()

    def delete_product(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"]
        except:
            self.message["text"] = "Por favor selecciona un requisito"
            return
        self.message["text"] = ""
        name = self.tree.item(self.tree.selection())
        query = "DELETE FROM product WHERE name = ?"
        self.run_query(query, (name, ))
        self.message["text"] = "El registro {} ha sido eliminado exitosamente".format(name)

if __name__=="__main__":
    window = Tk()
    application = Product(window)
    window.mainloop()