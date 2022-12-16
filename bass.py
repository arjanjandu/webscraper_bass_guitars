from csv import writer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as E
import time 
import requests
from bs4 import BeautifulSoup
import csv
import os
import os.path
from PIL import Image #pip install pillow 


class Bass:
    

    def __init__(self):
        self.driver = Chrome('./chromedriver')
        #self.driver = Chrome('./chromedriver')
        self.folder_name = "GuitarGuitar_Pictures"
        self.folder_name2 = "Bass_collected"

    def makefolder(self,folder_path):
        # Check if the folder exists
        if not os.path.exists(folder_path):
                # Create the folder if it does not exist
                os.makedirs(folder_path)
                # Assign the folder name to a variable
                self.foldercreated = folder_path
        else:
                # If the folder already exists, create a new folder with a revision update
                revision_number = 1
                while os.path.exists(folder_path + "_rev" + str(revision_number)):
                        revision_number += 1
                os.makedirs(folder_path + "_rev" + str(revision_number))
                # Assign the revision folder name to a variable
                self.foldercreated = folder_path + "_rev" + str(revision_number)

    def click(self,xpath):
        self.xpath = xpath
        bass = self.driver.find_element(By.XPATH, '//*[@id="cd-primary-nav"]/li[10]/a') 
        bass.click() #select button
        time.sleep(1)

    def scroller(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")  # scrolls down
        time.sleep(1)

    def cheap_bass(self):
        self.makefolder(self.folder_name2)
        self.datafolder = ''
        self.datafolder = self.foldercreated

        self.driver.get("https://www.guitarguitar.co.uk/")
        
        self.click('//*[@id="cd-primary-nav"]/li[10]/a')
        self.click('//*[@id="product-list-ordering"]/select')
        self.click('//*[@id="product-list-ordering"]/select/option[3]')

        url = self.driver.current_url # get current url 
        
        response = requests.get(url)
        soup = response.content
        soup = BeautifulSoup(soup, 'html.parser')
        lists = soup.find_all('div', class_="product-inner")
        dir = self.foldercreated

        with open(os.path.join(dir,'Bass_GuitarGuitar.csv'), 'w', encoding='utf8', newline='') as f:
            thewriter = writer(f)
            header = ['Bass', 'Price', 'Time/Date'] 
            thewriter.writerow(header)
            
            for list in lists:   
                current_date = time.strftime("%H:%M:%S_%Y-%m-%d")
                title = list.find('h3', class_="qa-product-list-item-title").text.replace('\n','')
                title = title.replace('            ','')
                price = list.find('span', class_="product-main-price").text.replace('\n','')
                info = [title, price, current_date] 
                thewriter.writerow(info)  # write to csc
                #print(info)

    def get_images(self):  
        self.makefolder(self.folder_name)
        self.imagefolder = ''
        self.imagefolder = self.foldercreated
        images = self.driver.find_element(By.CLASS_NAME, 'products')
        image_cont = images.find_elements(By.CLASS_NAME, 'product')
        n = 0
        for image in image_cont:
            current_time = time.strftime("%H:%M:%S")
            current_date = time.strftime("%Y-%m-%d")
            photo = image.find_element(By.TAG_NAME, 'img')
            image_src = photo.get_attribute('data-src')
            name = image.find_element(By.CLASS_NAME, 'qa-product-list-item-title').text
            name = name.replace('/','')
            self.download_image(image_src, f'{self.imagefolder}/[{current_time} {current_date}] {name}.jpg')


    def download_image(self, img_url, fp):
        img_data = requests.get(img_url).content
        with open(fp, 'wb') as handler:
            handler.write(img_data)
                            
        
    def quit(self):
        time.sleep(2)
        self.driver.quit() # closes driver

    def user(self): # allows user to search through the data they have just scraped
        with open(f'{self.datafolder}/Bass_GuitarGuitar.csv', newline='') as f:
                reader = csv.reader(f)
                data = list(reader)
                #print(data)
                result = list(zip(*data)) # split tuple
                l, r, g = result # asign tuples
                user1 = input(f'please enter a number between 1 and 40 to see the bass and its price, \n1 being the cheapest 40 being the most expensive\n')
                user1 = int(user1)
                print(f'Bass: {l[user1]} \nPrice: {r[user1]}') 
                self.Bname = l[user1]
    
    def showpic(self):  # shows a picture of the data you have just scraped
        directory = self.imagefolder
        filename = f'{self.Bname}.jpg'
        # Get a list of all files in the directory
        files = os.listdir(directory)

        # Loop through the files in the directory
        for file in files:
        # Check if the file name contains the specified string
            if filename in file:
                # If the string is found, open the file using PIL's Image module
                image = Image.open(os.path.join(directory, file))
                image.show()

if __name__ == '__main__':
    play = Bass()
    play.cheap_bass()
    play.scroller()
    play.get_images()
    play.quit()
    user_input = input("input('would you like to search through the data you have just scraped? \n Enter: \n 1 for Yes \n 2 for No ")
    while user_input=='1':
        play.user()
        play.showpic()
        user_input = input("input('would you like to continue searching through the data you have just scraped? \n Enter: \n 1 for Yes \n 2 for No ")
        if user_input == '2':
            break 

        
    

    

    

    












