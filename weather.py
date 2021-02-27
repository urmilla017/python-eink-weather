#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd2in13
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import requests, json
import datetime

try:
    # initialize EPD class
    epd = epd2in13.EPD()
    epd.init(epd.FULL_UPDATE)

    epd.Clear(0xFF)

    einkImage = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), 255)
    drawImage = ImageDraw.Draw(einkImage)

    fontSmall = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 12)
    fontMedium = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 16)
    fontLarge = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)

    iconSizeSmall = ImageFont.truetype('icons/meteocons-webfont.ttf', 30)
    iconSizebig = ImageFont.truetype('icons/meteocons-webfont.ttf', 50)
    
    weather_icon_map = {
    "01d" : "B", "01n" : "C", "02d" : "H", "02n" : "I", 
    "03d" : "N", "03n" : "N", "04d" : "Y", "04n" : "Y", "09d" : "Q", "09n" : "Q", 
    "10d" : "R", "10n" : "R", "11d" : "0", "11n" : "0", "13d" : "S", "13n" : "S", 
    "50d" : "M", "50n" : "M", "wind" : "F", "sunrise" : "J", "sunset" : "K"  
	}
    
    api_key = "API_KEY"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "Boston"
    city = "Boston   "
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
		
    response = requests.get(complete_url)
    response_data = response.json()
    if response_data["cod"] != "404":

        data = response_data["main"]
        current_temperature = "{:.1f}".format(data["temp"] - 273.15) + "\u00b0 C"
        weather_data = response_data["weather"]
        weather_description = weather_data[0]["description"]
        
        system_info = response_data["sys"]
        sunrise = system_info["sunrise"]
        sunset = system_info["sunset"]

        drawImage.text((10, 10), datetime.datetime.now().strftime("%d %B %Y"), font = fontSmall, fill = 0)
        drawImage.text((150, 10), str(city), font = fontMedium, fill = 0)
        drawImage.text((10, 40), str(current_temperature), font = fontLarge, fill = 0)
        drawImage.text((10, 80), str(weather_description).title(), font = fontLarge, fill = 0)
        drawImage.text((180, 70), datetime.datetime.utcfromtimestamp(sunrise).strftime("%H:%M %p"), font = fontSmall, fill = 0)
        drawImage.text((180, 110), datetime.datetime.utcfromtimestamp(sunset).strftime("%H:%M %p"), font = fontSmall, fill = 0)

        w3, h3 = iconSizebig.getsize(weather_icon_map[weather_data[0]["icon"]])
        drawImage.text((100, 30), weather_icon_map[weather_data[0]["icon"]], font = iconSizebig, fill = 0)
        drawImage.text((190, 40), weather_icon_map["sunrise"], font = iconSizeSmall, fill = 0)
        drawImage.text((190, 80), weather_icon_map["sunset"], font = iconSizeSmall, fill = 0)
          
        epd.display(epd.getbuffer(einkImage))
    epd.sleep()
        
except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()