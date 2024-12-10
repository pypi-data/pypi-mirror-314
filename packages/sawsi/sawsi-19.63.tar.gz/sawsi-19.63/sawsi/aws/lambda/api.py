from sawsi.aws import shared
import boto3
import boto3.exceptions


class LambdaAPI:
    """
    S3 를 활용하는 커스텀 ORM 클래스
    """
    def __init__(self, credentials=None, region=shared.DEFAULT_REGION):
        """
        :param credentials: {
            "aws_access_key_id": "str",
            "aws_secret_access_key": "str",
            "region_name": "str",
            "profile_name": "str",
        }
        """
        self.boto3_session = shared.get_boto_session(credentials)
        self.cache = {}
        self.client = boto3.client('lambda', region_name=region)
        self.region = region

    def update_lambda_code(self, function_name, s3_bucket, s3_key, publish=False, memory_size=None, timeout=None):
        """
        Updates the code of an existing Lambda function with optional configuration changes.

        :param function_name: Name of the Lambda function to update.
        :param s3_bucket: S3 bucket where the updated Lambda code is stored.
        :param s3_key: Key of the S3 object containing the updated Lambda code.
        :param publish: Whether to publish a new version of the function.
        :param memory_size: (Optional) Memory size for the Lambda function in MB.
        :param timeout: (Optional) Timeout for the Lambda function in seconds.
        :return: Response from the Lambda update_function_code and/or update_function_configuration API calls.
        """
        try:
            # Update function code
            code_response = self.client.update_function_code(
                FunctionName=function_name,
                S3Bucket=s3_bucket,
                S3Key=s3_key,
                Publish=publish
            )
            print("Function code updated successfully.")

            # Update function configuration if memory_size or timeout is provided
            if memory_size or timeout:
                config_params = {}
                if memory_size:
                    config_params['MemorySize'] = memory_size
                if timeout:
                    config_params['Timeout'] = timeout

                config_response = self.client.update_function_configuration(
                    FunctionName=function_name,
                    **config_params
                )
                print("Function configuration updated successfully.")
                return {
                    "CodeUpdateResponse": code_response,
                    "ConfigUpdateResponse": config_response
                }

            return {"CodeUpdateResponse": code_response}

        except boto3.exceptions.Boto3Error as e:
            print(f"Error updating Lambda function: {e}")
            raise


    def create_lambda_function(self, function_name, role_arn, s3_bucket, s3_key, handler, runtime="python3.13"):
        """
        Creates a new AWS Lambda function.

        :param function_name: Name of the new Lambda function.
        :param role_arn: ARN of the IAM role for the function.
        :param s3_bucket: S3 bucket containing the function code.
        :param s3_key: Key of the S3 object with the code.
        :param handler: Function handler (e.g., "app.handler").
        :param runtime: Runtime environment (default: "python3.9").
        :return: Response from the create_function API call.
        """
        try:
            response = self.client.create_function(
                FunctionName=function_name,
                Runtime=runtime,
                Role=role_arn,
                Handler=handler,
                Code={
                    'S3Bucket': s3_bucket,
                    'S3Key': s3_key
                },
                Publish=True
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            print(f"Error creating Lambda function: {e}")
            raise


    def delete_lambda_function(self, function_name):
        """
        Deletes an existing AWS Lambda function.

        :param function_name: Name of the Lambda function to delete.
        :return: Response from the delete_function API call.
        """
        try:
            response = self.client.delete_function(FunctionName=function_name)
            return response
        except boto3.exceptions.Boto3Error as e:
            print(f"Error deleting Lambda function: {e}")
            raise

    def get_lambda_function_info(self, function_name):
        """
        Retrieves information about an existing AWS Lambda function.

        :param function_name: Name of the Lambda function.
        :return: Response from the get_function API call.
        """
        try:
            response = self.client.get_function(FunctionName=function_name)
            return response
        except boto3.exceptions.Boto3Error as e:
            print(f"Error retrieving Lambda function info: {e}")
            raise

    def update_lambda_environment_variables(self, function_name, environment_variables):
        """
        Updates the environment variables of a Lambda function.

        :param function_name: Name of the Lambda function.
        :param environment_variables: Dictionary of environment variables to update.
        :return: Response from the update_function_configuration API call.
        """
        try:
            response = self.client.update_function_configuration(
                FunctionName=function_name,
                Environment={
                    'Variables': environment_variables
                }
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            print(f"Error updating Lambda environment variables: {e}")
            raise