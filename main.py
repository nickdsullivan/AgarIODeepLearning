from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import numpy as np
import time
import os.path
import cv2
import browserFunctions as bf


######################################
# CONSTANTS

## Size sets the size of the window  
window_size = (800,800)


######################################



#Fist get the browser
browser = bf.initBrowser(window_size)
#Next we open agar.io
bf.openPage(browser=browser,webpage='http://agar.io')