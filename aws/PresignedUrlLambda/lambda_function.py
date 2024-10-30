import boto3
import os

s3_client = boto3.client('s3')
bucket_name = os.environ.get('BUCKET_NAME', 'your-s3-bucket-name')

def handler(event, context):
    # Safely extract file_name and chunk_id from the query parameters
    query_params = event.get('queryStringParameters') or {}
    file_name = query_params.get('file_name', 'default_video.mp4')
    chunk_id = query_params.get('chunk_id', '1')
    
    # Define the S3 object key, e.g., 'uploads/default_video_chunk_1'
    object_key = f"uploads/{file_name}_chunk_{chunk_id}"
    
    # Generate the pre-signed URL
    try:
        upload_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=3600  # URL expires in 1 hour
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Failed to generate presigned URL: {str(e)}"
        }

    # Return the presigned URL to the client
    return {
        "statusCode": 200,
        "upload_url": upload_url,
        "object_key": object_key
    }
