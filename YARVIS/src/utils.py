from selenium import webdriver
import selenium
import time
import datetime

''' This is are just a bunch of functions to do some specific tasks mostly using
selenium and a webdriver to search or do something in the browser '''

# Get and configure webdriver (firefox)
def get_driver():
    driver = webdriver.Firefox()
    driver.get("http://www.google.com")
    driver.find_element_by_id("SIvCob").find_element_by_tag_name("a").click()

    driver.execute_script("window.open('https://www.youtube.com');")
    driver.execute_script("window.open('about:blank');")

    channels = {}
    channels["google"] = driver.window_handles[0]
    channels["youtube"] = driver.window_handles[1]
    channels["dummy"] = driver.window_handles[2]
    
    return driver, channels
    
# Get date and time from local time
def get_date_time():
    tmp_ = datetime.datetime.now()
    
    data_ = {}
    data_["year"] = tmp_.year
    data_["month"] = tmp_.month
    data_["day"] = tmp_.day
    data_["hour"] = tmp_.hour
    data_["minute"] = tmp_.minute
    
    sentence_ = f"The date is {tmp_.strftime('%A %B %C %Y')} and the time is {tmp_.strftime('%H %M')}"
    return data_, sentence_

# Play a song in youtube (click the first answer in the query)
def play_song_youtube(driver,channels,name_of_song):
    url = f"https://www.youtube.com/results?search_query={name_of_song.replace(' ','+')}"
    driver.switch_to.window(channels["youtube"])
    driver.get(url)
    driver.find_element_by_id("video-title").click()

# Get weather information from google search
def get_weather(driver, channels):
    driver.switch_to.window(channels["google"])
    driver.get("https://www.google.com/search?channel=fs&client=ubuntu&q=weather")
    temp = driver.find_element_by_id("wob_tm").text
    loc = driver.find_element_by_id("wob_loc").text
    weather = driver.find_element_by_id("wob_dcp").text
    precipitation = driver.find_element_by_id("wob_pp").text
    humidity = driver.find_element_by_id("wob_hm").text
    wind = driver.find_element_by_id("wob_ws").text

    data_ = {}
    data_["temperature"] = temp
    data_["location"] = loc
    data_["weather"] = weather
    data_["precipitation"] = precipitation
    data_["humidity"] = humidity
    data_["wind"] = wind
    
    sentence_ = f"Today's temperature at {loc} is {temp} Celsius degrees and the weather is {weather} with precipitation {precipitation} and humidity {humidity}"
    return data_, sentence_

# Get definitions of stuff (using google search)
def get_definition(driver,channels,word_or_sentence):
    driver.switch_to.window(channels["google"])
    url = f"https://www.google.com/search?q=what+is+{word_or_sentence.replace(' ','+')}"
    driver.get(url)
    try:
        ans = driver.find_element_by_class_name("kno-rdesc").find_element_by_tag_name("span").text
    except:
        ans = f"Could not find a definition for {word_or_sentence}"

    return ans
    
# Translate from english to any other language (working on...)
def translate(driver,channels,word_or_sentence):
    driver.switch_to.window(channels["dummy"])
    url = f"https://www.deepl.com/translator#en/ja/{word_or_sentence}"
    driver.get(url)
    driver.implicitly_wait(3)
    try:
        ans = driver.find_element_by_id("target-dummydiv").text
    except:
        ans = "Sorry, not ablet to translate it"
    
    return ans
