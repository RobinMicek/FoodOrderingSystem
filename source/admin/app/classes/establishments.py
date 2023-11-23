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
import re 

# IMPORTS FROM PACKAGES
from datetime import datetime, time

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.stats import Stats

from database.handle_database import Database
from random_string import random_string
from logs import create_log

# IMPORT CONSTANT VARIABLES (/app/variables.py)


class Establishment():

    def __init__(self):
        pass


    def create_new_establishment(self, data):

        try:
            # Save Image        
            if data["image"] != None:
                parent_dir =  os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

                slug = f"{random_string(length=10)}"
                url_image = f"/files/storage/images/establishments/{slug}.png"

                data["image"].save(os.path.join(parent_dir, f"web{url_image}"))
            else:
                url_image = "/files/storage/images/establishments/placeholder.png"


            # Generate slug and token - for KitchenHub auth
            regex_pattern = r'[^a-zA-Z0-9]'

            slug = f"{re.sub(regex_pattern, '', data['name'])}-{random_string(length=10)}"
            token = f"EST-{re.sub(regex_pattern, '', data['name'])[0:4]}-{random_string(length=4)}-{random_string(length=4)}-{random_string(length=4)}-{random_string(length=4)}"


            # Create Establishment
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                CALL InsertEstablishment('{data["name"]}', '{url_image}', '{data["address"]}', '{data["wifi"]}', '{data["dineIn"]}', '{data["yard"]}', '{data["playground"]}', '{data["parking"]}', '{data["eCharger"]}', '{slug}', '{token}', @insertedID);
            """)
            db.cursor.execute("""
                SELECT @insertedID;
            """)
            establishmentId = db.cursor.fetchall()[0]["@insertedID"]


            # Insert Opening Hours
            for day in range(1, 8):        
                db.cursor.execute(f"""
                    INSERT INTO establishments_openinghours
                    (establishmentId, dayOfTheWeek, openingTime, closingTime)
                    VALUES
                    ('{establishmentId}', '{day}', '{data[f"open_day_{day}"]}', '{data[f"close_day_{day}"]}')                  
                """)


            # Insert Menus
            for menu in data["menus"]:
                db.cursor.execute(f"""
                    INSERT INTO establishments_menus
                    (establishmentId, menuId)
                    VALUES
                    ('{establishmentId}', '{menu}')
                """)

            db.close()

            create_log(type="ALERT", message=f"Created new establishment - establishmentId: {establishmentId}")

            return establishmentId
        
        except Exception as e:
            create_log(type="ERROR", message=f"Could not create new establishment [{e}]")
    

    def update_establishment(self, data):

        try:
            db = Database()
            db.connect()

            # Save Image        
            if data["image"] != None:
                parent_dir =  os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
                slug = f"{random_string(length=10)}"
                url_image = f"/files/storage/images/establishments/{slug}.png"
            
                data["image"].save(os.path.join(parent_dir, f"web{url_image}"))

                # Update Establishment
                db.cursor.execute(f"""
                    CALL UpdateEstablishmentWithImage('{data["establishmentId"]}', '{data["name"]}', '{url_image}', '{data["address"]}', '{data["wifi"]}', '{data["dineIn"]}', '{data["yard"]}', '{data["playground"]}', '{data["parking"]}', '{data["eCharger"]}')
                """)
            else:
                # Update Establishment
                db.cursor.execute(f"""
                    CALL UpdateEstablishmentWithoutImage('{data["establishmentId"]}', '{data["name"]}', '{data["address"]}', '{data["wifi"]}', '{data["dineIn"]}', '{data["yard"]}', '{data["playground"]}', '{data["parking"]}', '{data["eCharger"]}')
                """)

            


            # Insert Opening Hours
            db.cursor.execute(f"""
                DELETE FROM establishments_openinghours
                WHERE establishmentId = '{data["establishmentId"]}'
            """)
            for day in range(1, 8):        
                db.cursor.execute(f"""
                    INSERT INTO establishments_openinghours
                    (establishmentId, dayOfTheWeek, openingTime, closingTime)
                    VALUES
                    ('{data["establishmentId"]}', '{day}', '{data[f"open_day_{day}"]}', '{data[f"close_day_{day}"]}')                  
                """)


            # Insert Menus
            db.cursor.execute(f"""
                DELETE FROM establishments_menus
                WHERE establishmentId = '{data["establishmentId"]}'
            """)
            for menu in data["menus"]:
                db.cursor.execute(f"""
                    INSERT INTO establishments_menus
                    (establishmentId, menuId)
                    VALUES
                    ('{data["establishmentId"]}', '{menu}')
                """)

            db.close()

            create_log(type="ALERT", message=f"""Updated establishment - establishmentId: {data["establishmentId"]}""")

        except Exception as e:
            create_log(type="ERROR", message=f"Could not update establishment [{e}]")


    def update_show(self, establishmentId = None):

        try:
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                CALL ToggleEstablishmentShow('{establishmentId}')
            """)
            db.close()

            create_log(type="ALERT", message=f"Toggled establishment visibility - establishmentId: {establishmentId}")

        except Exception as e:
            create_log(type="ERROR", message=f"Could not toggle establishment visibility [{e}]")
        

    def all_info(self, establishmentId = None):

        establishment_data = self.info(establishmentId=establishmentId)
        if establishment_data != []:
            establishment_data["menus"] = self.menus(establishmentId=establishmentId)
            establishment_data["openingHours"] = self.opening_hours(establishmentId=establishmentId)
            establishment_data["isOpen"] = self.is_open(establishmentId=establishmentId)

            return establishment_data
        
        return False


    def all_establishments(self):

        db = Database()
        db.connect()
        db.cursor.execute("""
            SELECT
                establishmentId,
                name,
                imagePath,
                address,
                wifi,
                dineIn,
                yard,
                playground,
                parking,
                eCharger,
                `show`
            FROM establishments
            ORDER BY establishmentId DESC
        """)
        query = db.cursor.fetchall()
        db.close()

        return query
    

    def info(self, establishmentId = None):
        
        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT *
            FROM establishments
            WHERE establishmentId = '{establishmentId}'
        """)
        query = db.cursor.fetchall()
        db.close()

        return query[0] if len(query) != 0 else []
    

    def opening_hours(self, establishmentId = None):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
            dayOfTheWeek,
            TIME_FORMAT(openingTime, '%H:%i') AS openingTime,
            TIME_FORMAT(closingTime, '%H:%i') AS closingTime
            FROM establishments_openinghours
            WHERE establishmentId = '{establishmentId}'
        """)
        query = db.cursor.fetchall()
        db.close()


        return query
    
    
    def is_open(self, establishmentId = None):

        if self.info(establishmentId=establishmentId)["show"] == 1:
            current_datetime = datetime.now()
            current_day = (current_datetime.weekday() + 1) % 7 if (current_datetime.weekday() + 1) % 7 != 0 else 7  # Start week with monday
            current_time = current_datetime.time()
            
            opening_hours = self.opening_hours(establishmentId=establishmentId)
            

            for entry in opening_hours:
                if entry["dayOfTheWeek"] == current_day:
                    opening_time = datetime.strptime(entry["openingTime"], "%H:%M").time()
                    closing_time = datetime.strptime(entry["closingTime"], "%H:%M").time()
                    
                    is_open = False
                    if opening_time <= current_time < closing_time:
                        is_open = True
                    
                    return {
                        "isOpen": is_open,
                        "openingTime": entry["openingTime"],
                        "closingTime": entry["closingTime"]
                    }
        
        return {
                "isOpen": False,
                "openingTime": None,
                "closingTime": None
            }
    

    def menus(self, establishmentId = None):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT *
            FROM establishments_menus
            INNER JOIN menus
            ON establishments_menus.menuId = menus.menuId
            WHERE establishmentId = '{establishmentId}'
        """)
        query = db.cursor.fetchall()
        db.close()

        return query
    

    def auth(self, slug = None, token = None):

        db = Database()
        db.connect()

        db.cursor.execute(f"CALL AuthEstablishmentToken('{slug}', '{token}', @establishmentId)")
        db.cursor.execute(f"SELECT @establishmentId")
        query = db.cursor.fetchall()
        
        db.close()

        return query[0]["@establishmentId"] if query[0]["@establishmentId"] != None else False


    def revenue(self, establishmentId = None, timeWindow = "today"):

        timeWindow = str(timeWindow).upper() if timeWindow != "today" else "DATE"

        db = Database()
        db.connect()

        if timeWindow != "ALLTIME":
            db.cursor.execute(f"""
                SELECT 
                    ROUND(SUM(orders_products.quantity * orders_products.price), 2) AS revenue
                FROM
                    orders_products
                LEFT JOIN 
                    orders
                    ON orders.orderId = orders_products.orderId 
                LEFT JOIN 
                    establishments
                    ON establishments.establishmentId = orders.establishmentId 
                WHERE 
                    establishments.establishmentId = { establishmentId } AND
                    { timeWindow }(orders.createdTime) = { timeWindow }(CURDATE())  
                    AND orders.status != "CANCELED"
                GROUP BY 
                    establishments.establishmentId 
            """)
            query = db.cursor.fetchall()

        else: 
            db.cursor.execute(f"""
                SELECT 
                    ROUND(SUM(orders_products.quantity * orders_products.price), 2) AS revenue
                FROM
                    orders_products
                LEFT JOIN 
                    orders
                    ON orders.orderId = orders_products.orderId 
                LEFT JOIN 
                    establishments
                    ON establishments.establishmentId = orders.establishmentId 
                WHERE 
                    establishments.establishmentId = { establishmentId } 
                    AND orders.status != "CANCELED"
                GROUP BY 
                    establishments.establishmentId 
            """)
            query = db.cursor.fetchall()

        db.close()

        return query[0]["revenue"] if len(query) != 0 else None


    def number_of_orders(self, establishmentId = None, timeWindow = "today"): # timeWindow = today, week, month, year, allTime

        timeWindow = str(timeWindow).upper() if timeWindow != "today" else "DATE"

        db = Database()
        db.connect()

        if timeWindow != "ALLTIME":
            db.cursor.execute(f"""
                SELECT 
                    COUNT(orders.orderId) AS orders
                FROM
                    orders 
                LEFT JOIN 
                    establishments
                    ON establishments.establishmentId = orders.establishmentId 
                WHERE 
                    establishments.establishmentId = { establishmentId } AND
                    { timeWindow }(orders.createdTime) = { timeWindow }(CURDATE()) 
                    AND orders.status != "CANCELED" 
                GROUP BY 
                    establishments.establishmentId 
            """)
            query = db.cursor.fetchall()

        else: 
            db.cursor.execute(f"""
                SELECT 
                    COUNT(orders.orderId) AS orders
                FROM
                    orders 
                LEFT JOIN 
                    establishments
                    ON establishments.establishmentId = orders.establishmentId 
                WHERE 
                    establishments.establishmentId = { establishmentId }
                    AND orders.status != "CANCELED"
                GROUP BY 
                    establishments.establishmentId 
            """)
            query = db.cursor.fetchall()
        
        db.close()

        return query[0]["orders"] if len(query) != 0 else None
    

    def revenue_per_day(self, establishmentId = None):

        db = Database()
        db.connect()
        db.cursor.execute(f"""                
            SELECT
                DATE_FORMAT(DATE(orders.createdTime), '%d. %m. %y') AS orderDate,
                DATE_FORMAT(DATE(orders.createdTime), '%Y-%m-%d') AS sortableDate,
                SUM(products.price * orders_products.quantity) AS totalRevenue
            FROM
                orders
            JOIN
                orders_products ON orders.orderId = orders_products.orderId
            JOIN
                products ON orders_products.productId = products.productId
            WHERE
                establishmentId = "{ establishmentId }"
                AND orders.status != "CANCELED"
            GROUP BY
                orderDate, sortableDate
            ORDER BY
                sortableDate ASC
        """)
        query = db.cursor.fetchall()
        db.close()

        return Stats().transform_data(input_data=query)
    

    def orders_per_day(self, establishmentId = None):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
                DATE_FORMAT(DATE(orders.createdTime), '%d. %m. %y') AS orderDate,
                DATE_FORMAT(DATE(orders.createdTime), '%Y-%m-%d') AS sortableDate,
                COUNT(orderId) AS totalOrders
            FROM
                orders
            WHERE
                establishmentId = "{ establishmentId }"
                AND orders.status != "CANCELED"
            GROUP BY
                orderDate, sortableDate
            ORDER BY
                sortableDate ASC
        """)
        query = db.cursor.fetchall()
        db.close()

        return Stats().transform_data(input_data=query)

        
