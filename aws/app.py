#!/usr/bin/env python3

import aws_cdk as cdk

from S3LambdaApiStack.S3LambdaApiStack import S3LambdaApiStack


app = cdk.App()
S3LambdaApiStack(app, "S3LambdaApiStack")

app.synth()
