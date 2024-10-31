import boto3
import json

s3_client = boto3.client('s3')
BUCKET_NAME = 'YOUR_BUCKET_NAME'

def lambda_handler(event, context):
    try:
        # Parse the upload ID and parts list from the request body
        body = json.loads(event['body'])
        upload_id = body['uploadId']
        parts = body['parts']

        # Complete the multipart upload
        response = s3_client.complete_multipart_upload(
            Bucket=BUCKET_NAME,
            Key='myvideo.mp4',
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"status": "Upload complete"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
