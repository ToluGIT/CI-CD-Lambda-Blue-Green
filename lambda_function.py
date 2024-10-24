import subprocess

def lambda_handler(event, context):
    # Insecure use of subprocess with shell=True
    command = event.get('command', 'ls -la')
    subprocess.call(command, shell=True)

    return {
        'statusCode': 200,
        'body': 'Command executed successfully! meant to fail'
    }
