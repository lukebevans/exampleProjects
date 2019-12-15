import json
import boto3
from boto3 import client
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
conn = client('s3')

# return a list of all unencrypted objects in an S3 bucket
def listObjects(bucketContents):
    bucketObjects = []
    # list all objects within the current bucket
    listBucketObjects = conn.list_objects(Bucket=bucketContents["Bucket"])['Contents']
    for object in listBucketObjects:
        key = s3.Object(bucketContents["Bucket"], object['Key'])
        # if object is not encrypted add to the response payload
        if key.server_side_encryption == None:
            obj = {
                "Key": object['Key'],
            }
            bucketObjects.append(obj)
    bucketContents["Objects"] = bucketObjects
    return bucketContents


# list all S3 buckets and their encryption type + call the listObjects function for each bucket
def listS3Buckets():
    s3Contents = {}
    listOfBuckets = []

    for bucket in s3.buckets.all():
        encryptionType = ""
        # get the encryption type applied to the bucket
        try:
            bucketEncryption = conn.get_bucket_encryption(Bucket=bucket.name)
            encryptionType = bucketEncryption['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                encryptionType = None
        bucketContentParams = {
            "Bucket": bucket.name,
            "Encryption": encryptionType
        }
        # retrieve bucket contents
        bucketContents = listObjects(bucketContentParams)
        listOfBuckets.append(bucketContents)
    # append bucket and contents to the response object
    s3Contents["Buckets"] = listOfBuckets
    print("Buckets: ", json.dumps(s3Contents) )
    return s3Contents

# main function - return result as json to the invoking API
def lambda_handler(event, context):
    # TODO implement
    s3Contents = listS3Buckets()
    return {
        'statusCode': 200,
        'body': json.dumps(s3Contents)
    }
