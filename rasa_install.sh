#!/bin/bash
rasa_ver=${1:-latest}
rasa_docker=${2:-sgino209/rasabot_app:newt_actions}

# RASA Compatability Matrix
declare -A rasa_comp_matrix=(
["latest"]="2.1.2" \
["0.34.0"]="2.1.2" \
["0.33.0"]="2.0.2" \
["0.32.2"]="1.10.2" \
["0.31.5"]="1.10.2" \
["0.30.1"]="1.10.2" \
["0.29.3"]="1.10.2" \
["0.28.6"]="1.10.1" \
["0.27.8"]="1.9.0" \
["0.26.4"]="1.8.1" \
["0.25.3"]="1.7.0" \
["0.24.8"]="1.6.1" \
["0.23.6"]="1.5.2" \
["0.22.2"]="1.4.0" \
["0.21.5"]="1.3.3" \
["0.20.5"]="1.2.0"
)
rasa_sdk_ver="${rasa_comp_matrix[${rasa_ver}]}"

# Start fresh
cd /etc/rasa
sudo docker-compose down --remove-orphans
sudo docker system prune -a
cd -
sudo rm -rf /etc/rasa

# Install RASA-X
curl -sSL -o install.sh https://storage.googleapis.com/rasa-x-releases/${rasa_ver}/install.sh
sudo bash ./install.sh
cd /etc/rasa

# Import legacy files, if exists:
if [ -d "/etc/rasa.old" ]; then
    sudo cp -r /etc/rasa.old/actions ./
    sudo cp /etc/rasa.old/Dockerfile ./
    sudo cp /etc/rasa.old/docker-compose.override.yml ./
    sudo cp /etc/rasa.old/credentials.yml ./
    sudo cat /etc/rasa.old/Dockerfile | sed "s/:latest/:${rasa_sdk_ver}/g" > ./Dockerfile
fi

# Create/Update a new user:
sudo python3 rasa_x_commands.py create admin me q1w2e3r4
sudo python3 rasa_x_commands.py create --update admin me q1w2e3r4
sudo python3 rasa_x_commands.py create --update admin me q1w2e3r4

# Prepare docker images:
sudo docker build . -t ${rasa_docker}
sudo docker push ${rasa_docker}

# Start RASA-X
sudo docker-compose up -d

# Display logs
sudo docker-compose logs
sudo docker-compose logs app | tail -100

echo "Done!"
