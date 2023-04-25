from google.cloud import secretmanager

class GCPSecretAuth:
    def __init__(self, secret_id, project_id):
        self.project_id = project_id
        self.secret_id = secret_id

    def get_secret(self, version_id="latest"):
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret version.
        name = f"projects/{self.project_id}/secrets/{self.secret_id}/versions/{version_id}"

        # Access the secret version.
        response = client.access_secret_version(name=name)

        # Return the decoded payload.
        return response.payload.data.decode('UTF-8')