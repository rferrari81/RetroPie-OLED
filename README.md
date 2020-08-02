# RetroPie-OLED
Retropie OLED Display MOD version by Roby F.

Show Game Title on 128x64 OLED I2C Display for RetroPie v4.0.2+

ABOUT

This script written in Python for RetroPie project (https://retropie.org.uk/) running on Raspberry Pi 2,3, which displays all necessary info on a 128x64 OLED I2C display

Thanks to members of Raspigamer forum for all the hard work (Duritz, losernator, RiNa, Yanubis, 까먹구, 꼬락이, 뇽가뤼, 다큰아이츄, 박군, 불친절한, 부천아저씨, 스트렌져, 유령군, 지껄러뷰, 쪼딩, 초단, 캡틴하록, 키티야, 허니버터꿀, 후루뚜뚜)

HOW DOES IT WORK
First, looking for title image from 'gametitle' folder with same filename of rom.

If no match, display title name from gamelist.xml(scraped metadata).

Could not find any info, then display the file name.

FEATURES
Current Date and Time, IP address of eth0, wlan0
CPU Temperature
Emulator name and ROM information
Title image of currently running romfile
Double-byte character set support (Korean/Chinese/Japanese)
Development Environment
Raspberry Pi 2, 3, 4
RetroPie v4.0.2 and later
128x64 OLED I2C display

INSTALL
Step 1. Scrap metadata ( https://github.com/RetroPie/RetroPie-Setup/wiki/Scraper )

Step 2. Install Retropie-OLED Script
cd ~
git clone https://github.com/rferrari81/RetroPie-OLED.git
cd ./RetroPie-OLED/
chmod 755 install.sh
./install.sh

Raspberry Pi I2C GPIO Pinout
FYI, VCC could be different by manufacturer (5v or 3.3v)
