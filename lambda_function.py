import json

def lambda_handler(event, context):
    # Hardcoded credentials (Insecure)
    db_password = "SuperSecretPassword123"
    print("Accessing database with password:", db_password)
    
    return {
        'statusCode': 200,
        'body': 'Function executed successfully!'
    }
