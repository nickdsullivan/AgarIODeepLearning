#Author Nicholas Sullivan
#nickdsullivan@gmail.com


#This controls the main game
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
import time
import os.path
import cv2
import browserFunctions as bf
from AgarioGameController import AgarioGameController


######################################
# CONSTANTS

## Size sets the size of the window  
window_size = (800,800)


######################################

######### AD BLOCK STUFF. UNCOMMENT IF YOU HAVE DONE THIS STUFF #########
chrome_options = Options()
#This is for ad block Need to download your own version of the crx file
file = '~/Library/Application Support/Google/Chrome/Default/Extensions/gighmmpiobklfepjocnamgkkbiglidom/5.6.0_0.crx'
chrome_options.add_extension(file);
######################################


#Frist get the selinium browser object
browser = bf.initBrowser(window_size, options=chrome_options)
bf.openPage(browser=browser,webpage='http://agar.io')
game = AgarioGameController(browser)

#Next we open agar.io
#bf.openPage(browser=browser,webpage='http://agar.io')

