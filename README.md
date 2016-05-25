Crosstag: A sensible gym solution for sensible gyms
=========================

Features
----------

- COTS RFID-reader compatible (https://www.sparkfun.com/products/retired/9875, https://www.sparkfun.com/products/13198)
- Stand alone server
- Stand alone reader
- Reader designed to run on a Raspberry Pi (http://www.raspberrypi.org/products/)
- Not much more

Installation
------------
### install dependencies and clone this repo
```sh
sudo pip3 install —upgrade pip
git clone https://github.com/ej222pj/crosstag.git
sudo pip3 install -r requirements.txt 
```
### To start the server
```sh
sudo python3 crosstag_server.py
```
### To start the reader on a Raspberry PI
```sh
sudo python3 crosstag_reader.py
```
