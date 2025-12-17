# Find the latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

# Create EC2 Instance
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.small" # t2.micro (Free Tier) often crashes with K8s. t3.small is cheap (~$0.02/hr).
  # If you strictly want Free Tier, change to "t2.micro" but be warned about performance.

  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true
  key_name                    = "ssis-key"

  tags = {
    Name = "ssis-server"
  }

  root_block_device {
    volume_size = 20 # 20GB Storage
  }
}
