# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 13:38:39 2021

@author: Kieran and Jacob
"""
import numpy as np #Import NumPy module
import cv2 #Import OpenCV module
import threading #Import Threading module
import speech_recognition as sr #Import Speech Recognition Module

running = True #Sets running true
Output = ""

def Speech():
    #Refer to globally referenced variable
    global running
    global Output
    global menuStage
    global camera
    global cursorSelection
    global taskStep
    global inputtingText
    global input1Value
    global input2Value
    global variableInput
    global needHelp
    
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
            print("Could not understand audio 1") 
            #Output = "Could not understand audio"
            continue
        except sr.RequestError as e: #If audio not recognised continue
            print("Could not request results; {0}".format(e))
            #Output = "Could not understand audio"
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
                
            #Checks if keywords are present in MicInput
            
            if Start in MicInput and KeywordCount == 1:
                print(BadCommand)
                
            if Options in MicInput and KeywordCount == 1:
                print(BadCommand)    
                
            if Quit in MicInput and KeywordCount == 1:  
                WindowClose() #Window Close Routine
                break  
                
            if Back in MicInput and KeywordCount == 1:
                if menuStage != "main":
                    menuStage = "main" 
                
            if Help in MicInput and KeywordCount == 1:
                if needHelp == False:
                    needHelp = True
                else:
                    print(BadCommand)
                
            if Close in MicInput and KeywordCount == 1:
                if needHelp == True:
                    needHelp = False
                else:
                    print(BadCommand)
                
            if Exit in MicInput and KeywordCount == 1:
                WindowClose()
                exec(open("TaskScreen.py").read()) #Open Task Screen     
                break    
                
            if Save in MicInput and KeywordCount == 1:
                # save the taskStep and other variables
                    with open("Tutorial1.txt", "w") as file:  # open the file 
                        file.write(str(taskStep) + "\n") # save the task step on line 1
                        file.write(input1Value + "\n") # save the input value on line 2
                        file.write(input2Value + "\n") # save on line 3
                        file.write(variableInput + "\n") # save on line 4
                        file.close() # close the file
# will reset the task to the beginning
            if Reset in MicInput and KeywordCount == 1:
                taskStep = 0
                input1Value = ""
                input2Value = ""
                variableInput = ""
                # will run the task 
            if Run in MicInput and KeywordCount == 1:
                if taskStep == 4:
                    taskStep = 5
                    # will print bad command
                else:
                    print(BadCommand)
                
            if Colour in MicInput and KeywordCount == 1:
                print(BadCommand)    
                # will select the button that the user is hovering over
            if Select in MicInput and KeywordCount == 1:
                closestButton = FindClosestButton()
                if closestButton == "exit":
                    WindowClose()
                    exec(open("TaskScreen.py").read()) #Open Task Screen       
                    break
                elif closestButton == "save":
                    with open("Tutorial1.txt", "w") as file:  # open the file 
                        file.write(str(taskStep) + "\n") # save the task step on line 1
                        file.write(input1Value + "\n") # save the input value on line 2
                        file.write(input2Value + "\n") # save on line 3
                        file.write(variableInput + "\n") # save on line 4
                        file.close() # close the file
                elif closestButton == "reset":
                    taskStep = 0
                    input1Value = ""
                    input2Value = ""
                    variableInput = ""
                elif closestButton == "run":
                    if taskStep == 4:
                        taskStep = 5
                    else:
                        print(BadCommand)
                elif closestButton == "help":
                    if needHelp == False:
                        needHelp = True
                    else:
                        print(BadCommand)
                elif closestButton == "menuChange":
                    print("menu change handled")
                    continue
                elif closestButton == "null":
                    print("no button selected")
                closestButton == "null"
                # will drop the current selection 
            if Drop in MicInput and KeywordCount == 1:
                if cursorSelection != "null":
                    FindTaskBox()
                cursorSelection = "null"
                # used to input text into the code 
            if Input in MicInput and KeywordCount == 1:
                inputtingText = True  
               # if to many keywords are said by user
            if KeywordCount > 1:
                print("Too many commands heard, please try again") 
            
def Screen():
    global camera #Refer to global running variable
    global running 
    global cursorX
    global cursorY
    global Output
    global needHelp
    global menuStage
    global cursorSelection
    global taskStep
    global input1Value
    global input2Value
    global variableInput
    global inputtingText
            
    try:
        with open("Colour.txt", "r") as file:
           ColourMode =  (int(open("Colour.txt","r").read()))
           file.close()  
    except:
        with open("Colour.txt", "w") as file:
            file.write("1")
            ColourMode =  (int(open("Colour.txt","r").read()))
            print("error has been resolved please run program again")
            file.close()
            
    try: # try and open file and view line by line 
        with open("Tutorial1.txt", "r") as file:
            for i, line in enumerate(file):
                if i == 0:
                    taskStep = int(line)
                if i == 1:
                    input1Value = line
                if i == 2:
                    input2Value = line
                if i == 3:
                    variableInput = line
        file.close()        
    except:    # if the file does not exsist then use default values  
        taskStep = 0
        input1Value = ""
        input2Value= ""
        variableInput= ""            
  
    if ColourMode == 1:
        LineColour = 0,255,0
        TextColour = 255,255,255
        BackgroundColour = 0,0,0
        
    if ColourMode == 2:
        LineColour = 255,0,0
        TextColour = 0,0,0
        BackgroundColour = 255,255,255    
    img = np.zeros((1080,1920,3), np.uint8) #Create black image
    
    windowName = "Tutorial1" #Set window name
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN) #Creates window
    cv2.moveWindow(windowName, 0,0) #Move window to origin
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) #Set window to fullscreen
    
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) #Capture camera
    camera.set(3,1920) #Set camera width
    camera.set(4,1080) #Set camera height
    
    hand = cv2.CascadeClassifier("haarcascades/Hand.Cascade.1.xml")  #Stores hand cascase file
      
    cursorX = 0 #Sets initial cursor position values
    cursorY = 0
    
    menuStage = "main"
    cursorSelection = "null"
    
    inputtingText = False
    
    needHelp = False
    
    while running == True: #While speech recognition and camera are running
        
        ret, frame = camera.read() #Main Camera Read
        
        cv2.rectangle(img,(0,0),(1920,1080),(BackgroundColour), cv2.FILLED) #Reset image background
   
        #Taskbar
        cv2.rectangle(img,(0,0),(1920,75),(LineColour),3) #Taskbar Border
        cv2.rectangle(img,(0,0),(250,75),(LineColour),3) #Exit Button
        cv2.putText(img,"Exit",(60,60),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Exit Text
        cv2.rectangle(img,(250,0),(500,75),(LineColour),3) #Save Button
        cv2.putText(img,"Save",(305,60),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Save Text
        cv2.rectangle(img,(500,0),(750,75),(LineColour),3) #Reset Button
        cv2.putText(img,"Reset",(530,60),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Reset Text
        cv2.rectangle(img,(750,0),(1000,75),(LineColour),3) #Run Button
        cv2.putText(img,"Run",(810,60),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Run Text
        cv2.rectangle(img,(1670,0),(1920,75),(LineColour),3) #Help Button
        cv2.putText(img,"Help",(1720,60),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Help Text 
        
        #ScreenLayout
        cv2.rectangle(img,(0,75),(500,1080),(LineColour),3) #Programming Menu
        cv2.rectangle(img,(0,810),(500,1080),(LineColour),3) #Microphone Input
        cv2.rectangle(img,(500,75),(1300,1080),(LineColour),3) #Program
        cv2.rectangle(img,(1300,75),(1920,720),(LineColour),3) #Output
        cv2.rectangle(img,(1300,720),(1920,1080),(LineColour),3) #Camera
        
        #Speech Output
        outputList = Output.split(" ")
        lineLevel = 850
        lineCharacterTotal = 0
        line = ""
        for x in outputList:
            lineCharacterTotal = lineCharacterTotal + len(x)
            line = line + x + " "
            if lineCharacterTotal > 15:
                cv2.putText(img,line,(20,lineLevel),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),2,cv2.LINE_AA) #Speech Text
                lineCharacterTotal = 0
                line = ""
                lineLevel = lineLevel + 50
        else:
            cv2.putText(img,line,(20,lineLevel),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),2,cv2.LINE_AA) #Speech Text
            lineCharacterTotal = 0
            line = ""
            lineLevel = lineLevel + 50
        
        #Hand Detection
        if (ret):        
            greyScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            palms = hand.detectMultiScale(greyScale, 1.5, 5, minSize=(30,30))
            for (x,y,w,h) in palms:
                #Draws cursor square on hand
                if cursorSelection != "null":
                    selectX = x + (w//2)
                    selectY = y + (h//2)
                    textSpace = len(cursorSelection) * 25
                    img = cv2.rectangle(img,(selectX-100,selectY-50),(selectX+textSpace-20,selectY+50),(LineColour),2)
                    cv2.putText(img,cursorSelection,(selectX-80,selectY+20),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Help Text
                else:
                    img = cv2.rectangle(img,(x+(w//4),y+(h//4)),(x+((w//4)*3),y+((h//4)*3)),(TextColour),2)   
                frame = cv2.rectangle(frame,(x+(w//4),y+(h//4)),(x+((w//4)*3),y+((h//4)*3)),(TextColour),2) 
                #Stores cursor position
                cursorX = (x+(w//2))
                cursorY = (y+(h//2))                                      
                    
        
        #Camera resize for image
        video = cv2.resize(frame, dsize=(480,270)) #Resize Camera for video Stream    
        img[760:1030, 1370:1850] = video #Place video stream on image
        
        #Programming Menu
        if menuStage == "main":
            cv2.rectangle(img,(10,85),(490,220),(LineColour),3) #Basic Button        
            cv2.putText(img,"Basic",(170,175),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Basic Text                       
            cv2.rectangle(img,(10,230),(490,365),(LineColour),3) #Selection Button
            cv2.putText(img,"Selection",(120,320),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Selection Text
            cv2.rectangle(img,(10,375),(490,510),(LineColour),3) #Iterative Button
            cv2.putText(img,"Iterative",(130,465),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Iterative Text  
            cv2.rectangle(img,(10,520),(490,655),(LineColour),3) #Arithmetic Button
            cv2.putText(img,"Arithmetic",(100,610),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Arithmetic Text  
            cv2.rectangle(img,(10,665),(490,800),(LineColour),3) #Functions Button
            cv2.putText(img,"Functions",(105,755),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Functions Text            
        elif menuStage == "basic":
            cv2.rectangle(img,(10,85),(210,170),(LineColour),3) #Back Button
            cv2.putText(img,"Back",(30,150),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Back Text 
            cv2.rectangle(img,(10,180),(490,315),(LineColour),3) #Print Button
            cv2.putText(img,"Print",(170,270),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Print Text
            cv2.rectangle(img,(10,325),(490,460),(LineColour),3) #Variable Button
            cv2.putText(img,"Variable",(130,415),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Variable Text      
        elif menuStage == "selection":
            cv2.rectangle(img,(10,85),(210,170),(LineColour),3) #Back Button
            cv2.putText(img,"Back",(30,150),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Back Text  
            cv2.rectangle(img,(10,180),(490,315),(LineColour),3) #IF Button
            cv2.putText(img,"IF",(230,270),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #IF Text  
            cv2.rectangle(img,(10,325),(490,460),(LineColour),3) #Else Button
            cv2.putText(img,"Else",(185,415),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Else Text       
        elif menuStage == "iterative":
            cv2.rectangle(img,(10,85),(210,170),(LineColour),3) #Back Button
            cv2.putText(img,"Back",(30,150),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Back Text   
            cv2.rectangle(img,(10,180),(490,315),(LineColour),3) #While Button
            cv2.putText(img,"While",(170,270),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #While Text   
            cv2.rectangle(img,(10,325),(490,460),(LineColour),3) #For Button
            cv2.putText(img,"For",(200,415),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #For Text     
        elif menuStage == "arithmetic":
            cv2.rectangle(img,(10,85),(210,170),(LineColour),3) #Back Button
            cv2.putText(img,"Back",(30,150),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Back Text
            cv2.rectangle(img,(10,180),(490,275),(LineColour),3) #Plus Button
            cv2.putText(img,"Plus",(170,250),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Plus Text
            cv2.rectangle(img,(10,285),(490,380),(LineColour),3) #Minus Button
            cv2.putText(img,"Minus",(150,355),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Minus Text  
            cv2.rectangle(img,(10,390),(490,485),(LineColour),3) #Greater Than Button
            cv2.putText(img,"Greater Than",(40,460),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Greater Than Text  
            cv2.rectangle(img,(10,495),(490,590),(LineColour),3) #Less Than Button
            cv2.putText(img,"Less Than",(80,565),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Less Than Text 
            cv2.rectangle(img,(10,600),(490,695),(LineColour),3) #Equal To Button
            cv2.putText(img,"Equal To",(90,670),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Equal To Text
            cv2.rectangle(img,(10,705),(490,800),(LineColour),3) #Not Equal To Button
            cv2.putText(img,"Not Equal To",(40,775),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Not Equal To Text            
        elif menuStage == "functions":
            cv2.rectangle(img,(10,85),(210,170),(LineColour),3) #Back Button
            cv2.putText(img,"Back",(30,150),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Back Text           
            cv2.rectangle(img,(10,180),(490,315),(LineColour),3) #.length Button
            cv2.putText(img,".length",(140,270),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #.length Text            
            cv2.rectangle(img,(10,325),(490,460),(LineColour),3) #.lower Button
            cv2.putText(img,".lower",(160,415),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #.lower Text            
            cv2.rectangle(img,(10,470),(490,605),(LineColour),3) #Variable Button
            cv2.putText(img,".upper",(140,560),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #.upper Text
        
        #Task Area
        if taskStep == 0:
            cv2.putText(img,"Insert VAR below here",(520,150),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),1,cv2.LINE_AA) #Help Text
            cv2.rectangle(img,(520,180),(1280,315),(LineColour),3) #Input Area 1
            cv2.putText(img,input1Value,(550,270),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Input Area 1 Text      
        elif taskStep == 1:
            input1Value = "VAR1 = "
            cv2.putText(img,"Use INPUT to enter value",(520,150),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),1,cv2.LINE_AA) #Help Text
            cv2.rectangle(img,(520,180),(1280,315),(LineColour),3) #Input Area 1
            cv2.putText(img,input1Value,(550,270),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Input Area 1 Text
            if inputtingText == True:
                    FindTaskBox()
        elif taskStep == 2:
            input1Value = "VAR1 = " + "'" + variableInput + "'"
            cv2.rectangle(img,(520,120),(1280,265),(LineColour),3) #Input Area 1
            cv2.putText(img,input1Value,(550,220),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Input Area 1 Text
            cv2.putText(img,"Insert PRINT below here",(520,335),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),1,cv2.LINE_AA) #Help Text
            cv2.rectangle(img,(520,365),(1280,510),(LineColour),3) #Input Area 2
            cv2.putText(img,input2Value,(550,465),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Input Area 2 Text 
        elif taskStep == 3:
            input1Value = "VAR1 = " + "'" + variableInput + "'"
            input2Value = "PRINT(    )"
            cv2.rectangle(img,(520,120),(1280,265),(LineColour),3) #Input Area 1
            cv2.putText(img,input1Value,(550,220),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Input Area 1 Text
            cv2.putText(img,"Insert VAR into PRINT",(520,335),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),1,cv2.LINE_AA) #Help Text
            cv2.rectangle(img,(520,365),(1280,510),(LineColour),3) #Input Area 2
            cv2.putText(img,input2Value,(550,465),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Input Area 2 Text   
        elif taskStep == 4:
            input1Value = "VAR1 = " + "'" + variableInput + "'"
            input2Value = "PRINT(VAR1)"
            cv2.rectangle(img,(520,120),(1280,265),(LineColour),3) #Input Area 1
            cv2.putText(img,input1Value,(550,220),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Input Area 1 Text
            cv2.rectangle(img,(520,300),(1280,445),(LineColour),3) #Input Area 2
            cv2.putText(img,input2Value,(550,400),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Input Area 2 Text
            cv2.putText(img,"Now RUN the program",(520,525),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),1,cv2.LINE_AA) #Help Text  
        elif taskStep == 5:
            input1Value = "VAR1 = " + "'" + variableInput + "'"
            input2Value = "PRINT(VAR1)"
            programOutput = input1Value[8:-1]
            cv2.rectangle(img,(520,120),(1280,265),(LineColour),3) #Input Area 1
            cv2.putText(img,input1Value,(550,220),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Input Area 1 Text
            cv2.rectangle(img,(520,300),(1280,445),(LineColour),3) #Input Area 2
            cv2.putText(img,input2Value,(550,400),cv2.FONT_HERSHEY_SIMPLEX,2,(TextColour),2,cv2.LINE_AA) #Input Area 2 Text
            cv2.putText(img,"> " + programOutput,(1320,130),cv2.FONT_HERSHEY_SIMPLEX,1,(TextColour),1,cv2.LINE_AA) #Output Text
        # help pop-up
        if needHelp == True:
            cv2.rectangle(img,(99,99),(1821,981),(LineColour),3)   #boarder
            cv2.rectangle(img,(100,100),(1820,980),(BackgroundColour),-1) #background
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
        
        if cv2.waitKey(1) == 27: #Wait for <ESC> key
            cv2.destroyAllWindows() #Close window
            break #Break while loop

    WindowClose() #Window Close Routine
    
def WindowClose(): # will stop the program from running by setting running to false and releasing the camera 
    global camera
    global running 
    running = False
    camera.release()
    cv2.destroyAllWindows()
    
#returns button the user is hovering over
def FindClosestButton():
    global cursorX
    global cursorY
    global menuStage
    global cursorSelection
    
    closestButton = "null"
    menuChangeMade = False
    # all buttons and their positions
    if menuStage == "main":     
        if cursorX in range(10,490) and cursorY in range (85,220) and menuChangeMade == False: #Basic
            menuStage = "basic"
            menuChangeMade = True

        if cursorX in range(10,490) and cursorY in range (230,365) and menuChangeMade == False: #Selection
            menuStage = "selection"
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (375,510) and menuChangeMade == False: #Iterative
            menuStage = "iterative"  
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (520,655) and menuChangeMade == False: #Arithmetic
            menuStage = "arithmetic"   
            menuChangeMade = True
    
        if cursorX in range(10,490) and cursorY in range (665,800) and menuChangeMade == False: #Functions
            menuStage = "functions"  
            menuChangeMade = True
            
    if menuStage == "basic":
        if cursorX in range(10,210) and cursorY in range (85,170) and menuChangeMade == False: #Back
            menuStage = "main"
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (180,315) and menuChangeMade == False: #Print
            cursorSelection = "print"
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (325,460) and menuChangeMade == False: #Variable
            cursorSelection = "var"  
            menuChangeMade = True

    if menuStage == "selection":
        if cursorX in range(10,210) and cursorY in range (85,170) and menuChangeMade == False: #Back
            menuStage = "main" 
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (180,315) and menuChangeMade == False: #IF
            cursorSelection = "if"
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (325,460) and menuChangeMade == False: #Else 
            cursorSelection = "else"  
            menuChangeMade = True
            
    if menuStage == "iterative":
        if cursorX in range(10,210) and cursorY in range (85,170) and menuChangeMade == False: #Back
            menuStage = "main"    
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (180,315) and menuChangeMade == False: #While
            cursorSelection = "while"
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (325,460) and menuChangeMade == False: #For 
            cursorSelection = "for"  
            menuChangeMade = True
            
    if menuStage == "arithmetic":
        if cursorX in range(10,210) and cursorY in range (85,170) and menuChangeMade == False: #Back
            menuStage = "main"    
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (180,275) and menuChangeMade == False: #Plus
            cursorSelection = "+"
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (285,380) and menuChangeMade == False: #Minus
            cursorSelection = "-"   
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (390,485) and menuChangeMade == False: #Greater than
            cursorSelection = ">"  
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (495,590) and menuChangeMade == False: #Less than
            cursorSelection = "<"   
            menuChangeMade = True
    
        if cursorX in range(10,490) and cursorY in range (600,695) and menuChangeMade == False: #Equal to
            cursorSelection = "="     
            menuChangeMade = True
    
        if cursorX in range(10,490) and cursorY in range (705,800) and menuChangeMade == False: #Not equal to 
            cursorSelection = "!=" 
            menuChangeMade = True

    if menuStage == "functions":
        if cursorX in range(10,210) and cursorY in range (85,170) and menuChangeMade == False: #Back
            menuStage = "main"     
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (180,315) and menuChangeMade == False: #.length 
            cursorSelection = ".length"
            menuChangeMade = True
            
        if cursorX in range(10,490) and cursorY in range (325,460) and menuChangeMade == False: #.lower 
            cursorSelection = ".lower"  
            menuChangeMade = True

        if cursorX in range(10,490) and cursorY in range (470,605) and menuChangeMade == False: #.upper             
            cursorSelection = ".upper"
            menuChangeMade = True
    
    if menuChangeMade == True:
        closestButton = "menuChange"
        
    if cursorX in range(0,250) and cursorY in range (0,75):
        closestButton = "exit"
        
    if cursorX in range(250,500) and cursorY in range (0,75):
        closestButton = "save"   
        
    if cursorX in range(500,750) and cursorY in range (0,75):
        closestButton = "reset"   
    
    if cursorX in range(750,1000) and cursorY in range (0,75):
        closestButton = "run"   
        
    if cursorX in range(1670,1920) and cursorY in range (0,75):
        closestButton = "help"  
    
    return closestButton

# will check the taskStep
def FindTaskBox():
    global cursorX
    global cursorY
    global menuStage
    global cursorSelection
    global taskStep
    global Output
    global variableInput
    global inputtingText
    
    if taskStep == 0:
        if cursorX in range(520,1280) and cursorY in range (180,315) and cursorSelection == "var": #Input Area 1
            taskStep = 1
    elif taskStep == 1:
        if cursorX in range(520,1280) and cursorY in range (180,315) and inputtingText == True: #Input Area 1
            if Output != "ok program input" and Output != "ok program inputs":
                variableInput = Output
                inputtingText = False
                taskStep = 2
    elif taskStep == 2:
        if cursorX in range(520,1280) and cursorY in range (365,510) and cursorSelection == "print": #Input Area 2
            taskStep = 3
    elif taskStep == 3:
        if cursorX in range(520,1280) and cursorY in range (365,510) and cursorSelection == "var": #Input Area 2
            taskStep = 4
    elif taskStep == 4:
        pass
    elif taskStep == 5:
        pass
         
#Threads
threadScreen = threading.Thread(target=Screen) #Declare screen thread
threadSpeech = threading.Thread(target=Speech) #Declare speech thread
threadScreen.start() #Run screen thread
threadSpeech.start() #Run speech thread