sudo apt-get update -y
sudo apt-get install -y python3-pip
sudo apt-get install -y libjpeg-dev zlib1g-dev  # pillow
pip3 install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
