# reporter
 Report what you see

## Update Ubuntu Server
```
sudo apt update && sudo apt upgrade -y
```

## Enable Root user password and SSH
#### Set a password for the root user:
```
sudo passwd root
```
#### Enable SSh for the root user:
```
sudo nano /etc/ssh/sshd_config
```
##### Find the line that says:
```
PermitRootLogin prohibit-password
```
##### Change it to:
```
PermitRootLogin yes
```
#### Restart the SSH service:
```
sudo systemctl restart ssh
```

## Install Docker on Ubuntu Server

##### Add Docker's official GPG key:
```
sudo apt-get install ca-certificates curl gnupg
```
```
sudo install -m 0755 -d /etc/apt/keyrings
```
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
```
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```
##### Add the repository to Apt sources:
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
```
sudo apt-get update
```
##### Install Docker packages:
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

## Install Portainer with Docker
##### Create a volume that Portainer Server will use to store its database:
```
sudo docker volume create portainer_data
```
##### Download and install Portainer Server:
```
sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```
##### Login to the admin account:
```
https://<serverip>:9443
```

## To download and install this application on Docker on Ubuntu Server run the following commands:

##### You can run this command in any directory you want I just run it from the home directory
```
sudo git clone https://github.com/Ewsmyth/reporter.git
```
##### This should be altered to the proper path to the directory you cloned the git into
```
cd reporter
```
##### The period is for if you are inside the "reporter" directory if you are not then you should replace this with the path to the cloned reporter directory
```
sudo docker build -t reporter-image .
```
##### Setup a volume for the the database for persistent storage
```
sudo docker volume create <volume name>
```
###### Example
```
sudo docker volume create reporter-data
```
##### Install Reporter
```
sudo docker run -d -p <port>:<port> --restart=unless-stopped \
    -e SQLALCHEMY_DATABASE_URI='sqlite:///<path of .db file> \
    -e SECRET_KEY='<create a key>' \
    -e HOST='0.0.0.0'
    -e PORT=<port>
    -v <volume name>:/var/lib/docker/volumes/<volume name> \
    reporter-image
```
###### Example
```
sudo docker run -d -p 80:80 --restart=unless-stopped \
    -e SQLALCHEMY_DATABASE_URI='sqlite:////var/lib/docker/volumes/reporter-data/reporter-data.db' \
    -e SECRET_KEY='aabbccddeeffgghhiijjkkllmmnnoopp' \
    -e HOST='0.0.0.0' \
    -e PORT=80 \
    -v reporter-data:/var/lib/docker/volumes/reporter-data \
    reporter-image
```