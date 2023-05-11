Author Nicholas Sullivan
Email nickdsullivan@gmail.com, d.sullivan@wustl.edu

**************************************************************************************
INTRODUCTION

About:  This project uses a combination of image recognition, web navigation and deep learning to play the game agar.io.  There is a more in depth explaination of each.  I could not find any training data for this game so the usual gradient descent is not going to cut it.  So we are using a genetic algorithm!  The difference between say https://wagenaartje.github.io/agario-ai/ and my algorithm is that I will be playing against real humans and it will have the full range of contols.  I might use transfer learning with his genomes.  We will see.  
If you do know what Agar.io what that is here is a quick summary:
Agar.io is a simple online multiplayer game. You play as a blob(s) and the goal is to gain mass.  You can do this in two ways.  First you can eat small dots that spawn randomely throughout the playing field.  Secondly you can eat other players and gain their mass.  You can only eat other players if you are bigger than them.  
**************************************************************************************


**************************************************************************************
POTENTIAL BUGS FOR USERS

Some difficulties you may run into when trying to run this on your machine:  

I used exclusively have used chrome for this project.  Not sure how this will work for firefox. 

I am currently using an M1 mac with rosetta.  OS: MacOS Monterey V12.6.3.  I am not sure how this will work with windows.  In any case I will upload a video showing the progress.

Selenium requires you to give it a path to your own chrome application.  Make sure this is installed and pathed correctly.  I also added an adblocker to the chrome.  Specifically "adblock" id "gighmmpiobklfepjocnamgkkbiglidom".  I have uploaded the crx and think this will be fine for other users but I am not sure.  This may be tricky to debug if it doesn't work.  But it is vital that you do this because Agario has some of the worst ads for any game.  

**************************************************************************************


**************************************************************************************
WEBSITE NAVIGATION

This is done using selenium 4.9.0

Because agar.io has many on screen ads which block the vision of the player(and have many symbols that make it more difficult for computer vision to solve) it is important install an ad blocker.  This has been done.  After that the menu navigates to the settings where the proper settings are applied.  These are no names, dark theme, no colors(Because we greyscale it anyway), no skins, and skipping the stats after.


**************************************************************************************
Image recognition.  

Because we are learning a genetic algo and already don't have enough data, I have done a lot of feature engineering on the inputs.   We first take the and use cv2 canny filter (after blurring) for finding the edges.  We then take that image and then use cv2's blob recognition to find the blobs.  These blobs are the final inputs to the network.  This total process take .12 seconds

We also find the score every few seconds by using pytesseract.  Because the score in agar is not a component.  This takes longer than the other image process (and we need it less) so every 10 seconds.  (I know my WASHU CSE132 would be proud of me for using delta time)
That way we know the fitness every few seconds.  If this fails twice in a row then we know we have died and need to start the game again.  Our final fitness will be that score for each of the AI players.  




**************************************************************************************
OUTPUTS FOR THE NETWORK


Here are controls(outputs of the network):

Movement.  You blob always moves towards the direction of your mouse. Because the blob is always centered on your screen I simply had the network output a 0-1 representing at which the mouse should be at.  This can be easily converted to real world cordinates y=sin(2pi (number)), x = cos(2pi (number)).  

Spliting This splits your blob into 2 blobs (both controlled the same way).  When doing so the new blob will shoot out with speed thus allowing you to capture smaller blobs running away from you. (A key part of this game is that smaller blobs are faster).  This output's activation function is simply 0 {a<0} and 1 {z>=0}.  As previously stated this game has no training data and thus 

We will not be  Ejecting mass.  Too complex.   

The network is a simple NN with a 




