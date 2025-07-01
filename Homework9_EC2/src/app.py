import json
import boto3

ec2_instance = boto3.client('ec2')

def lambda_handler(event, context):
    # get the name or id of the ec2 instance from the event
    instance_id = event.get('instance_id')

    # get the action of the event (whether start of stop)
    action = event.get('action')

    if not instance_id or action not in ['start', 'stop']:
        return {
            'statusCode': 400,
            'body': 'Invalid input'
        }
    
    try:
        if action == "start":
            ec2_instance.start_instances(InstanceIds = [instance_id])
            return {'statusCode': 200, 'body': f'Start instance successfully{instance_id}'}
        elif action == 'stop':
            ec2_instance.stop_instances(InstanceIds = [instance_id])
            return {'statusCode': 200, 'body': f'Stop instance successfully{instance_id}'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
            


