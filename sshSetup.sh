export DEBIAN_FRONTEND=noninteractive

sudo apt-get update

printf "\nsshSetup: Installing Git"
sudo apt-get install -y git

printf "\nsshSetup: Installing Pip"
sudo apt-get install -y python-pip --fix-missing

printf "\nsshSetup: Installing Dependencies"
sudo pip install Beaker

sudo pip install oauth2client

sudo pip install google-api-python-client

sudo pip install pymongo

printf "\nsshSetup: Cloning Git Project Repo"
sudo git clone https://github.com/manikchaudhery/pleaseworkbuddy.git

cd pleaseworkbuddy
cd lab3csc

sudo python searchEngine.py

printf "\nsshSetup: Server is now running. Open the public IP address on your browser"
