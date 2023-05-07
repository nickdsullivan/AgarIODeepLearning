#Author Nicholas Sullivan
#nickdsullivan@gmail.com





#This file handles browser functions (like opening the window) as menu navigation. 
#it also handles checking if the menu is on screen which is a simple way detect death
#Another potential way is just to take an image but I am pretty sure that this is fastest

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
#this function takes a window_size and returns a browser object
def initBrowser(window_size,window_pos=(0,0),options=None):
	#First we have to get the webdriver
	if options != None:
		browser = webdriver.Chrome(chrome_options=options)
		
		time.sleep(20)
		browser.switch_to.window(browser.window_handles[1])
		browser.close()
		browser.switch_to.window(browser.window_handles[0])
	else:
		browser = webdriver.Chrome()
	#set the size of the window
	browser.set_window_size(window_size[0],window_size[1]+95)
	browser.set_window_position(window_pos[0],window_pos[1])




	return browser

#Opens a given webpage.  Defaults to agar.io = hype
def openPage(browser,webpage='http://agar.io',adblockWindow=False):
	#Open the webpage
	browser.get(webpage)
	#If we used a adblock then the donation page will come up
	#If so then way till it does then close it

		

#This function navigates the agar.io menu
#Inputs
#browser: the browser with the page loaded on it
#maxIter: how many tries until you raise an error
#timeBetweenTries: Time between each try
#timeAfterClickingPlay: How long until this method should return after a success.  
#For agar.io it is after a 30sec ad so waiting 35 seconds helps

def startAgarioGame(browser,maxIter=100,timeBetweenTries = 2,timeAfterClickingPlay = 35):
	#Keep track if we are still in the menu kind of
	button = 0
	#current itteration
	count = 0
	while count < maxIter:
		#increment count
		count = count +1
		#This waits inbetween tries
		time.sleep(timeBetweenTries)
		
		try:
			#Click on the settings tab
			browser.find_element('xpath','//*[@id="settingsButton"]').click()
			#Click on the no skins option for better image recognizion
			noSkins = browser.find_element('xpath','//*[@id="mainui-settings"]/div[2]/div[3]/div[1]')
			noSkins.click()
			#Click on the no names option for better image recognizion
			browser.find_element('xpath','//*[@id="mainui-settings"]/div[2]/div[3]/div[2]').click()

			# TODO this is commented because I think we need to try and detect death and get score
			#This will skip the ending stats 
			#browser.find_element('xpath','//*[@id="mainui-settings"]/div[2]/div[3]/div[6]').click()

			#Init mouse clicks
			ac = ActionChains(browser)
			#Agario closes the settings menu with a click outside the setting menu
			#So go to the noSkins element and click -100 px away 
			ac.move_to_element(noSkins).move_by_offset(-100, 0).click().perform()

			#Now that the settings menu is out of the way click the play button
			browser.find_element('xpath','//*[@id="play"]').click()
			time.sleep(timeAfterClickingPlay)
		except:
			try:
				#If the setting menu is open then close it
				ac = ActionChains(browser)
				ac.move_to_element(noSkins).move_by_offset(-100, 0).click().perform()
			except:
				#If the settings menu is not open then most of the time (if it failed on the noSkins than it won't but I doubt that will happen) 
				#it will throw an error when trying to access noSkins.  
				#Most of the errors will come from the first access or something after the menu clicks 
				#Obviously TODO fix this thing moron so it works better.  
				continue
			continue
			#I know the above looks bad give me a break

		return True
	if count > maxIter:
		raise RuntimeError("Maximium iterations reached when trying to navigate agario website") from error
