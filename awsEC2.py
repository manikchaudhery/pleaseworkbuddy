import boto.ec2

AWS_ACCESS_KEY_ID = "AKIAI7B4RQLPCPLLRQLA";
AWS_SECRET_ACCESS_KEY = "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";
KEY_NAME = "KEY"
	
#Initial the aws connection, create key-pair, security group, and return the connection and the first instance
def init():
	#Connect to AWS
	conn = boto.ec2.connect_to_region("us-east-1", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

	#Create a key pair
	key_pair = conn.create_key_pair(KEY_NAME)
	key_pair.save("")

	#Create a security group with 3 rules 
	group = conn.create_security_group("Zafeers_Group5", "First group created")
	group.authorize("icmp", -1, -1, "0.0.0.0/0")
	group.authorize("TCP", 22, 22, "0.0.0.0/0")
	group.authorize("TCP", 80, 80, "0.0.0.0/0")

	#Create an instance object
	resp = conn.run_instances("ami-9eaa1cf6", instance_type="t2.micro", key_name= KEY_NAME, security_groups=[group])

	inst = resp.instances[0]
	while (inst.update() != "running"):
		inst.update()

	address = conn.allocate_address()
	if (address.associate(inst.id)):
		print "Set up static IP address"
		print "Paste this in your browser: ", address

	return address 

def get_static_address(conn, inst):
	address = conn.allocate_address()
	if (address.associate(inst.id)):
		print "Set up static IP address"
	return address 

ipAddress = init()

#print "Sending sshSetup to AWS EC2 instance"
#subprocess.call("scp -i %s.pem -o StrictHostKeyChecking=no sshSetup.sh ubuntu@%s:~/" % (KEY_NAME, ipAddress), shell=True)

#print "Opening project on AWS EC2 instance"
#subprocess.Popen("ssh -i %s.pem ubuntu@%s ~/sshSetup.sh" % (KEY_NAME, ipAddress))


