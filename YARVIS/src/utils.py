from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
import time
import datetime
import os
import sys

''' This class opens firefox using geckodriver and do some specific functions
inside the browser '''

class YarvisBrowser:
    # Creating the webdriver (and open the browser) and the channels (active tabs)
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.google.com")
        self.driver.find_element_by_id("SIvCob").find_element_by_tag_name("a").click()

        self.driver.execute_script("window.open('about:blank');")
        self.driver.execute_script("window.open('https://www.youtube.com');")
        self.channels = {}
        self.channels["google"] = self.driver.window_handles[0]
        self.channels["youtube"] = self.driver.window_handles[1]
        self.channels["dummy"] = self.driver.window_handles[2]

    # Switch to a different tab
    def switch_tab(self,tab_name):
        try:
            if tab_name in self.channels:
                self.driver.switch_to.window(self.channels[tab_name])
        except:
            print("Could not switch tabs")

    # Search something on google
    # Show results in the browser
    def search_on_google(self,query):
        url = f"https://www.google.com/search?q={query.replace(' ','+')}"
        try:
            self.driver.switch_to.window(self.channels["google"])
            self.driver.get(url)
        except:
            print("could not search on google")
    
    # Play a song on youtube (tab)
    def play_song_youtube(self,name_of_song):
        url = f"https://www.youtube.com/results?search_query={name_of_song.replace(' ','+')}"
        try:
            self.driver.switch_to.window(self.channels["youtube"])
            self.driver.get(url)
            self.driver.find_element_by_id("video-title").click()
        except:
            print("Could not play song")
    
    # Pause or resume the current music being played in youtube
    def pause_resume_song_youtube(self):
        try:
            self.driver.switch_to.window(self.channels["youtube"])
            self.driver.find_element_by_id("movie_player").click()
            # self.driver.find_element_by_tag_name("body").send_keys(Keys.SPACE)
        except:
            print("No video being played")

    # Skip ad on youtube
    def skip_ad_youtube(self):
        try:
            self.driver.switch_to.window(self.channels["youtube"])
            self.driver.find_element_by_class_name("ytp-ad-skip-button-container").find_element_by_tag_name("button").click()
        except:
            print("No skip ad button")

    # Get weather information from google search
    def get_weather_data(self):
        data_ = None
        try:
            self.driver.switch_to.window(self.channels["dummy"])
            self.driver.get("https://www.google.com/search?channel=fs&client=ubuntu&q=weather")
            temp = self.driver.find_element_by_id("wob_tm").text
            loc = self.driver.find_element_by_id("wob_loc").text
            weather = self.driver.find_element_by_id("wob_dcp").text
            precipitation = self.driver.find_element_by_id("wob_pp").text
            humidity = self.driver.find_element_by_id("wob_hm").text
            wind = self.driver.find_element_by_id("wob_ws").text

            data_ = {}
            data_["temperature"] = temp
            data_["location"] = loc
            data_["weather"] = weather
            data_["precipitation"] = precipitation
            data_["humidity"] = humidity
            data_["wind"] = wind
        except:
            print("Could not get weather")
        return data_
    
    # Get weather information from google search and send the information
    def get_weather(self):
        sentence_ = None
        try:
            data_ = self.get_weather_data()
            sentence_ = f"Today's temperature at {data_['location']} is {data_['temperature']} Celsius degrees and the weather is {data_['weather']} with precipitation {data_['precipitation']} and humidity {data_['humidity']}"
        except:
            print("Could not get weather")

        return sentence_

    # Get definitions of stuff (using google search)
    def get_definition(self,word_or_sentence):
        definition_ = None
        url = f"https://www.google.com/search?q=what+is+{word_or_sentence.replace(' ','+')}"
        try:
            self.driver.switch_to.window(self.channels["google"])
            self.driver.get(url)
            definition_ = self.driver.find_element_by_class_name("kno-rdesc").find_element_by_tag_name("span").text
        except:
            print("Could not search for definition")
            definition_ = f"Could not find definition for {word_or_sentence}"
        return definition_

    def search_location_and_directions(self,loc):
        try:
            self.driver.switch_to.window(self.channels["dummy"])
            self.driver.get("https://www.google.com/maps")
            self.driver.find_element_by_id("searchboxinput").send_keys(loc)
            self.driver.find_element_by_id("searchbox-directions").click()
            tmp_ = self.driver.find_elements_by_class_name("tactile-searchbox-input")[3]
        except:
            print("no location found")


    def get_my_location(self):
        loc = None
        try:
            self.driver.switch_to.window(self.channels["dummy"])
            self.driver.get("https://www.google.com/maps")
            self.driver.implicitly_wait(3)
            loc_ = self.driver.current_url.replace("@","").split(["/"])[-1].split(",")
            loc = {}
            loc["latitude"] = loc_[0]
            loc["longitude"] = loc_[1]
            loc["high"] = loc[2]
        except:
            print("could not get my location")
        
        return loc
    
    # Translate from english to any other language (working on...)
    def translate_from_english(self,word_or_sentence,lang):
        url = f"https://www.deepl.com/translator#en/ja/{word_or_sentence}"
        try:
            self.driver.switch_to.window(self.channels["dummy"])
            self.driver.get(url)
            self.driver.implicitly_wait(3)
            ans = self.driver.find_element_by_id("target-dummydiv").text
        except:
            ans = "Sorry, not able to translate it"

        return ans


''' This is a simple interface for yarvis to interact with the operative system
'''
class YarvisSystem:
    def __init__(self):
        pass

    # Get the time from computer's local time
    def get_time(self):
        tmp_ = datetime.datetime.now()
        sentence_ = f"The time is {tmp_.strftime('%H %M')}"
        return sentence_
    
    # Get the date from computer's local time
    def get_date(self):
        tmp_ = datetime.datetime.now()
        sentence_ = f"Today is {tmp_.strftime('%A %B %C %Y')}"
        return sentence_

    # Get the date and time from computer's local time
    def get_date_time(self):
        tmp_ = datetime.datetime.now()
        sentence_ = f"The date is {tmp_.strftime('%A %B %C %Y')} and the time is {tmp_.strftime('%H %M')}"
        return sentence_

    def open_emacs(self):
        os.system("emacs &")

    def open_gedit(self):
        os.system("gedit &")

    def open_folder(self):
        os.system("nautilus &")

    def open_facebook(self):
        os.system("firefox https://www.facebook.com")

    def open_youtube(self):
        os.system("firefox https://www.youtube.com")

    def open_mail(self):
        os.system("firefox https://www.gmail.com")

