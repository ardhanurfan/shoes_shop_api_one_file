from errno import errorcode
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel 

app = FastAPI()

# Models
class Brand(BaseModel):
    name:str

class Shoes(BaseModel):
    brand_id:int
    name:str
    category:str
    stock:int

class Varian(BaseModel):
    shoes_id:int
    color:str
    virtual_url:str

# Load the stored environment variables
load_dotenv()

# Obtain connection string information from the portal
config = {
  'host': os.getenv('HOST_MYSQL'),
  'user': os.getenv('USER_MYSQL'),
  'password':os.getenv('PASSWORD_MYSQL'),
  'database':os.getenv('DATABASE_MYSQL'),
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': '/DigiCertGlobalRootG2.crt.pem'
}

# Construct connection string
try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = conn.cursor(dictionary=True)

    @app.get('/brand')
    async def read_data():
        query = "SELECT * FROM brands;"
        cursor.execute(query)
        data = cursor.fetchall()
        return {
            "code": 200,
            "messages" : "Get All Brands successfully",
            "data" : data
        }

    @app.get('/brand/{id}')
    async def read_data(id: int):
        select_query = "SELECT * FROM brands WHERE id = %s;"
        cursor.execute(select_query, (id,))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail=f"Data brand id {id} Not Found")

        return {
            "code": 200,
            "messages" : "Get Brand successfully",
            "data" : data
        }

    @app.post('/brand')
    async def write_data(brand: Brand):
        brand_json = brand.model_dump()
        query = "INSERT INTO brands(name) VALUES(%s);"
        cursor.execute(query, (brand_json["name"],))
        conn.commit()

        select_query = "SELECT * FROM brands WHERE id = LAST_INSERT_ID();"
        cursor.execute(select_query)
        new_brand = cursor.fetchone()

        return {
            "code": 200,
            "messages" : "Add Brand successfully",
            "data" : new_brand
        }
        
    @app.put('/brand/{id}')
    async def update_data(brand: Brand, id:int):
        brand_json = brand.model_dump()
        select_query = "SELECT * FROM brands WHERE id = %s;"
        cursor.execute(select_query, (id,))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail=f"Data brand id {id} Not Found")
        
        query = "UPDATE brands SET name = %s WHERE brands.id = %s;"
        cursor.execute(query, (brand_json["name"], id,))
        conn.commit()

        select_query = "SELECT * FROM brands WHERE brands.id = %s;"
        cursor.execute(select_query, (id,))
        new_brand = cursor.fetchone()
        
        return {
            "code": 200,
            "messages" : "Update Brand successfully",
            "data" : new_brand
        }

    @app.delete('/brand/{id}')
    async def delete_data(id: int):
        select_query = "SELECT * FROM brands WHERE id = %s;"
        cursor.execute(select_query, (id,))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail=f"Data brand id {id} Not Found")
        
        query = "DELETE FROM brands WHERE id = %s;"
        cursor.execute(query, (id,))
        conn.commit()
        return {
            "code": 200,
            "messages" : "Delete Brand successfully",
        }
    
    @app.get('/shoes')
    async def read_data():
        query = "SELECT * FROM shoes;"
        cursor.execute(query)
        data = cursor.fetchall()

        for i in range (0, len(data)):
            query = "SELECT * FROM varians WHERE shoes_id = %s;"
            cursor.execute(query, (data[i]["id"],))
            data_varians = cursor.fetchall()
            data[i]["varians"] = data_varians 

            query = "SELECT * FROM brands WHERE id = %s;"
            cursor.execute(query, (data[i]["brand_id"],))
            data_varians = cursor.fetchone()
            data[i]["brand"] = data_varians 

        return {
            "code": 200,
            "messages" : "Get All Shoes successfully",
            "data" : data
        }

    @app.get('/shoes/{id}')
    async def read_data(id: int):
        select_query = "SELECT * FROM shoes WHERE id = %s;"
        cursor.execute(select_query, (id,))
        data = cursor.fetchone()

        if data is None:
            raise HTTPException(status_code=404, detail=f"Data shoes id {id} Not Found")

        query = "SELECT * FROM varians WHERE shoes_id = %s;"
        cursor.execute(query, (data["id"],))
        data_varians = cursor.fetchall()
        data["varians"] = data_varians 

        query = "SELECT * FROM brands WHERE id = %s;"
        cursor.execute(query, (data["brand_id"],))
        data_varians = cursor.fetchone()
        data["brand"] = data_varians 
        
        return {
            "code": 200,
            "messages" : "Get Shoes successfully",
            "data" : data
        }

    @app.post('/shoes')
    async def write_data(shoes: Shoes):
        shoes_json = shoes.model_dump()
        select_query = "SELECT * FROM brands WHERE id = %s;"
        cursor.execute(select_query, (shoes_json["brand_id"],))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail=f"Brand id {shoes_json['brand_id']} Not Found")

        query = "INSERT INTO shoes(brand_id, name, category, stock) VALUES(%s, %s, %s, %s);"
        cursor.execute(query, (shoes_json["brand_id"], shoes_json["name"], shoes_json["category"], shoes_json["stock"],))
        conn.commit()

        select_query = "SELECT * FROM shoes WHERE id = LAST_INSERT_ID();"
        cursor.execute(select_query)
        new_shoes = cursor.fetchone()

        return {
            "code": 200,
            "messages" : "Add Shoes successfully",
            "data" : new_shoes
        }
        
    @app.put('/shoes/{id}')
    async def update_data(shoes: Shoes, id:int):
        shoes_json = shoes.model_dump()
        select_query = "SELECT * FROM shoes WHERE id = %s;"
        cursor.execute(select_query, (id,))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail=f"Data shoes id {id} Not Found")
        
        query = "UPDATE shoes SET brand_id=%s, name=%s, category=%s, stock=%s WHERE shoes.id = %s;"
        cursor.execute(query, (shoes_json["brand_id"], shoes_json["name"], shoes_json["category"], shoes_json["stock"], id,))
        conn.commit()

        select_query = "SELECT * FROM shoes WHERE shoes.id = %s;"
        cursor.execute(select_query, (id,))
        new_shoes = cursor.fetchone()
        
        return {
            "code": 200,
            "messages" : "Update Brand successfully",
            "data" : new_shoes
        }

    @app.delete('/shoes/{id}')
    async def delete_data(id: int):
        select_query = "SELECT * FROM shoes WHERE id = %s;"
        cursor.execute(select_query, (id,))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail=f"Data shoes id {id} Not Found")
        
        query = "DELETE FROM shoes WHERE id = %s;"
        cursor.execute(query, (id,))
        conn.commit()
        return {
            "code": 200,
            "messages" : "Delete Shoes successfully",
        }
    
    @app.get('/varian')
    async def read_data():
        query = "SELECT * FROM varians;"
        cursor.execute(query)
        data = cursor.fetchall()
        return {
            "code": 200,
            "messages" : "Get All Varians successfully",
            "data" : data
        }

    @app.get('/varian/{id}')
    async def read_data(id: int):
        select_query = "SELECT * FROM varians WHERE id = %s;"
        cursor.execute(select_query, (id,))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail=f"Data varian id {id} Not Found")

        return {
            "code": 200,
            "messages" : "Get Varian successfully",
            "data" : data
        }

    @app.post('/varian')
    async def write_data(varian: Varian):
        varian_json = varian.model_dump()
        select_query = "SELECT * FROM shoes WHERE id = %s;"
        cursor.execute(select_query, (varian_json["shoes_id"],))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail=f"Shoes id {varian_json['shoes_id']} Not Found")
        
        query = "INSERT INTO varians(shoes_id, virtual_url, color) VALUES(%s, %s, %s);"
        cursor.execute(query, (varian_json["shoes_id"], varian_json['virtual_url'], varian_json['color'],))
        conn.commit()

        select_query = "SELECT * FROM varians WHERE id = LAST_INSERT_ID();"
        cursor.execute(select_query)
        new_varian = cursor.fetchone()

        return {
            "code": 200,
            "messages" : "Add Varian successfully",
            "data" : new_varian
        }
        
    @app.put('/varian/{id}')
    async def update_data(varian: Varian, id:int):
        varian_json = varian.model_dump()
        select_query = "SELECT * FROM varians WHERE id = %s;"
        cursor.execute(select_query, (id,))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail=f"Data varian id {id} Not Found")
        
        query = "UPDATE varians SET shoes_id=%s, virtual_url=%s, color=%s WHERE varians.id = %s;"
        cursor.execute(query, (varian_json["shoes_id"], varian_json['virtual_url'], varian_json['color'], id,))
        conn.commit()

        select_query = "SELECT * FROM varians WHERE varians.id = %s;"
        cursor.execute(select_query, (id,))
        new_varian = cursor.fetchone()
        
        return {
            "code": 200,
            "messages" : "Update Varian successfully",
            "data" : new_varian
        }

    @app.delete('/varian/{id}')
    async def delete_data(id: int):
        select_query = "SELECT * FROM varians WHERE id = %s;"
        cursor.execute(select_query, (id,))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail=f"Data varian id {id} Not Found")
        
        query = "DELETE FROM varians WHERE id = %s;"
        cursor.execute(query, (id,))
        conn.commit()
        return {
            "code": 200,
            "messages" : "Delete Varian successfully",
        }
