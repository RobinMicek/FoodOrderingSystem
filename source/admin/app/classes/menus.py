"""
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

    Jakákoliv úprava a distribuce tohoto kódu 
    bez povolení autora je zakázána!

    © Robin Míček 2023 - 2024

********************************************************
"""

# PACKAGES IMPORTS
import os
import sys

import hashlib

# IMPORTS FROM PACKAGES

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database
from random_string import random_string
from logs import create_log

# IMPORT CONSTANT VARIABLES (/app/variables.py)


class Menu():

    def __init__(self): 
        pass

    def create_new_menu(self, data):
        try:
            # Save Image        
            if data["image"] != None:
                parent_dir =  os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

                slug = f"{random_string(length=10)}"
                url_image = f"/files/storage/images/menus/{slug}.png"

                data["image"].save(os.path.join(parent_dir, f"web{url_image}"))
            else:
                url_image = "/files/storage/images/menus/placeholder.png"


            # Create Product
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                CALL InsertMenu('{data["name"]}', '{str(data["note"])}', '{str(data["description"])}', '{url_image}', @insertedID);
            """)
            db.cursor.execute("""
                SELECT @insertedID;
            """)
            menuId = db.cursor.fetchall()[0]["@insertedID"]
            db.close()

            create_log(type="ALERT", message=f"Created new product - menuId: {menuId}")

            return menuId
        
        except Exception as e:
            create_log(type="ERROR", message=f"Could not create new menu [{e}]")


    def update_menu(self, data):

        try:
            db = Database()
            db.connect()

            # Save Image        
            if data["image"] != None:
                parent_dir =  os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
                slug = f"{random_string(length=10)}"
                url_image = f"/files/storage/images/menus/{slug}.png"
            
                data["image"].save(os.path.join(parent_dir, f"web{url_image}"))

                # Update Product
                db.cursor.execute(f"""
                    CALL UpdateMenuWithImage('{data["menuId"]}', '{data["name"]}', '{str(data["note"])}', '{str(data["description"])}', '{url_image}')
                """)
            else:
                # Update Product
                db.cursor.execute(f"""
                    CALL UpdateMenuWithoutImage('{data["menuId"]}', '{data["name"]}', '{str(data["note"])}', '{str(data["description"])}')
                """)

            db.close()

            create_log(type="ALERT", message=f"""Updated menu - MenuId: {data["menuId"]}""")

        except Exception as e:
            create_log(type="ERROR", message=f"Could not update menu [{e}]")


    def update_products(self, data):

        try:
            db = Database()
            db.connect()

            # Insert Products
            db.cursor.execute(f"""
                DELETE FROM menus_products
                WHERE menuId = '{data["menuId"]}'
            """)
            for product in data["products"]:        
                db.cursor.execute(f"""
                    INSERT INTO menus_products
                    (menuId, productId)
                    VALUES
                    ('{data["menuId"]}', '{product}')                  
                """)

            db.close()

            create_log(type="ALERT", message=f"""Updated menu's products - menuId: {data["menuId"]}""")

        except Exception as e:
            create_log(type="ERROR", message=f"Could not update menu's products [{e}]")


    def all_menus(self):
        
        db = Database()
        db.connect()
        db.cursor.execute("""
            SELECT menus.*,
            COALESCE(COUNT(menus_products.menuId), 0) AS productsCount
            FROM menus
            LEFT JOIN menus_products
            ON menus.menuId = menus_products.menuId
            GROUP BY menus.menuId;

        """)
        query = db.cursor.fetchall()
        db.close()

        return query
    

    def all_info(self, menuId):

        menu_data = self.info(menuId=menuId)
        if menu_data != []:
            menu_data["products"] = self.products(menuId=menuId)

            return menu_data
        
        return False
    

    def products(self, menuId):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT *,
            TIME_FORMAT(products.preparationTime, '%H:%i:%s') AS preparationTime
            FROM products
                          
            INNER JOIN menus_products
            ON products.productId = menus_products.productId
                          
            WHERE menus_products.menuId = "{menuId}"
        """)
        query = db.cursor.fetchall()
        db.close()

        return query
    

    def info(self, menuId):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT *
            FROM menus
            WHERE menuId = "{menuId}"
        """)
        query = db.cursor.fetchall()
        db.close()

        return query[0] if len(query) != 0 else []
    

    def update_show(self, menuId = None):

        try:
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                CALL ToggleMenuShow('{menuId}')
            """)
            db.close()

            create_log(type="ALERT", message=f"Toggled menu visibility - menuId: {menuId}")

        except Exception as e:
            create_log(type="ERROR", message=f"Could not toggle menu visibility [{e}]")

