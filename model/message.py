import os, mysql.connector
import sqlalchemy.pool as pool
from dotenv import *
from flask import jsonify
from datetime import *

load_dotenv(".env")

def getconn():
	
	c = mysql.connector.connect(
            
        host="database-1.clmepehxmhif.us-east-1.rds.amazonaws.com",
        user=os.getenv('MYSQL_USERNAME'),
        password=os.getenv('MYSQL_PASSWORD'),
        database="phase_3"

    )
	return c

mypool = pool.QueuePool(getconn, max_overflow=10, pool_size=5)

class MessageModel:
    def add_message(text,filename):
        time = datetime.now()
        try:
            conn = mypool.connect()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO message(time, text, image)
                VALUES (%s, %s, %s)
                """,(time, text, filename,)
            )
            return jsonify({
                "result":{
                    "time":time,
                    "text":text,
                    "image":filename
                }}), 200
        except:
            return jsonify({
                "error":True,
                "message":"上傳失敗"}), 400
        finally:
            conn.commit()
            cursor.close()
            conn.close()
    
    def get_message():
        try:
            conn = mypool.connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT time, text, image 
                FROM message
                ORDER BY time ASC
                LIMIT 10 
                OFFSET 0
                """
            )
            result = cursor.fetchall()
            
            return jsonify({"result":result})
        except:
            return jsonify({
                "error":True,
                "message":"獲取失敗"}), 400
        finally:
            cursor.close()
            conn.close()  