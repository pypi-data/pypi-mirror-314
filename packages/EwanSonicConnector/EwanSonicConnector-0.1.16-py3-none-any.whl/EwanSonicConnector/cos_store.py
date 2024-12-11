import hashlib
import json
import os
import time
import uuid

import requests
from qcloud_cos import CosConfig, CosS3Client


class CosBucket:
    def __init__(self, secret_id, secret_key, region, bucket_name, token=None):
        self.bucket_name = bucket_name
        self.config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
        self.client = CosS3Client(self.config)

    def bucket_upload(self, file_path, key):
        try:
            # 检查 Key 是否已存在
            existing_keys = self.list_all_keys().get('keys', [])
            if key in existing_keys:
                return {"msg": "error", "code": 1, "error": "Key already exists"}

            # 上传文件
            response = self.client.upload_file(
                Bucket=self.bucket_name,
                LocalFilePath=file_path,
                Key=key,
                PartSize=10,
                MAXThread=10,
                EnableMD5=False
            )
            return {"msg": "success", "code": 0, "ETag": response['ETag']}
        except Exception as e:
            raise e

    def generate_download_url(self, key):
        try:
            url = self.client.get_presigned_url(
                Bucket=self.bucket_name,
                Key=key,
                Method='GET',
                Expired=int(time.time()) + 3600 * 24 * 31
            )
            return {"msg": "success", "code": 0, "url": url}
        except Exception as e:
            raise e

    def list_all_keys(self):
        try:
            keys = []
            response = self.client.list_objects(
                Bucket=self.bucket_name,
                MaxKeys=100
            )
            for content in response.get('Contents', []):
                keys.append(content['Key'])

            while 'NextMarker' in response:
                response = self.client.list_objects(
                    Bucket=self.bucket_name,
                    Marker=response['NextMarker'],
                    MaxKeys=100
                )
                for content in response.get('Contents', []):
                    keys.append(content['Key'])

            return {"msg": "success", "code": 0, "keys": keys}
        except Exception as e:
            raise e

    def upload_directory(self, dir_path, uuid, prefix=''):
        keys = {}
        try:
            for root, _, files in os.walk(dir_path):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_file_path, dir_path)
                    key = os.path.join(prefix, uuid, relative_path).replace("\\", "/")
                    print(f"Uploading {local_file_path} to {key}")
                    result = self.bucket_upload(local_file_path, key)
                    keys[key.split(".")[-1]] = key
                    print(result)

            return keys
        except Exception as e:
            print(f"Error uploading directory: {e}")

    def send_feishu_card(self, url, payload, secret_key):
        try:
            payload_json = json.dumps(payload, sort_keys=True)

            timestamp = str(int(time.time()))

            raw_string = payload_json + timestamp + secret_key
            signature = hashlib.md5(raw_string.encode('utf-8')).hexdigest()

            headers = {
                'Content-Type': 'application/json',
                'X-SIGNATURE': signature,
                'X-TIMESTAMP': timestamp,
                'Cookie': 'csrftoken=GO4Plb5CECvbtXJrPmSCNqsXiyswMnH2nYtuM2t2vED5Oa7Ivpn0PuzhFkVb2FKY'
            }

            response = requests.post(url, headers=headers, data=payload_json)

            return response.json()
        except Exception as e:
            raise e
