from aws_cdk import (
    App, Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigw,
    aws_s3 as s3
)
from constructs import Construct

class S3LambdaApiStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "BackendBucket-Cronos")

        base_lambda = _lambda.Function(
            self, "PresignedUrlLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("PresignedUrlLambda"), 
            environment={
                "BUCKET_NAME": bucket.bucket_name
            }
        )

        base_api = _apigw.RestApi(self, 'CronosAPIGateway',
                                  rest_api_name='CronosAPIGateway')

        example_entity = base_api.root.add_resource(
            'presigned-url',
            default_cors_preflight_options=_apigw.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=_apigw.Cors.ALL_ORIGINS)
        )
        example_entity_lambda_integration = _apigw.LambdaIntegration(
            base_lambda,
            proxy=False,
            integration_responses=[
                _apigw.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )
        example_entity.add_method(
            'GET', example_entity_lambda_integration,
            method_responses=[
                _apigw.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )
        # Outputs
        self.api_url = base_api.url
        self.bucket_name = bucket.bucket_name
