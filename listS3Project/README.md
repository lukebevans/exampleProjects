# List S3 contents

This project contains a python3.6 lambda function that lists all S3 buckets within an AWS account and their default encryption status.
It also lists all unencrypted objects within each S3 bucket

## Getting Started

Run the command: "pip3 install -r requirements.txt" to install all required modules

## Running unit tests

Run the command "python3 test_index.py" from the project root.

## Deployment

Zip the contents of the project folder: "zip -r project-name.zip * "

Upload the zip file to your lambda function

## Author

* **Luke Bevans**
