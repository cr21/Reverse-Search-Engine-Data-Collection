## Docker install In ubuntu 22.04  lts
sudo apt-get update
sudo apt-get upgrade  -y

sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce -y
sudo systemctl status docker

sudo usermod -aG docker ubuntu
newgrp docker

## Aws cli installation
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install

## Github Runner configuration

mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.299.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.299.1/actions-runner-linux-x64-2.299.1.tar.gz
echo "147c14700c6cb997421b9a239c012197f11ea9854cd901ee88ead6fe73a72c74  actions-runner-linux-x64-2.299.1.tar.gz" | shasum -a 256 -c
tar xzf ./actions-runner-linux-x64-2.299.1.tar.gz

## Important Allow github token so we can connect with github token automatically whenever machine goes down
./config.sh --url https://github.com/cr21/Reverse-Search-Engine-Data-Collection --token ACG5HLVRSKZ7L5O7S3LKI5TDTQBLG
./run.sh

## Add Github runner as a service
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh status

## To stop the service
sudo ./svc.sh stop
sudo ./svc.sh uninstall