# -*- coding: utf-8 -*-
"""
Created on Wed Apr 7 13:26:45 2021

@author: Kieran and Jacob
"""
import numpy as np #Import NumPy module
import cv2 #Import OpenCV module
import threading #Import Threading module
import speech_recognition as sr #Import Speech Recognition Module

running = True #Set running true
Output = ""
# try to open the colour.txt file and extract the colourmode number from it
try:
    ColourMode =  (int(open("Colour.txt","r").read()))
except: # if the file does not exist then default colour and write to file and inform the user
    with open("Colour.txt", "w") as file:
        file.write("1")
        ColourMode =  (int(open("Colour.txt","r").read()))
        print("error has been resolved please run program again")

def Speech():
    #Refer to globally referenced variable
    global running
    global Output
    global camera
    global needHelp
    global cursorX
    global cursorY
    
    #Keywords
    ActivateWord = "ok program" #Declare activation term   
    
    Keywords = ["start","options","quit","back","help","close","exit","save","reset","run","colour","select","drop","input"] #Declare Keywords
    
    #Keyword declarations 
    Start ="start"
    Options = "options"
    Quit = "quit"
    Back = "back"
    Help = "help"
    Close = "close"
    Exit = "exit"
    Save = "save" 
    Reset = "reset"
    Run ="run"
    Colour = "colour"
    Select = "select"
    Drop = "drop"
    Input = "input"
    
    BadCommand = "This command cannot be used right now, please try a different one." #To be printed when the user cannot use a certain command
    
    #This will run as long as the program is running 
    while running == True:
        
        if running == False: #Break out of while loop when program stopped
            break
        
        r = sr.Recognizer() #Speech recogniser                                                                              
        with sr.Microphone() as source: #Gets the current microphone                                                                       
            print("Speak:") #Prints speak into the console      
            
            if Output == "": #If the user hasnt spoken yet display this 
                Output = "Speak to enter a command:"
            #Output = "Speak:"                                 
            audio = r.listen(source)   #Listens for audio from the mic 
        try:    #If audio not recognised continue 
            print("Audio received: " + r.recognize_google(audio))
            #Output = "Audio received"
        except sr.UnknownValueError:
            print("Could not understand audio") 
            #Output = "Could not understand audio"
            continue
        except sr.RequestError as e: #If audio not recognised continue
            print("Could not request results; {0}".format(e))
            Output = "Could not understand audio"
            continue
        
        RawMicInput = r.recognize_google(audio) #Raw mic input with capital letters 
            
        MicInput = RawMicInput.lower() #Removes capital letters for later use
        if MicInput != "":
            Output = MicInput
        
        KeywordCount = 0 #Number of keywords in the sentence set to 0 

        if(ActivateWord in MicInput):
            #This will activate when the activation word (ok program) is heard by the mic
            print("Keyword Heard")
            
            # check if there is more than one KeyWord in MicInput 
            for x in range(0,len(Keywords)):
                    if  Keywords[x] in MicInput:
                        KeywordCount +=1
                
            #Checks if keywords are present in MicInput if not will print bad command 
            
            if Start in MicInput and KeywordCount == 1:
                print(BadCommand)
                
            if Options in MicInput and KeywordCount == 1:
                print(BadCommand)    
                
            if Quit in MicInput and KeywordCount == 1:
                WindowClose() #Call WindowClose function
                break  
                
            if Back in MicInput and KeywordCount == 1:
                print(BadCommand)
                
            if Help in MicInput and KeywordCount == 1: #sets needHelp to true when user says help
                if needHelp == False:
                    needHelp = True
                else: # if help is already true the bad command will be shown 
                    print(BadCommand)
                
            if Close in MicInput and KeywordCount == 1: # sets needHelp to false when user says close
                if needHelp == True:
                    needHelp = False
                else:
                    print(BadCommand) # if help is already false will show bad command
                
            if Exit in MicInput and KeywordCount == 1:
                WindowClose() #Call WindowClose function
                exec(open("Menu.py").read()) #Open Options Screen
                break
                
            if Save in MicInput and KeywordCount == 1:
                print(BadCommand)        
                
            if Reset in MicInput and KeywordCount == 1:
                print(BadCommand)   
                
            if Run in MicInput and KeywordCount == 1:
                print(BadCommand) 
                
            if Colour in MicInput and KeywordCount == 1:
                file = open("Colour.txt", "w")
                if ColourMode < 2:
                    file.write(str(ColourMode + 1))                      
                if ColourMode >= 2:
                    file.write("1")  
                file.close()
                WindowClose() #Call WindowClose function
                exec(open("Options.py").read()) #Open Task Screen       
                break 
                # will use the FindClosestButton def to activate the button the user is hovering over
            if Select in MicInput and KeywordCount == 1:
                closestButton = FindClosestButton()
                if closestButton == "colour":
                    file = open("Colour.txt", "w")
                    if ColourMode < 2:
                        file.write(str(ColourMode + 1))  
                    if ColourMode >= 2:
                        file.write("1")  
                    file.close()
                    WindowClose() #Call WindowClose function
                    exec(open("Options.py").read()) #Open Task Screen       
                    break
                elif closestButton == "exit":
                    WindowClose() #Call WindowClose function
                    exec(open("Menu.py").read()) #Open Options Screen
                    break
                elif closestButton == "null":
                    print("no button selected") 
                closestButton == "null"
                
            if Drop in MicInput and KeywordCount == 1: # cannot be used on this screen 
                print(BadCommand) 
                
            if Input in MicInput and KeywordCount == 1:
                print(BadCommand)  
               
            if KeywordCount > 1:
                print("Too many commands heard, please try again")                
            
