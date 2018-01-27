#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########LIBRARIES###########
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import serial
import csv
import codecs

def send_email(ph_val,nitrate_val,phosphate_val, oxygen_val, temperature_val, w_eng, w_chi, site):
    ph_val = str(ph_val)
    oxygen_val = str(oxygen_val)
    nitrate_val= str(nitrate_val)
    phosphate_val = str(phosphate_val)
    temperature_val = str(temperature_val)
    w_eng = str(w_eng)
    w_chi = str(w_chi)
    site=str(site)
    
    fromaddr = "shivashanti89@gmail.com"
    toaddr = "cbollig10@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Water Quality Level"
    body_chi = "您好,"+"\n"\
    +"住接近 " + site + " ,今天的水質：\n\n"\
    +"pH值:\t\t" + ph_val + "\t"+"安全值為 6.5-8.5"+"\n\n"\
    +"氧:\t\t" + oxygen_val + "\t"+"安全值需低於 110%"+"\n\n"\
    +"硝酸鹽:\t\t" + nitrate_val + "\t"+"安全值需低於 4.0"+"\n\n"\
    +"磷酸鹽:\t\t" + phosphate_val + "\t"+"安全值需低於 0.1"+"\n\n"\
    +"水溫:\t\t" + temperature_val + "\t"+"安全值為 11-30 °C"+"\n\n"\
    +"危險值為:\t\t"+ w_chi
    
    body_eng = "Dear Sir/Madam,"+"\n"\
    +"Residents close to " + site + " ,here is your water quality.\n\n"\
    +"pH:\t\t" + ph_val + "\t"+"safe levels are 6.5-8.5"+"\n\n"\
    +"Oxygen:\t\t" + oxygen_val + "\t"+"safe levels are below 110%"+"\n\n"\
    +"Nitrate:\t\t" + nitrate_val + "\t"+"safe levels are below 4.0"+"\n\n"\
    +"Phosphates:\t\t" + phosphate_val + "\t"+"safe levels are below 0.1"+"\n\n"\
    +"Water temperature:\t\t" + temperature_val + "\t"+"safe levels are between 11-30 °C"+"\n\n"\
    +"Danger level is:\t\t"+ w_eng
    
    body = body_chi + "\n\n" + body_eng
    msg.attach(MIMEText(body, 'plain'))
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "v1sa98b9$")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def send_R():
    ser = serial.Serial("/dev/tty.KTM3887-DevB", 9600)
    written_R=ser.write('R')

send_email(9,5,0.3,120,35, "RED", "紅色", "台北101")
send_R()
