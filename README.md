# AWS Lambda Deployment with Blue-Green Deployment using Jenkins and AWS CodeDeploy

This project demonstrates how to set up a CI/CD pipeline using Jenkins to deploy an AWS Lambda function with blue-green deployment managed by AWS CodeDeploy. The pipeline automates the process of packaging, uploading, and deploying the Lambda function, ensuring zero downtime and seamless updates. It integrates with multiple AWS services such as **S3, Lambda, CloudFormation, CodeDeploy, and SNS**; focus on static code analysis with **Bandit** and infrastructure scanning with **cfn-nag** and sends notifications upon successful deployment.

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
   - Pipeline: AWS Steps plugin

4. **S3 Bucket** to store the Lambda ZIP file.
   
---

## Project Structure
     
      ├── Jenkinsfile                      # Jenkins pipeline definition
      ├── deployment_production.yaml       # CloudFormation template for AWS resources
      ├── lambda_function.py               # Lambda function code
      ├── appspec.yaml                     # Deployment instructions for AWS CodeDeploy
      └── README.md                        # Project documentation

-----
## Pipeline Workflow

1.  **Checkout Code**
    
    *   The pipeline pulls the latest code from the **main branch** of the GitHub repository.
      
2.  **Security Scans**
    
    *   **Static Code Analysis with Bandit:** Scans Python code for security vulnerabilities.
    *   **Infrastructure as Code Scanning with cfn-nag:** Analyzes CloudFormation templates for security issues.
      
3.  **Evaluate Security Reports**
    
    *   The pipeline evaluates the results from the security scans.
    *   If any critical vulnerabilities are found, the build fails, preventing deployment.
      
4.  **Build Lambda Package**
    
    *   The Lambda function code and **`appspec.yaml`** are compressed into a **ZIP file**.
5.  **Upload to S3**
    
    *   The ZIP file is uploaded to the specified **S3 bucket** for deployment.
6.  **Deploy to Lambda**
    
    *   If the Lambda function exists, the pipeline **updates the function code**.
    *   If it doesn’t exist, the **CloudFormation template** creates it along with any required infrastructure.
7.  **Update AppSpec File**
    
    *   The **`appspec.yaml`** file is updated with the **current and target Lambda function versions**.
8.  **Blue-Green Deployment**
    
    *   Traffic is **shifted to the new version** using CodeDeploy.
    *   If an issue occurs, traffic can quickly **roll back** to the previous version.
9.  **Notifications**
    
    *   A notification is sent to **SNS** upon successful deployment.
---
   Security Enhancements
    
 This project incorporates DevSecOps practices by integrating security checks into the CI/CD pipeline to ensure that only secure and compliant code is deployed.
    
  ### **1\. Static Code Analysis with Bandit**

  *   **Tool Used:** [Bandit](https://bandit.readthedocs.io/en/latest/)
  *   **Purpose:** Scans the Python code (`lambda_function.py`) for security issues like hardcoded credentials, weak cryptography, and injection vulnerabilities.
  *   **Integration:** Added as a pipeline stage called **"Security: Static Code Analysis"**.
    
    

    
### **2\. Infrastructure as Code Scanning with cfn-nag**
    
   *   **Tool Used:** [cfn-nag](https://github.com/stelligent/cfn_nag)
   *   **Purpose:** Analyzes the CloudFormation template (`deployment_production.yaml`) for security vulnerabilities, such as insecure configurations and permissive policies.
   *   **Integration:** Added as a pipeline stage called **"Security: Infrastructure Scan"**.

### **3\. Security Report Evaluation**
    
 *   **Purpose:** Parses the reports generated by the security tools.
 *   **Integration:** Added as a pipeline stage called **"Security: Evaluate Reports"**.
 *   **Behavior:** If critical vulnerabilities are found, the pipeline fails to prevent insecure code from being deployed.

  ### **4\. Credentials and Secrets Management**
  
  *   **AWS Credentials:** Stored securely in Jenkins using the **Credentials Plugin**.
  *   **Access Keys and Secrets:** Managed through Jenkins credentials and injected into the pipeline as environment variables.

  ### **5\. IAM Roles and Permissions**
    
 *   **Principle of Least Privilege:** IAM roles (`LambdaExecutionRole` and `CodeDeployServiceRole`) are configured with minimal required permissions.
 *   **Policy Validation:** IAM policies are reviewed to ensure they do not grant excessive permissions.
    
  ### **6\. Secure Storage and Transmission**
    
  *   **S3 Bucket Security:** The S3 bucket used for storing the Lambda package is secured with proper access controls and encryption at rest.
  *   **Encryption:** Data in transit is secured using HTTPS when uploading to S3.
    
  ### **7\. Logging and Monitoring**
    
   *   **Pipeline Logs:** Jenkins pipeline logs are maintained for audit purposes.
   *   **AWS CloudWatch:** Used for monitoring Lambda function execution and logging.


1.  Setup Instructions
    ------------------
    
    ### 1\. Clone the Repository
   
        .git clone https://github.com/YourUsername/YourRepository.git
         cd YourRepository
-----
### 2\. Install Security Tools on Jenkins Agents

Ensure that the following security tools are installed on the Jenkins agent machines:
  * Bandit
  * cfn-nag
-----
   ### 3\. Configure AWS Resources

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
   ### 4\. Prepare the Lambda Function Package
     zip lambda_function.zip lambda_function.py appspec.yaml

   ### 5\. Deploy the CloudFormation Stack
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

### 6\. Configure Jenkins

### 

1.  **Install Required Plugins**
    
    *   AWS Credentials Plugin
    *   Git Plugin
    *   Pipeline AWS Steps Plugin
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

### 7\. Run the Jenkins Pipeline

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

## Conclusion

By integrating security checks directly into the CI/CD pipeline, this project not only ensures seamless and reliable deployments but also promotes a security-first mindset throughout the development process. We have demonstrated how tools like **Bandit** and **cfn-nag** can be effectively used to identify and mitigate potential security risks before they reach production.

Building on AWS services and Jenkins, this project showcases a practical approach to implementing DevSecOps principles in a serverless application environment. It emphasizes the importance of automating security tasks to enhance efficiency without compromising on safety.

I hope this project serves as a valuable resource for you to build your own secure CI/CD pipelines. Your feedback and contributions are welcome!

If you have any questions, suggestions, or need further assistance, please feel free to reach out. 


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

References
----------

### 

*   [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
*   [AWS CodeDeploy Documentation](https://docs.aws.amazon.com/codedeploy/)
*   [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/)
*   [Jenkins Documentation](https://www.jenkins.io/doc/)
*   [Blue-Green Deployments with CodeDeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-create-advanced-blue-green.html)
*   [Bandit Documentation](https://bandit.readthedocs.io/en/latest/)
*   [cfn-nag Documentation](https://github.com/stelligent/cfn_nag)
