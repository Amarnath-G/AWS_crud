import boto3
import os
import sys

REGION = os.getenv('AWS_REGION', 'us-east-1')
INSTANCE_ID = os.getenv('INSTANCE_ID')
AMI_ID = os.getenv('AMI_ID')
INSTANCE_TYPE = os.getenv('INSTANCE_TYPE', 't2.micro')
KEY_NAME = os.getenv('KEY_NAME')
SECURITY_GROUP = os.getenv('SECURITY_GROUP')
SUBNET_ID = os.getenv('SUBNET_ID')

ec2 = boto3.client('ec2', region_name=REGION)

def list_instances():
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"{instance['InstanceId']} - {instance['State']['Name']} - {instance.get('Tags', [])}")

def describe():
    response = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
    print(response)

def start():
    response = ec2.start_instances(InstanceIds=[INSTANCE_ID])
    print(response)

def stop():
    response = ec2.stop_instances(InstanceIds=[INSTANCE_ID])
    print(response)

def create():
    response = ec2.run_instances(
        ImageId=AMI_ID,
        MinCount=1,
        MaxCount=1,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        SecurityGroupIds=[SECURITY_GROUP],
        SubnetId=SUBNET_ID,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'Jenkins-Boto3-Instance'}]
            }
        ]
    )
    print("Created instance:", response['Instances'][0]['InstanceId'])

def terminate():
    response = ec2.terminate_instances(InstanceIds=[INSTANCE_ID])
    print(response)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ec2_crud.py [list|describe|start|stop|create|terminate]")
        sys.exit(1)

    action = sys.argv[1].lower()

    {
        'list': list_instances,
        'describe': describe,
        'start': start,
        'stop': stop,
        'create': create,
        'terminate': terminate
    }.get(action, lambda: print("Invalid action"))()
