# AWS Lambda Deployment with Blue-Green Deployment using Jenkins and AWS CodeDeploy

This project demonstrates how to set up a CI/CD pipeline using Jenkins to deploy an AWS Lambda function with blue-green deployment managed by AWS CodeDeploy. The pipeline automates the process of packaging, uploading, and deploying the Lambda function, ensuring zero downtime and seamless updates. It integrates with multiple AWS services such as **S3, Lambda, CloudFormation, CodeDeploy, and SNS** and sends notifications upon successful deployment.

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

4. **S3 Bucket** to store the Lambda ZIP file.
   
---

## Project Structure
     
      ├── Jenkinsfile           # Jenkins pipeline definition
      ├── deployment_production.yaml       # CloudFormation template for AWS resources
      ├── lambda_function.py    # Lambda function code
      ├── appspec.yaml          # Deployment instructions for AWS CodeDeploy
      └── README.md             # Project documentation

-----
## Pipeline Workflow

1.  **Checkout Code**
    
    *   The pipeline pulls the latest code from the **main branch** of the GitHub repository.
2.  **Build Lambda Package**
    
    *   The Lambda function code and **`appspec.yaml`** are compressed into a **ZIP file**.
3.  **Upload to S3**
    
    *   The ZIP file is uploaded to the specified **S3 bucket** for deployment.
4.  **Deploy to Lambda**
    
    *   If the Lambda function exists, the pipeline **updates the function code**.
    *   If it doesn’t exist, the **CloudFormation template** creates it along with any required infrastructure.
5.  **Update AppSpec File**
    
    *   The **`appspec.yaml`** file is updated with the **current and target Lambda function versions**.
6.  **Blue-Green Deployment**
    
    *   Traffic is **shifted to the new version** using CodeDeploy.
    *   If an issue occurs, traffic can quickly **roll back** to the previous version.
7.  **Notifications**
    
    *   A notification is sent to **SNS** upon successful deployment.
---

1.  Setup Instructions
    ------------------
    
    ### 1\. Clone the Repository
   
        .git clone https://github.com/YourUsername/YourRepository.git
         cd YourRepository
-----

   ### 2\. Configure AWS Resources

#### Create IAM Roles

1.  **Lambda Execution Role**  
    Create a role named **LambdaExecutionRole** with:
    
    *   **AWSLambdaBasicExecutionRole** policy.
    *   Any additional permissions your Lambda function requires.
2.  **CodeDeploy Service Role**  
    Create a role named **CodeDeployServiceRole** with:
    
    *   **AWSCodeDeployRole** policy.
    *   **AWSLambdaRole** policy.
    *   An inline policy allowing CodeDeploy to manage Lambda functions and aliases.
    
    ###  Create an S3 Bucket
   
        aws s3 mb s3://s3-jenkins-lambda
    --- 
   ### 3\. Configure AWS Resources 
     zip lambda_function.zip lambda_function.py appspec.yaml

   ### 4\. Deploy the CloudFormation Stack
     aws cloudformation deploy \
     --template-file deployment_production.yaml \
     --stack-name lambda-blue-green-stack \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameter-overrides \
       LambdaExecutionRoleArn=arn:aws:iam::YOUR_ACCOUNT_ID:role/LambdaExecutionRole \
       CodeDeployServiceRoleArn=arn:aws:iam::YOUR_ACCOUNT_ID:role/CodeDeployServiceRole \
       LambdaFunctionName=blue-green-lambda \
       CodeDeployApplicationName=blue-green-lambda \
       DeploymentGroupName=blue-green-deployment-group \
       S3BucketName=s3-jenkins-lambda \
       S3Key=lambda_function.zip
### 

**Note**: Replace `YOUR_ACCOUNT_ID` with your AWS account ID.

---

### 5\. Configure Jenkins

### 

1.  **Install Required Plugins**
    
    *   AWS Credentials Plugin
    *   Git Plugin
2.  **Add AWS Credentials to Jenkins**
    
    *   Go to **Jenkins Dashboard > Credentials > System > Global Credentials**.
    *   Add new credentials:
        *   **Kind**: AWS Credentials
        *   **ID**: `aws`
        *   **Access Key ID** and **Secret Access Key**: Your AWS credentials.
        *   create other parameters referenced in the 'jenkinsfile' as secret text such as the lambda-execution-role-arn, sns-topic-arn
          
3.  **Create a New Jenkins Pipeline Job**
    
    *   **Pipeline Script from SCM**:
        *   **SCM**: Git
        *   **Repository URL**: `https://github.com/YourUsername/YourRepository.git`
        *   **Script Path**: `Jenkinsfile`

* * *

### 6\. Run the Jenkins Pipeline

### 

1.  **Build the Pipeline**
    
    *   Click **Build Now** to start the pipeline.
2.  **Monitor the Pipeline**
    
    *   Check the **console output** for errors.
    *   Ensure all stages are completed successfully.

---

### Testing the Deployment

### 

1.  **Invoke the Lambda Function**  
    Use the AWS Console or CLI to invoke the Lambda function:

          aws lambda invoke --function-name blue-green-lambda:live output.json
          cat output.json
### 

2.  **Verify Lambda Alias**  
    Ensure the **`live` alias** points to the correct Lambda function version.
    
3.  **Monitor CodeDeploy Deployments**  
    In the **AWS Console**, navigate to **CodeDeploy** and check the **deployment history** to confirm successful deployments.
---

### Cleanup

1.  **Delete the CloudFormation Stack**

        aws cloudformation delete-stack --stack-name lambda-blue-green-stack

2.  **Delete the S3 Bucket and Objects**

         aws s3 rm s3://s3-jenkins-lambda --recursive
         aws s3 rb s3://s3-jenkins-lambda
    
3.   **Delete IAM Roles**  
    Remove **LambdaExecutionRole** and **CodeDeployServiceRole** from the IAM console.
    
4.   **Delete Jenkins Job**  
    Remove the pipeline job from Jenkins.

---

* * *

This project showcases a CI/CD pipeline leveraging **AWS services and Jenkins** to achieve **seamless and reliable deployments** of serverless applications.


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

References
----------
*  [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/index.html)
*  [AWS CodeDeploy Documentation](https://docs.aws.amazon.com/codedeploy/index.html)
*  [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/index.html) 
*  [Jenkins Documentation](https://www.jenkins.io/doc/)
*  [Blue-Green Deployments with CodeDeploy](https://aws.amazon.com/blogs/devops/implementing-blue-green-deployments-with-aws-codedeploy/)