def Screen():
    global camera #Refer to global running variable
    global running 
    global cursorX
    global cursorY
    global Output
    global needHelp
    global ColourMode
    # will use the colour mode value to set colours 
    if ColourMode == 1:
        LineColour = 0,255,0
        TextColour = 255,255,255
        BackgroundColour = 0,0,0
        
    if ColourMode == 2:
        LineColour = 255,0,0
        TextColour = 0,0,0
        BackgroundColour = 255,255,255
        
    img = np.zeros((1080,1920,3), np.uint8) #Create black image
    
    windowName = "Options" #Set window name
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN) #Creates window
    cv2.moveWindow(windowName, 0,0) #Move window to origin
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) #Set window to fullscreen
    
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) #Capture camera
    camera.set(3,1920) #Set camera width
    camera.set(4,1080) #Set camera height
    
    hand = cv2.CascadeClassifier("haarcascades/Hand.Cascade.1.xml")  #Stores hand cascase file
      
    cursorX = 0 #Sets initial cursor position values
    cursorY = 0
    
    needHelp = False
    
    while running == True:   #While speech recognition and camera are running 

        ret, frame = camera.read() #Main Camera Read
        
        cv2.rectangle(img,(0,0),(1920,1080),(BackgroundColour), cv2.FILLED) #Reset image background
   
        #Taskbar
        cv2.rectangle(img,(0,0),(1920,75),(LineColour),3) #Taskbar Border
        cv2.rectangle(img,(0,0),(250,75),(LineColour),3) #Exit Button
        cv2.putText(img,"Exit",(60,60),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Exit Text
        
        #MenuOptions  
        cv2.rectangle(img,(100,150),(700,350),(LineColour),3) #Option 1 Button
        cv2.putText(img,"Colour",(200,300),cv2.FONT_HERSHEY_SIMPLEX,4,(TextColour),2,cv2.LINE_AA) #Option 1 Text
        cv2.rectangle(img,(100,450),(700,650),(LineColour),3) #Option 2 Button
        cv2.putText(img,"-",(350,600),cv2.FONT_HERSHEY_SIMPLEX,4,(TextColour),2,cv2.LINE_AA) #Option 2 Text
        cv2.rectangle(img,(100,750),(700,950),(LineColour),3) #Option 3 Button
        cv2.putText(img,"-",(350,900),cv2.FONT_HERSHEY_SIMPLEX,4,(TextColour),2,cv2.LINE_AA) #Option 3 Text
        
        #Speech Output
        cv2.rectangle(img,(100,1000),(1200,1080),(LineColour),3) #Speech Outline
        cv2.putText(img,Output[0:36],(125,1050),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),2,cv2.LINE_AA) #Speech Text
        
        #Hand Detection
        if (ret):        
            greyScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            palms = hand.detectMultiScale(greyScale, 1.5, 5, minSize=(30,30))
            for (x,y,w,h) in palms:
                #Draws cursor square on hand
                img = cv2.rectangle(img,(x+(w//4),y+(h//4)),(x+((w//4)*3),y+((h//4)*3)),(TextColour),2)   
                frame = cv2.rectangle(frame,(x+(w//4),y+(h//4)),(x+((w//4)*3),y+((h//4)*3)),(TextColour),2) 
                #Stores cursor position
                cursorX = (x+(w//2))
                cursorY = (y+(h//2))  
        
        #Camera resize for image
        video = cv2.resize(frame, dsize=(480,270)) #Resize Camera for video Stream    
        img[760:1030, 1370:1850] = video #Place video stream on image  
        
        # help pop-up
        if needHelp == True:
            cv2.rectangle(img,(99,99),(1821,981),(LineColour),3)   # boarder
            cv2.rectangle(img,(100,100),(1820,980),(BackgroundColour),-1)  # background
            cv2.line(img,(115,180),(835,180),(LineColour),2) # boarder 2
                        # Help Text all on new lines
            cv2.putText(img,"Voice Commands Help",(120,165),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Help Text
            cv2.putText(img,"- Start: This will start the program from the menu screen",(120,220),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Options: This will allow the user to get to the options screen",(120,260),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Quit: This will exit the program",(120,300),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Back: This will take the user to the previous screen or menu option",(120,340),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Help: This will bring up the help screen",(120,380),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Close: This will close the help screen",(120,420),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Exit: This will exit from the current page to the previous page",(120,460),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Save: This will allow the user to save their progress in the tutorials",(120,500),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Reset: This will reset the progress of the tutorials",(120,540),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Run: This will run the user's code in the tutorials",(120,580),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Colour: This will change the theme colour when on the options screen",(120,620),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Select: This will select the button or object beneath the cursor",(120,660),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Drop: This will drop the selected item on the tutorial screen",(120,700),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
            cv2.putText(img,"- Input: This will allow the user to input variables.",(120,740),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA)
        
        cv2.imshow(windowName, img) #Show image        
        
        #Keyboard Control    
        if cv2.waitKey(1) == 27: #Wait for <ESC> Key 
            cv2.destroyAllWindows() #Close window
            break #Break while loop     

    WindowClose()   # runs the windowclose def
 
def WindowClose(): # will stop the program from running by setting running to false and releasing the camera 
    global camera
    global running 
    running = False
    camera.release()
    cv2.destroyAllWindows()
   
def FindClosestButton():  #returns button the user is hovering over
    global cursorX
    global cursorY
    
    button = "null"
    
    if cursorX in range(100,700) and cursorY in range (150,350):
        button = "colour"
        
    if cursorX in range(0,250) and cursorY in range (0,60):
        button = "exit"   
    
    return button

threadScreen = threading.Thread(target=Screen) #Declare screen thread #Threads to make the speech and screen run simultaneous
threadSpeech = threading.Thread(target=Speech) #Declare speech thread
threadScreen.start() #Run screen thread
threadSpeech.start() #Run speech thread



