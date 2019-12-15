import sys
#import StringIO
import unittest

import boto3
import botocore
from moto import mock_s3

from listS3Contents.index import listObjects


class TestS3List(unittest.TestCase):
    def setUp(self):

        self.bucket1 = 'unencryptedBucket'
        self.key1 = 'unencryptedKey'
        self.value1= 'value1'
        self.bucket2 = 'encryptedBucket'
        self.key2 = 'encryptedKey'
        self.value2 = 'value2'

    @mock_s3
    def __moto_setup(self):

        s3 = boto3.client('s3')
        s3.create_bucket(Bucket=self.bucket1)
        s3.create_bucket(Bucket=self.bucket2)

        s3.put_object(Bucket=self.bucket1, Key=self.key1, Body=self.value1)
        s3.put_object(Bucket=self.bucket2, Key=self.key2, Body=self.value2)

    @mock_s3
    def test_listObjects(self):

        self.__moto_setup()
        bucketParams = {
            "Bucket": self.bucket1,
            "Encryption": None
        }
        contents = listObjects(bucketParams)
        objects = []
        for o in contents['Objects']:
            objects.append(o['Key'])
        result = False
        for key in objects:
            if key == self.key1:
                result = True
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
