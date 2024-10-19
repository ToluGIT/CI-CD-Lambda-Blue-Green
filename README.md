# Lambda Blue-Green Deployment with Jenkins Pipeline

This repository demonstrates a **CI/CD pipeline** for deploying AWS Lambda functions using **Jenkins**. The project implements a **blue-green deployment strategy** to ensure zero-downtime releases and safe rollbacks. It integrates with multiple AWS services such as **S3, Lambda, CloudFormation, CodeDeploy, and SNS** and sends notifications to **Slack** upon successful deployment.

 **Note** - currently in use is 'LambdaAllAtOnce', it can be tweaked to support other deployment Strategies.
---

## Project Overview

The pipeline automates the following tasks:

- **Package the Lambda code** into a ZIP archive.
- **Upload the ZIP file to S3** for deployment.
- **Deploy the Lambda function** using CloudFormation and Lambda versioning.
- **Shift traffic using a blue-green deployment strategy** with AWS CodeDeploy.
- **Notify the team** via SNS and optional Slack messages upon successful deployment.

---

## Prerequisites

1. **AWS Credentials** with access to:
   - S3  
   - Lambda  
   - CloudFormation  
   - CodeDeploy  
   - SNS  
2. **Jenkins Server** with the following plugins installed:
   - AWS Credentials Plugin  
   - Git Plugin  
   - Slack Notification Plugin (optional)  
3. **Slack Webhook URL** (if Slack notifications are required).
4. **S3 Bucket** to store the Lambda ZIP file.

---

## Project Structure


---

## Pipeline Workflow

1. **Checkout Code**  
   - The pipeline pulls the latest code from the **main branch** of the GitHub repository.

2. **Build Lambda Package**  
   - The Lambda function code is compressed into a **ZIP file**.

3. **Upload to S3**  
   - The ZIP file is uploaded to the specified **S3 bucket** for deployment.

4. **Deploy to Lambda**  
   - If the Lambda function **exists**, the pipeline updates the function code and publishes a new version.
   - If the Lambda function **does not exist**, the CloudFormation template creates it along with the required infrastructure.

5. **Blue-Green Deployment**  
   - Traffic is shifted to the **new version** using **AWS CodeDeploy**.  
   - If an issue occurs, traffic can quickly be rolled back to the **previous version**.

6. **Notifications**  
   - A **notification is sent to SNS** and optionally to **Slack** upon successful deployment.

---

## How to Run

1. **Configure Jenkins**:
   - Add AWS credentials in Jenkins using the AWS Credentials Plugin.
   - Create a **new pipeline job** in Jenkins and point it to this repository.

2. **Set Environment Variables**:
   - Ensure the following variables are configured in the Jenkinsfile:
     - `IMAGE_NAME`: Name of the Lambda ZIP package.
     - `BUCKET_NAME`: S3 bucket name for storing Lambda code.
     - `LAMBDA_FUNCTION_NAME`: Name of the Lambda function.
     - `AWS_DEFAULT_REGION`: AWS region to deploy the function.
     - `SNS_TOPIC_ARN`: ARN of the SNS topic for notifications.
  
3. **Run the Pipeline**:
   - Trigger the Jenkins job and monitor the console output for progress.
   - Verify the Lambda function deployment and traffic shift using the **AWS Console**.

---

## Technologies Used

- **Jenkins**: Automates the CI/CD process.
- **AWS Lambda**: Serverless compute platform for running the function.
- **AWS S3**: Stores the Lambda ZIP package.
- **AWS CodeDeploy**: Manages blue-green traffic shifting.
- **AWS CloudFormation**: Deploys the Lambda function and CodeDeploy resources.
- **AWS SNS**: Sends deployment notifications.
- **Slack**: Optional team notifications.

