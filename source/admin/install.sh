#!/bin/bash

# 1. Install python
echo""
echo "Installing Python..."
apt install python3 python3-pip -y

# 2. Install requirements
echo""
echo "Installing Python requirements..."
pip3 install -r ./requirements.txt --break-system-packages

# 3. Copy the systemd service file and enable it
echo""
echo "Copying systemd service file..."
cp ./kokenku-admin.service /etc/systemd/system/
systemctl enable kokenku-admin.service

# 4. Reload systemd to recognize the new service file
echo""
echo "Reloading systemd..."
systemctl daemon-reload

# 5. Start the systemd service
echo""
echo "Starting the systemd service..."
systemctl start kokenku-admin.service

echo""
echo "Installation completed."
echp "You may now proceed to inicializing the database and creating new user."
