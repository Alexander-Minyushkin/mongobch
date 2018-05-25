
# Setup for Amazon Linux AMI 2018.03.0 (HVM)

sudo yum update -y
sudo yum install git -y
sudo yum install python36 -y

git clone https://github.com/Alexander-Minyushkin/mongobch.git
cd mongobch/
sudo python3 -m pip install -r requirements.txt


