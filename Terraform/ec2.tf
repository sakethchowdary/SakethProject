terraform {
  required_providers {
    name = {
      source = "hashicorp/aws"
     }
  }
}

provider "aws" {
  region = "us-east-1"
}


resource "aws_instance" "backendlogic-ec2" {
  ami = "ami-0022f774911c1d690"
  instance_type = "t2.micro"
  associate_public_ip_address = true
  key_name = aws_key_pair.ec2-keypair.key_name
  security_groups = [ aws_security_group.ec2-security-group.name ]

  connection {
    type     = "ssh"
    user     = "ec2-user"
    private_key = file("~/.ssh/id_rsa")
    host     = self.public_ip
    agent = true
  }

  # Copying AWS config file to remote  
  provisioner "file" {
    source = "~/.aws/config"
    destination = "/home/ec2-user/config"
  }
  # Copying AWS creds file to remote
  provisioner "file" {
    source = "~/.aws/credentials"
    destination = "/home/ec2-user/credentials"
  }

  provisioner "remote-exec" {
    inline = [
        "mkdir -p /home/ec2-user/.aws",
        "mv /home/ec2-user/config /home/ec2-user/credentials /home/ec2-user/.aws/",
        "echo 'Installing updates'",
        "sudo yum update -y",
        "echo 'Installing Docker'",
        "sudo yum install docker -y",
        "echo 'Enabling Docker daemon'",
        "sudo service docker start",
        "echo 'Adding default user to docker group'",
        "sudo usermod -aG docker ec2-user",
        "echo 'Installing GIT'",
        "sudo yum install git -y",
        "echo 'cloning GIT project'",
        "git clone https://github.com/sakethchowdary/SakethProject.git",
        "cd SakethProject/Project",
        "echo 'Building docker image'",
        "sudo docker build -t backend-logic-repo:latest .",
        "sudo docker tag backend-logic-repo:latest 409043763943.dkr.ecr.us-east-1.amazonaws.com/backend-logic-repo:latest"
        # "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 409043763943.dkr.ecr.us-east-1.amazonaws.com",
        # "docker push 409043763943.dkr.ecr.us-east-1.amazonaws.com/backend-logic-repo:latest"
    ]
  }

  tags = {
    "Name" = "Backend-Logic-Deployer"
  }
}

output "backend-logic-ec2" {
    value = aws_instance.backendlogic-ec2.public_ip
    depends_on = [
      aws_instance.backendlogic-ec2
    ]
}

resource "aws_key_pair" "ec2-keypair" {
  key_name = "backend-logic-key"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_security_group" "ec2-security-group" {
  vpc_id = "vpc-021fdd87abf09e0db"
  name = "ec2-open-security-group"
  ingress{
        cidr_blocks = [ "0.0.0.0/0" ]
        description = "open ingress"
        from_port = 0
        protocol = -1
        to_port = 0
    }
    egress{
        cidr_blocks = [ "0.0.0.0/0" ]
        description = "open egress"
        from_port = 0
        protocol = "-1"
        to_port = 0
    }
}

