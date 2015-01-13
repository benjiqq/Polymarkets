# Sample local_settings.py

# Github Value
github_user = 'possiplex'

# Github Repo
PROJECT = "btcexchange"

REPO = '%s/%s.git' % (github_user,PROJECT)

#this is the AWS standard home
remote_dir = '/home/ubuntu/'


# Here lie the Amazon secrets
AWS = {
	'secrets':{
		'aws_key' : 'AKIAJXXDTXCQF42JD4LQ',
		'aws_secret' : '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',
		'aws_key_path' : '/Users/blc/.ssh/bensh.pem',
	}
}

localwd = '/Users/blc/w3/repos/showcase/'

APP = {
	'appname' : 'testapp.py'
}

#ec2-54-221-23-109.compute-1.amazonaws.com

SERVER = {
		'image_id' : 'ami-05355a6c',       # Amazon Linux 64-bit
		'instance_type' : 't1.micro',      # Micro Instance
		'security_groups' : 'default',
		'key_name' : 'myssh'
}
