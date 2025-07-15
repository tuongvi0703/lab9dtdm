from flask import Flask, request, redirect
import boto3
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            s3.upload_fileobj(file, BUCKET_NAME, filename)
            return f"Đã upload file {filename} lên S3!"
    return '''
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" />
            <input type="submit" />
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
