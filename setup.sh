#sudo adduser crosstag
cd /home/pi
git clone https://github.com/lundstrj/crosstag.git

sudo apt-get install python-pip
sudo pip install requests
sudo pip install pyserial
sudo pip install flask-security 
sudo pip install flask-sqlalchemy
sudo pip install Flask-WTF
touch crosstag.db
