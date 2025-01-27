import boto3
import aws_encryption_sdk
from aws_encryption_sdk import CommitmentPolicy

def encrypt_video(kms_key_id):
