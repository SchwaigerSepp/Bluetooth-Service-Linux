# Bluetooth-Service-Linux
A python script, that will run as a service. It will start a RFCOMM Socket that will listen for connections from the NavigationApp, parse the incomming data and send it to the display..  


To create the service, first run 

sudo systemctl edit --force --full bluetooth.service 

then write the below commands into the file:

[Unit]
Description=Bluetooth Service
Wants=network.target
After=network.target

[Service]
ExecStartPre=/bin/sleep 10
ExecStart= PATH TO PYTHON SCRIPT
Restart=always

[Install]
WantedBy=multi-user.target

Then you need to enable the service with

sudo systemctl enable bluetooth.service

Then just reboot the system and it should work
