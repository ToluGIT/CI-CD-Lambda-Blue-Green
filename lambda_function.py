import random

def lambda_handler(event, context):
    # Insecure random number generation
    token = random.random()
    print("Generated insecure token:", token)
    
    return {
        'statusCode': 200,
        'body': 'Function executed successfully!'
    }
