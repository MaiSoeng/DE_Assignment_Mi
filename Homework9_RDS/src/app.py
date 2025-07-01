import json
import os
import boto3
import pymysql
from pymysql.cursors import DictCursor
import logging
import sys

# RDS settings
proxy_host_name = os.environ['DB_Host']
db_name = os.environ['DB_Name']
db_user_name = os.environ['DB_User']
db_password = os.environ['DB_Password']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# connect to the rds database that has already been created
try:
    connection = pymysql.connect(
        host=proxy_host_name,
        user=db_user_name,
        password=db_password,
        db=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            age INT)       
            """)
        connection.commit()

except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)

logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")


def lambda_handler(event, context):
    action  = event.get("action")
    payload = event.get("payload", {})

    # After connecting with the database, check the events and perform the actions accordingly
    try:
        with connection.cursor() as cursor:
            if action == "insert":
                name = payload.get("name")
                age  = payload.get("age")
                cursor.execute(
                    "INSERT INTO users (name, age) VALUES (%s, %s)",
                    (name, age)
                )
                connection.commit()
                result = {"message": "Insert Successful"}

            elif action == "read":
                cursor.execute("SELECT * FROM users")
                rows = cursor.fetchall()
                result = {"users": rows}

            elif action == "update":
                user_id = payload.get("id")
                name = payload.get("name")
                age = payload.get("age")
                cursor.execute(
                    "UPDATE users SET name=%s, age=%s WHERE id=%s",
                    (name, age, user_id)
                )
                connection.commit()
                result = {"message": "Update Successful"}

            elif action == "delete":
                user_id = payload.get("id")
                cursor.execute(
                    "DELETE FROM users WHERE id=%s",
                    (user_id,)
                )
                connection.commit()
                result = {"message": "Delete Successful"}

            else:
                result = {"error": f"Unsupported action '{action}'."}

        # connection.close()
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

