import boto3
import base64
import json
import uuid
from botocore.exceptions import ClientError
from datetime import datetime


class AWSSecretAuth:
    def __init__(self, config: dict):
        self.region_name = config["REGION_NAME"]
        self.secret_name = config["SECRET_NAME"]

    def get_secret(self) -> dict:
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager", region_name=self.region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "DecryptionFailureException":
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InternalServiceErrorException":
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InvalidRequestException":
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "ResourceNotFoundException":
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if "SecretString" in get_secret_value_response:
                secret = get_secret_value_response["SecretString"]
                credentials = json.loads(secret)
                return credentials
            else:
                decoded_binary_secret = base64.b64decode(
                    get_secret_value_response["SecretBinary"]
                )
                return decoded_binary_secret


class S3Export:
    def write_to_s3(aws_key: str, aws_secret: str, env: str, config: dict, data):
        """
        Writes data to AWS S3 bucket
        """
        # Create Client
        client = boto3.client(
            "s3", aws_access_key_id=aws_key, aws_secret_access_key=aws_secret
        )
        # Specify S3 bucket
        bucket = f"{config['S3_BUCKET']}-{env}"
        # Create filename
        ingestion_date = datetime.utcnow().strftime("%Y-%m-%d/%H-%M-%S")
        file_destination = f"{config['S3_PATH']}/{ingestion_date}/" + str(uuid.uuid4())
        # Write to Bucket
        client.put_object(data, Bucket=bucket, Key=file_destination)
        print(f"{file_destination} was copied to AWS S3")
