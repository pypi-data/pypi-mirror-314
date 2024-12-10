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
