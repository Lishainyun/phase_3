import os, boto3, botocore
from werkzeug.utils import secure_filename
from dotenv import *
from flask import jsonify

load_dotenv(".env")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def upload_file_to_s3(file):
    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            file.filename,
        )

    except Exception as error:
        print("Something Happened: ", error)
        return error
    
    return file.filename