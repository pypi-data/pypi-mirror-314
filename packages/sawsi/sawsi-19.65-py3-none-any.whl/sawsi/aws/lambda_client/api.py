from sawsi.aws import shared
import boto3
import boto3.exceptions
from typing import Any


class LambdaAPI:
    def __init__(self, credentials=None, region=shared.DEFAULT_REGION):
        self.boto3_session = shared.get_boto_session(credentials)
        self.lambda_client = self.boto3_session.client('lambda', region_name=region)

    def invoke(self, function_name: str, payload: Any):
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # 'Event' for asynchronous execution
            Payload=payload
        )

        # 응답에서 Payload 추출
        response_payload = response['Payload'].read()
        response_body = response_payload.decode('utf-8')
        return response_body

    def create_event_source_mapping(
            self, function_name: str, event_source_arn: str,
            enabled: bool = True, batch_size: int = 100, starting_position: str = 'LATEST'
    ):
        """
        Lambda 함수에 트리거 추가
        """
        response = self.lambda_client.create_event_source_mapping(
            EventSourceArn=event_source_arn,
            FunctionName=function_name,
            Enabled=enabled,
            BatchSize=batch_size,  # 처리할 항목 수 조정 가능
            StartingPosition=starting_position  # 최신 항목부터 시작
        )
        return response


    def update_lambda_code(self, function_name, s3_bucket, s3_key, publish=False):
        """
        Updates the code of an existing Lambda function.

        :param function_name: Name of the Lambda function to update.
        :param s3_bucket: S3 bucket where the updated Lambda code is stored.
        :param s3_key: Key of the S3 object containing the updated Lambda code.
        :param publish: Whether to publish a new version of the function.
        :return: Response from the Lambda update_function_code API call.
        """
        try:
            response = self.lambda_client.update_function_code(
                FunctionName=function_name,
                S3Bucket=s3_bucket,
                S3Key=s3_key,
                Publish=publish
            )
            print("Function code updated successfully.")
            return response
        except boto3.exceptions.Boto3Error as e:
            print(f"Error updating Lambda function code: {e}")
            raise

    def update_lambda_configuration(self, function_name, memory_size=None, timeout=None):
        """
        Updates the configuration of an existing Lambda function.

        :param function_name: Name of the Lambda function to update.
        :param memory_size: (Optional) Memory size for the Lambda function in MB.
        :param timeout: (Optional) Timeout for the Lambda function in seconds.
        :return: Response from the Lambda update_function_configuration API call.
        """
        try:
            if not memory_size and not timeout:
                print("No configuration parameters provided for update.")
                return

            config_params = {}
            if memory_size:
                config_params['MemorySize'] = memory_size
            if timeout:
                config_params['Timeout'] = timeout

            response = self.lambda_client.update_function_configuration(
                FunctionName=function_name,
                **config_params
            )
            print("Function configuration updated successfully.")
            return response
        except boto3.exceptions.Boto3Error as e:
            print(f"Error updating Lambda function configuration: {e}")
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
            response = self.lambda_client.create_function(
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
            response = self.lambda_client.delete_function(FunctionName=function_name)
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
            response = self.lambda_client.get_function(FunctionName=function_name)
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
            response = self.lambda_client.update_function_configuration(
                FunctionName=function_name,
                Environment={
                    'Variables': environment_variables
                }
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            print(f"Error updating Lambda environment variables: {e}")
            raise