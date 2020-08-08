#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Title        : RetroPie_OLED.py
Author       : zzeromin, losernator and members of Tentacle Team
Creation Date: Nov 13, 2016
Cafe         : http://cafe.naver.com/raspigamer
Thanks to    : smyani, zerocool, GreatKStar and members of Raspigamer Cafe.
Free and open for all to use. But put credit where credit is due.

Reference    :
https://github.com/haven-jeon/piAu_volumio
https://github.com/adafruit/Adafruit_CircuitPython_SSD1306
https://pillow.readthedocs.io/en/stable/

Notice       :
installed package(apt): python3-pip python3-dev python3-smbus i2c-tools
installed package(pip): Pillow, adafruit-circuitpython-ssd1306

This code edited for rpi3 Retropie v4.0.2 and later by zzeromin
"""

import time
import os
import board
import textwrap
import busio
import adafruit_ssd1306
import subprocess
import os

from sys import exit
from subprocess import *
from time import *
from datetime import datetime
from random import randint
from PIL import Image, ImageDraw, ImageFont
from board import SCL, SDA

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
# Alternatively you can change the I2C address of the device with an addr parameter:
#oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x31)

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

intro = 0
HighCPUvariable = 0

def run_cmd(cmd):
# runs whatever in the cmd variable
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def get_cpu_temp():
    tempFile = open("/sys/class/thermal/thermal_zone0/temp")
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000
    
def get_gpu_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        temp = temp[:-3]
        return (temp.replace("temp=",""))
        
def get_cpu_speed():
    tempFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    cpu_speed = tempFile.read()
    tempFile.close()
    return float(cpu_speed)/1000
    
def Shutdown():  
    os.system("sudo shutdown -h now") 

def main():
    global intro
    global HighCPUvariable
     
    infoimg = Image.open("/home/pi/RetroPie-OLED/SysInfo.png").convert('1')    
    retroarchimg = Image.open("/home/pi/RetroPie-OLED/RetroArchLogo.png").convert('1')
    titleimg = Image.open("/home/pi/RetroPie-OLED/RetropieLogo.png").convert('1')
    raspyimg = Image.open("/home/pi/RetroPie-OLED/RaspberryLogo.png").convert('1')
    alertimage = Image.open("/home/pi/RetroPie-OLED/AlertImage.png").convert('1')
   
    # Clear display.
    oled.fill(0)
    oled.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = oled.width
    height = oled.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    padding = 0
    top = padding
    bottom = height-padding

    # Load default font.
    font = ImageFont.load_default()
    font_system = ImageFont.truetype('/home/pi/RetroPie-OLED/neodgm.ttf', 16)
    font_rom = ImageFont.truetype('/home/pi/RetroPie-OLED/BM-HANNA.ttf', 16)
    fonte_rom = ImageFont.truetype('/home/pi/RetroPie-OLED/lemon.ttf', 10)
    font_msg = ImageFont.truetype('/home/pi/RetroPie-OLED/d2.ttf', 11)
    font_icon = ImageFont.truetype('/home/pi/RetroPie-OLED/fontawesome-webfont.ttf', 20)
    font_icon2 = ImageFont.truetype('/home/pi/RetroPie-OLED/fontawesome-webfont.ttf', 14)
    font_icon3 = ImageFont.truetype('/home/pi/RetroPie-OLED/fontawesome-webfont.ttf', 16)
    new_Speed = round(get_cpu_speed(),1)
    new_Temp = round(get_cpu_temp(),1)
    #CPUTemp = str( new_Temp )
    #HighCPU = float(CPUTemp)

    while True:    
        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True )
        cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"%s\", $3}'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"%s\", $2}'"
        MemTotal = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
        MemPercent = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"%d\", $3}'"
        DiskFree = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"%d\", $2}'"
        DiskUsed = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"%s\", $5}'"
        DiskPercent = subprocess.check_output(cmd, shell = True )
        #CPUTemp = str( new_Temp ) + chr(0xB0) +"C"
        CPUTemp = str( new_Temp )
        new_Speed = round(get_cpu_speed(),1)
        CPUSpeed = str( new_Speed )
        GPUTemp = (get_gpu_temp())
        HighCPU = float(CPUTemp)
        HighGPU = float(GPUTemp)
        
        if HighCPU > 70 and HighCPU < 75:
            new_Temp = round(get_cpu_temp(),1)
            CPUTemp = str( new_Temp )
            HighCPU = float(CPUTemp)
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            HighCPUvariable = 1
            image.paste(alertimage,(0,0))
            msg1 = "CPU OVER TEMPERATURE"
            msg1_size = draw.textsize(msg1, font=font)
            draw.text(((width-msg1_size[0])/2, top+40), msg1, font=font, fill=255)
            draw.text((47, top+50), str( new_Temp ) + chr(0xB0) +"C", font=font, fill=255)
            oled.image(image)
            oled.show()
            sleep(.1)
        elif HighCPU > 75:
            new_Temp = round(get_cpu_temp(),1)
            CPUTemp = str( new_Temp )
            HighCPU = float(CPUTemp)
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            HighCPUvariable = 1
            #image.paste(alertimage,(0,0))
            msg1 = "SYSTEM SHUTDOWN"
            msg1_size = draw.textsize(msg1, font=font_system)
            draw.text(((width-msg1_size[0])/2, top+10), msg1, font=font_system, fill=255)
            msg1 = "CPU OVER TEMPERATURE"
            msg1_size = draw.textsize(msg1, font=font)
            draw.text(((width-msg1_size[0])/2, top+40), msg1, font=font, fill=255)
            draw.text((47, top+50), str( new_Temp ) + chr(0xB0) +"C", font=font, fill=255)
            oled.image(image)
            oled.show()
            sleep(.1)
            Shutdown()
        else:
            HighCPUvariable = 0
            
            if HighCPUvariable == 0:

                try:
                    f = open('/dev/shm/runcommand.log', 'r', -1,"utf-8")
                    # except FileNotFoundError:
                except IOError:
                    try:
                        infoimg = Image.open("/home/pi/RetroPie-OLED/SysInfo.png").convert('1')
                    except IOError:
                        draw.rectangle((0,0,width,height), outline=0, fill=0)
                        msg1 = "SYSTEM INFO"
                        msg1_size = draw.textsize(msg1, font=font)
                        draw.text(((width-msg1_size[0])/2, top), msg1, font=font, fill=255)
                        # Icons
                        # Icon temperator
                        draw.text((5, top+7),    chr(62152),  font=font_icon, fill=255)
                        # Icon CPU
                        draw.text((65, top+12), chr(61614),  font=font_icon2, fill=255)
                        # Icon memory
                        draw.text((65, top+33), chr(62171),  font=font_icon3, fill=255)
                        # Icon disk
                        draw.text((5, top+33), chr(61888),  font=font_icon2, fill=255)
                        # Icon Wifi
                        #draw.text((0, top+52), chr(61931),  font=font_icon2, fill=255)
                    
                        draw.text((15, top+48),    str(IP,'utf-8'),               font=font_system, fill=255)
                        draw.text((20, top+8),     CPUTemp,                       font=font,        fill=255)
                        draw.text((45, top+8),     str('CPU'),                    font=font,        fill=255)
                        draw.text((20, top+18),    GPUTemp,                       font=font,        fill=255)
                        draw.text((45, top+18),    str('GPU'),                    font=font,        fill=255)                    
                        draw.text((82, top+8),     str(CPU,'utf-8'),              font=font,        fill=255)                    
                        draw.text((82, top+18),    CPUSpeed,                      font=font,        fill=255)
                        draw.text((20, top+29),    str(DiskFree,'utf-8'),         font=font,        fill=255)
                        draw.text((45, top+29),    str('GB'),                     font=font,        fill=255)                    
                        draw.text((20, top+39),    str(DiskUsed,'utf-8'),         font=font,        fill=255)
                        draw.text((45, top+39),    str('GB'),                     font=font,        fill=255)                    
                        draw.text((82, top+29),    str(MemUsage,'utf-8'),         font=font,        fill=255)
                        draw.text((111, top+29),   str('MB'),                     font=font,        fill=255)                    
                        draw.text((82, top+39),    str(MemTotal,'utf-8'),         font=font,        fill=255)
                        draw.text((111, top+39),   str('MB'),                     font=font,        fill=255)                    

                        oled.image(image)
                        oled.show()
                        sleep(.1)
                        pass
                    else:
                        draw.rectangle((0,0,width,height), outline=0, fill=0)
                        if intro == 0:
                            image.paste(raspyimg,(0,0))
                            oled.image(image)
                            oled.show()
                            intro = 1
                            sleep(3)
                        elif intro == 1:
                            draw.rectangle((0,0,width,height), outline=0, fill=0)
                            image.paste(retroarchimg,(0,0))
                            oled.image(image)
                            oled.show()
                            intro = 2
                            sleep(3)
                        elif intro == 2:
                            draw.rectangle((0,0,width,height), outline=0, fill=0)
                            image.paste(titleimg,(0,0))
                            oled.image(image)
                            oled.show()
                            intro = 3
                            sleep(3)
                        elif intro == 3:
                            draw.rectangle((0,0,width,height), outline=0, fill=0)
                            image.paste(infoimg,(0,0))
                            # Icons
                            # Icon temperator
                            draw.text((5, top+7),    chr(62152),  font=font_icon, fill=255)
                            # Icon CPU
                            draw.text((65, top+12), chr(61614),  font=font_icon2, fill=255)
                            # Icon memory
                            draw.text((65, top+33), chr(62171),  font=font_icon3, fill=255)
                            # Icon disk
                            draw.text((5, top+33), chr(61888),  font=font_icon2, fill=255)
                            # Icon Wifi
                            #draw.text((0, top+52), chr(61931),  font=font_icon2, fill=255)
                    
                            draw.text((15, top+48),    str(IP,'utf-8'),               font=font_system, fill=255)
                            draw.text((20, top+8),     CPUTemp,                       font=font,        fill=255)
                            draw.text((45, top+8),     str('CPU'),                    font=font,        fill=255)
                            draw.text((20, top+18),    GPUTemp,                       font=font,        fill=255)
                            draw.text((45, top+18),    str('GPU'),                    font=font,        fill=255)                    
                            draw.text((82, top+8),     str(CPU,'utf-8'),              font=font,        fill=255)                    
                            draw.text((82, top+18),    CPUSpeed,                      font=font,        fill=255)
                            draw.text((20, top+29),    str(DiskFree,'utf-8'),         font=font,        fill=255)
                            draw.text((45, top+29),    str('GB'),                     font=font,        fill=255)                    
                            draw.text((20, top+39),    str(DiskUsed,'utf-8'),         font=font,        fill=255)
                            draw.text((45, top+39),    str('GB'),                     font=font,        fill=255)                    
                            draw.text((82, top+29),    str(MemUsage,'utf-8'),         font=font,        fill=255)
                            draw.text((111, top+29),   str('MB'),                     font=font,        fill=255)                    
                            draw.text((82, top+39),    str(MemTotal,'utf-8'),         font=font,        fill=255)
                            draw.text((111, top+39),   str('MB'),                     font=font,        fill=255)                    

                            oled.image(image)
                            oled.show()
                            sleep(.1)
                else:
                    system = f.readline()
                    system = system.replace("\n","")
                    systemMap = {
                        "c64":"Commodore 64",
                        "dosbox":"DOS BOX",
                        "arcade":"Arcade Game",
                        "fba":"FinalBurn Alpha",
                        "gba":"GameBoy Advance",
                        "kodi":"KODI",
                        "mame-mame4all":"MAME4ALL",
                        "mame-advmame":"AdvanceMAME",
                        "mame-libretro":"lr-MAME",
                        "megadrive":"SEGA Megadrive",
                        "genesis":"SEGA Genesis",
                        "mastersystem":"SEGA Mastersystem",
                        "msx":"MSX",
                        "nes":"Famicom",   # Nintendo Entertainment System
                        "psp":"PSPortable",    # PlayStation Portable
                        "psx":"Playstation",
                        "ports":"Ports",
                        "snes":"Super Famicom", # Super Nintendo Entertainment System
                        "notice":"TURN OFF",
                    }
                    systemicon = systemMap.get(system, "none")
                    if systemicon != "none" :
                        icon = Image.open("/home/pi/RetroPie-OLED/system/" + system + ".png").convert('1')
                        system = systemicon
                    rom = f.readline()
                    rom = rom.replace("\n","")
                    game = rom
                    game_length = len(game)
                    romfile = f.readline()
                    romfile = romfile.replace("\n","")
                    f.close()
                    new_Temp = round(get_cpu_temp(),1)
                    info = str( new_Temp ) + chr(0xB0) +"C"

                    if game_length == 0 :
                        game = romfile
                        game_length = len(game)
                    try:
                        titleimg = Image.open("/home/pi/RetroPie-OLED/gametitle/" + romfile + ".png").convert('1')
                        # except FileNotFoundError:
                    except IOError:
                        #print "no title image"
                        draw.rectangle((0,0,width,height), outline=0, fill=0 )
                        system_size = draw.textsize(system, font=font_system)
                        gname = textwrap.wrap(game, width=10)

                        if game_length > 16:
                            current_h, text_padding = 18, 0
                        else :
                            current_h, text_padding = 26, 2
                            draw.rectangle((0,0,width,height), outline=0, fill=0 )
                        if systemicon != "none" :
                            image.paste(icon,(0,0))
                        else :
                            draw.text( ((width-system_size[0])/2, top), system, font=font_system, fill=255 )
                        for line in gname:
                            #print "text name display"
                            gname_size = draw.textsize(line, font=font_rom)
                            draw.text(((width - gname_size[0])/2, current_h), line, font=font_rom, fill=255)
                            current_h += gname_size[1] + text_padding
                        if system == "TURN OFF":
                            #draw.text((96, top+54), info , font=fonte_rom, fill=255)
                            draw.text((0, top+54), ipaddr, font=fonte_rom, fill=255)
                        oled.image(image)
                        oled.show()
                        sleep(3)
                        pass
                    else:
                        draw.rectangle((0,0,width,height), outline=0, fill=0 )
                        image.paste(titleimg,(0,0))
                        if system == "TURN OFF":
                            draw.rectangle((0,0,width,height), outline=0, fill=0)
                            image.paste(infoimg,(0,0))
                            # Icons
                            # Icon temperator
                            draw.text((5, top+7),    chr(62152),  font=font_icon, fill=255)
                            # Icon CPU
                            draw.text((65, top+12), chr(61614),  font=font_icon2, fill=255)
                            # Icon memory
                            draw.text((65, top+33), chr(62171),  font=font_icon3, fill=255)
                            # Icon disk
                            draw.text((5, top+33), chr(61888),  font=font_icon2, fill=255)
                            # Icon Wifi
                            #draw.text((0, top+52), chr(61931),  font=font_icon2, fill=255)
                    
                            draw.text((15, top+48),    str(IP,'utf-8'),               font=font_system, fill=255)
                            draw.text((20, top+8),     CPUTemp,                       font=font,        fill=255)
                            draw.text((45, top+8),     str('CPU'),                    font=font,        fill=255)
                            draw.text((20, top+18),    GPUTemp,                       font=font,        fill=255)
                            draw.text((45, top+18),    str('GPU'),                    font=font,        fill=255)                    
                            draw.text((82, top+8),     str(CPU,'utf-8'),              font=font,        fill=255)                    
                            draw.text((82, top+18),    CPUSpeed,                      font=font,        fill=255)
                            draw.text((20, top+29),    str(DiskFree,'utf-8'),         font=font,        fill=255)
                            draw.text((45, top+29),    str('GB'),                     font=font,        fill=255)                    
                            draw.text((20, top+39),    str(DiskUsed,'utf-8'),         font=font,        fill=255)
                            draw.text((45, top+39),    str('GB'),                     font=font,        fill=255)                    
                            draw.text((82, top+29),    str(MemUsage,'utf-8'),         font=font,        fill=255)
                            draw.text((111, top+29),   str('MB'),                     font=font,        fill=255)                    
                            draw.text((82, top+39),    str(MemTotal,'utf-8'),         font=font,        fill=255)
                            draw.text((111, top+39),   str('MB'),                     font=font,        fill=255)
                    
                        oled.image(image)
                        oled.show()
                        sleep(.1)

if __name__ == "__main__":
    import sys

    try:
        main()

    # Catch all other non-exit errors
    except Exception as e:
        sys.stderr.write("Unexpected exception: %s" % e)
        sys.exit(1)

    # Catch the remaining exit errors
    except:
        sys.exit(0)
