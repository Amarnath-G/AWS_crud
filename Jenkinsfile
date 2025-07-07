pipeline {
    agent any

    parameters {
        choice(name: 'ACTION', choices: ['list', 'describe', 'start', 'stop', 'create', 'terminate'], description: 'Choose EC2 operation')
    }

    environment {
        AWS_REGION = 'us-east-1'
        INSTANCE_ID = 'i-0123456789abcdef0'
        AMI_ID = 'ami-0abc1234567890'
        INSTANCE_TYPE = 't2.micro'
        KEY_NAME = 'my-key'
        SECURITY_GROUP = 'sg-01234abcd'
        SUBNET_ID = 'subnet-01234abc'
    }

    stages {
        stage('Install Boto3') {
            steps {
                sh 'pip install boto3'
            }
        }

        stage('Run EC2 Action') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-keys', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-keys', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        echo "Running action: $ACTION"
                        python3 ec2_crud.py $ACTION
                    '''
                }
            }
        }
    }
}
