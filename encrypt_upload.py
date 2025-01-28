import boto3
import aws_encryption_sdk
from aws_encryption_sdk.identifiers import CommitmentPolicy
from aws_encryption_sdk.streaming_client import StreamEncryptor
from aws_cryptographic_material_providers.mpl.models import CreateAwsKmsKeyringInput
from config import S3_BUCKET, KMS_KEY_ARN

s3_client = boto3.client('s3')
kms_key_provider = KMSMasterKeyProvider(key_ids=[KMS_KEY_ARN])

def encrypt_and_upload(file_path, s3_key):
    try:
        with open(file_path, "rb") as infile:
            encryptor = StreamEncryptor(
                source=infile,
                key_provider=kms_key_provider,
                commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT
            )

            encrypted_chunks = bytearray()
            for chunk in encryptor:
                encrypted_chunks.extend(chunk)

        s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=bytes(encrypted_chunks))
        print(f"File uploaded and encrypted successfully: {s3_key}")

    except Exception as e:
        print(f"Error: {str(e)}")

