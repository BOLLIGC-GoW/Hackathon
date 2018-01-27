#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########LIBRARIES###########
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

###import serial
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
    
def send_Y():
    ser = serial.Serial("/dev/tty.KTM3887-DevB", 9600)
    written_Y=ser.write('Y')
    
def send_G():
    ser = serial.Serial("/dev/tty.KTM3887-DevB", 9600)
    ser.write('G')

count = 0
totalString = ""
dictKeys = {'site','latitude','longitude','date','namePhosphate','totalPhosphate','nameNitrates','nitrates','nameOxygen','dissolvedOxygen','namePh','ph','nameWaterTemp','waterTemperature'}
totalDict = []

with codecs.open('WQXDam_20160923232750.csv', 'rb') as fIn:
	fieldnames =['SiteName','SiteEngName','DamName','County','Township','TWD97Lon','TWD97Lat','TWD97TM2X','TWD97TM2Y','SampleDate','SampleLayer','SampleDepth','ItemName','ItemEngName','ItemEngAbbreviation','ItemValue','ItemUnit']
	reader = csv.DictReader(fIn)
	for row in reader:
	    	#for i in row[0:]:
	       #	print str(i).decode('UTF-8')
		count = count + 1
		if(count == 3):
			namePhosphate = str(row['ItemName'])+"("+str(row['ItemEngName'])+")"
			totalPhosphate = row['ItemValue']
		if(count == 4):
			nameOxygen = str(row['ItemName'])+"("+str(row['ItemEngName'])+")"
			percentageOxygen  = row['ItemValue']
		if(count == 5):
			nameNitrates = str(row['ItemName'])+"("+str(row['ItemEngName'])+")"
			nitrates = row['ItemValue']

		if(count == 13):
			namePH = str(row['ItemName'])+"("+str(row['ItemEngName'])+")"
			ph = row['ItemValue']
		if(count == 15):
			nameWaterTemp = str(row['ItemName'])+"("+str(row['ItemEngName'])+")"
			waterTemperature = row['ItemValue']
		if(count == 16):
			site = str(row['County'])+" | "+str(row['Township'])
			latitude = row['TWD97Lat']
			longitude = row['TWD97Lon']
			date  = row['SampleDate']
			runningString =  site+" Lat:"+str(latitude)+" Long:"+" "+str(longitude)+" Date:"+str(date)+"\n"+namePhosphate+": "+str(totalPhosphate)+"\n"+nameNitrates+": "+str(nitrates)+"\n"+nameOxygen+": "+str(percentageOxygen)+"\n"+namePH+": "+str(ph)+"\n"+nameWaterTemp+": "+str(waterTemperature)+"\n\n"
			count = 0
			print runningString
'''			totalDict.append({'site':site,'latitude':latitude,'longitude':longitude,'date':date,'namePhosphate':namePhosphate,'totalPhosphate':totalPhosphate,'nameNitrates':nameNitrates,'nitrates':nitrates,'nameOxygen':nameOxygen,'percentageOxygen':percentageOxygen,'namePh':namePH,'ph':ph,'nameWaterTemp':nameWaterTemp,'waterTemperature':waterTemperature})
    '''
fIn.close()
'''	for value in totalDict:
		if value['totalPhosphate'] >= 0.05 or value['percentageOxygen'] >= 108.0 or value['nitrates'] >= 0.1:
			send_email(value['ph'],value['nitrates'],value['totalPhosphate'],value['percentageOxygen'],value['waterTemperature'], "YELLOW", "黃色", value['site'])
			send_Y()
		
		elif value['ph'] <= 6.5 or value['ph'] >= 8.5 or value['totalPhosphate'] >= 0.01 or value['percentageOxygen'] >= 110.0 or value['nitrates'] >= 4.0:
			send_email(value['ph'],value['nitrates'],value['totalPhosphate'],value['percentageOxygen'],value['waterTemperature'], "RED", "紅色", value['site'])
			send_R()
        else:
            send_G()
##TESTING'''
    

