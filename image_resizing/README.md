# AWS Lambda Image Resizer

This project demonstrates how to use AWS Lambda to automatically resize images uploaded to an S3 bucket and save the resized images to another S3 bucket.

## Prerequisites

- AWS Account
- AWS CLI installed and configured
- Python 3.x
- Boto3 and Pillow Python libraries

## Project Setup

### Step 1: Create S3 Buckets

1. Log in to the AWS Management Console.
2. Go to the S3 service.
3. Create two S3 buckets:
   - Source bucket for original images (e.g., `source-images-bucket`)
   - Destination bucket for resized images (e.g., `resized-images-bucket`)

### Step 2: Prepare Lambda Function

1. Create a new directory for the project and navigate into it:

    ```sh
    mkdir lambda_project
    cd lambda_project
    ```

2. Install the Pillow library in the project directory:

    ```sh
    pip install pillow -t .
    ```

3. Create a `lambda_function.py` file with the following content:

    ```python
    import json
    import boto3
    from PIL import Image
    import io

    s3 = boto3.client('s3')

    def lambda_handler(event, context):
        # Get the bucket name and object key from the S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Retrieve the image from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        image_content = response['Body'].read()
        
        # Resize the image
        image = Image.open(io.BytesIO(image_content))
        resized_image = image.resize((128, 128))
        
        # Save the resized image to an in-memory buffer
        output_buffer = io.BytesIO()
        resized_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)
        
        # Upload the resized image to the destination bucket
        resized_bucket = 'resized-images-bucket'
        s3.put_object(Bucket=resized_bucket, Key=key, Body=output_buffer, ContentType='image/jpeg')
        
        return {
            'statusCode': 200,
            'body': json.dumps('Image resized and uploaded successfully')
        }
    ```

4. Package the Lambda function and dependencies into a ZIP file:

    ```sh
    zip -r lambda_function.zip .
    ```

### Step 3: Deploy the Lambda Function

1. Log in to the AWS Management Console.
2. Go to the Lambda service.
3. Create a new Lambda function:
   - Runtime: Python 3.x
   - Upload the `lambda_function.zip` file created earlier.
4. Configure the Lambda function:
   - Set the handler to `lambda_function.lambda_handler`.
   - Assign a role that has the necessary S3 permissions (e.g., `AmazonS3ReadOnlyAccess` and `AWSLambdaBasicExecutionRole`).

### Step 4: Configure S3 Event Notification

1. Navigate to the source S3 bucket (`source-images-bucket`).
2. Go to the "Properties" tab.
3. In the "Event notifications" section, add a new event notification:
   - Event type: `All object create events`
   - Send to: `Lambda function`
   - Lambda function: Select the function created in Step 3.

### Step 5: Test the Setup

1. Upload an image to the source S3 bucket (`source-images-bucket`).
2. Check the destination S3 bucket (`resized-images-bucket`) to verify that the resized image has been uploaded.

## Cleanup

To avoid incurring unnecessary charges, remember to delete the S3 buckets and the Lambda function when you are done with this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
