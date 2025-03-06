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
import boto3.s3

from config import KMS_KEY_ARN
S3_BUCKET = 'weaponwatch-demo'
s3_client = boto3.client('s3') 
def download_and_decrypt(s3_key, output_path):

    # Initialize AWS Encryption SDK client with required policy
    client = aws_encryption_sdk.EncryptionSDKClient(
        commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT
    )

    # Create KMS client for key decryption
    kms_client = boto3.client('kms', region_name="us-east-1")

    # Configure cryptographic material providers
    mat_prov: AwsCryptographicMaterialProviders = AwsCryptographicMaterialProviders(
        config=MaterialProvidersConfig()
    )

    # Create AWS KMS keyring for decryption
    keyring_input: CreateAwsKmsKeyringInput = CreateAwsKmsKeyringInput(
        kms_key_id=KMS_KEY_ARN,
        kms_client=kms_client
    )
    kms_keyring: IKeyring = mat_prov.create_aws_kms_keyring(
        input=keyring_input
    )

    try:
        # Retrieve encrypted object from S3
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
        ciphertext = response['Body'].read()

        # Decrypt and write to the output file
        with open(output_path, "wb") as outfile:
            plaintext_bytes, _ = client.decrypt(
                source=ciphertext,
                keyring=kms_keyring,
            )
            outfile.write(plaintext_bytes)
            print(f"Successfully decrypted {s3_key} and downloaded to {output_path}")
    except Exception as e:
        print(e)  # Print error if decryption or download fails