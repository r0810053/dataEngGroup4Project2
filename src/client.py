from minio import Minio

url = "play.min.io"
access_key = "minioadmin"
secret_key = "minioadmin"

client = Minio(url, 
               access_key=access_key, 
               secret_key=secret_key)

print("Created Minio client!")