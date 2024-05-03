### Step 1: Create an AWS account
You can [create an AWS account](http://aws.amazon.com/) and then go to the [AWS Console](https://console.aws.amazon.com/).

### Step 2: Creating an EC2 instance
Find the AWS EC2 serive. Select `Launch Instance` to start creating the VM. Make sure you select your region in the top right. This project uses `Ubutu` and the `Ubuntu Server 22.04 LTS (HVM), SSD Volume Type` with the `64-bit (x86)` architecture (all free tiers). I used the  `t2.micro ` instance type and created a new key-pair (rsa and pem). Move this file to a secure spot since you will need to get access to your instance. Run:
```
chmod 400 <path_to_your_pem_file>
```
on the key file to restrict access. Finally, launch your instance. Then, set an Elastic IP address so that the IP remains the same even if you stop or restart the instance. In the AWS Console, find `Elastic IPs` on the lefthand side and select `Allocate Elastic IP address`. Attach it to your instance.

### Step 3: Enabling ssh
Find the `Security Groups` on the lefthand side (below Elastic IPs). We want to create one if there isn't already one. Add an inbound rule with Type:SSH, Protocol:TCP, Port Range: 22, and Source:Custom 0.0.0.0/0.

### Step 4: Logging in and Updating
On your own computer enter:
```
ssh -i "<path to private key>" <ec2_user>@<ec2_public_ip>
```
If you didn't change anything, <ec2_user> is `ubuntu`. Run `sudo apt-get update` and `sudo apt upgrade` and accept any prompts. Follow the same steps in [Setting Up Lampi](../Setting%20Up%20LAMPI) to get python3. 

### Move on to [Accessing NYT API](../Accessing%20NYT%20API)
