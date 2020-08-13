#!/bin/bash
# Title          : RetroPie-OLED
# Author         : zzeromin, member of Raspberrypi Village
# Creation Date  : Nov 13, 2016
# Thanks to      : smyani, zerocool, superstar
# Free and open for all to use. But put credit where credit is due.
# MOD version by : Roby F.
# Release        : 02-02-2020
#
# Install        :
# cd ~
# git clone https://github.com/rferrari81/RetroPie-OLED.git
# cd RetroPie-OLED
# chmod 755 install.sh
# sudo ./install.sh
#
# Reference      :
# https://github.com/ipromiseyou/RetroPie-AutoSet.git


#get script path
scriptfile=$(readlink -f $0)
installpath=`dirname $scriptfile`

#run as root user
if [ "$(whoami)" != "root" ]; then
	echo "Switching to root user..."
	sudo bash $scriptfile $*
	exit 1
fi

cd $installpath
cp runcommand-onstart.sh /opt/retropie/configs/all/
cp runcommand-onend.sh /opt/retropie/configs/all/
chgrp pi /opt/retropie/configs/all/runcommand-onstart.sh
chown pi /opt/retropie/configs/all/runcommand-onstart.sh
chgrp pi /opt/retropie/configs/all/runcommand-onend.sh
chown pi /opt/retropie/configs/all/runcommand-onend.sh

sed -i '/RetroPie-OLED/d' /opt/retropie/configs/all/autostart.sh
sed -i '1i\\python3 '$installpath'/RetroPie-OLED.py &' /opt/retropie/configs/all/autostart.sh
echo "OLED Setup Complete."
echo "I2C, Python Tools Setup are starting now"
sleep 1

sudo sed -i '/dtparam=i2c_arm=on/d' /boot/config.txt
sudo sed -i '/dtparam=i2c_arm_baudrate=400000/d' /boot/config.txt
sudo sed -i '/dtparam=i2c_dev=on/d' /boot/config.txt
echo "dtparam=i2c_arm=on" >> /boot/config.txt
echo "dtparam=i2c_arm_baudrate=400000" >> /boot/config.txt
echo "dtparam=i2c_dev=on" >> /boot/config.txt
if ! grep --quiet "i2c-bcm2708" /etc/modules; then echo "i2c-bcm2708" >> /etc/modules; fi
if ! grep --quiet "i2c-dev" /etc/modules; then echo "i2c-dev" >> /etc/modules; fi
apt-get update
apt-get install -y python3-pip python3-dev python3-smbus i2c-tools
echo "I2C, Python Tools Setup Complete."
sleep 1
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
python3 -m pip install adafruit-circuitpython-ssd1306
echo "Python Library Setup Complete."
sleep 1
chgrp -R -v pi $installpath
chown -R -v pi $installpath

echo "All Setup Complete. Reboot after 3 Seconds."
sleep 3
reboot
