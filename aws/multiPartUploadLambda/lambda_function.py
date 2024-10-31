import boto3
import json

s3_client = boto3.client('s3')
BUCKET_NAME = 'YOUR_BUCKET_NAME'

def lambda_handler(event, context):
    try:
        response = s3_client.create_multipart_upload(Bucket=BUCKET_NAME, Key='myvideo.mp4')
        upload_id = response['UploadId']
        return {
            "statusCode": 200,
            "body": json.dumps({"uploadId": upload_id})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
