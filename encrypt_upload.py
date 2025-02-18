import boto3
import aws_encryption_sdk
import aws_encryption_sdk.key_providers.kms
from aws_encryption_sdk.identifiers import CommitmentPolicy
from aws_encryption_sdk.streaming_client import StreamEncryptor
from aws_cryptographic_material_providers.mpl.models import CreateAwsKmsKeyringInput
from aws_cryptographic_material_providers.mpl import AwsCryptographicMaterialProviders
from aws_cryptographic_material_providers.mpl.config import MaterialProvidersConfig
from aws_cryptographic_material_providers.mpl.models import CreateAwsKmsKeyringInput
from aws_cryptographic_material_providers.mpl.references import IKeyring
from config import KMS_KEY_ARN
S3_BUCKET = 'weaponwatch-demo'
s3_client = boto3.client('s3')

def encrypt_and_upload(file_path, s3_key):
    client = aws_encryption_sdk.EncryptionSDKClient(
        commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT
    )
    kms_client = boto3.client('kms', region_name="us-east-1")
    mat_prov: AwsCryptographicMaterialProviders = AwsCryptographicMaterialProviders(
        config=MaterialProvidersConfig()
    )

    keyring_input: CreateAwsKmsKeyringInput = CreateAwsKmsKeyringInput(
        kms_key_id=KMS_KEY_ARN,
        kms_client=kms_client
    )
    kms_keyring: IKeyring = mat_prov.create_aws_kms_keyring(
        input=keyring_input
    )
    try:
        with open(file_path, "rb") as infile:
            ciphertext, _ = client.encrypt(
            source=infile,
            keyring=kms_keyring,
            )

        s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=bytes(ciphertext))
        print(f"File uploaded and encrypted successfully: {s3_key}")

    except Exception as e:
        print(f"Error: {str(e)}")

