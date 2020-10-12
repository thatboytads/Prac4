# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import time

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
guessnum=0 # guessed number
scoreArray=[]
scorecount=0 #number of guesses
value = 0 #Randomly generated number
# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()
cnt=0


# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        while not end_of_game:
             if GPIO.input(btn_increase) == 1:
                btn_increase_pressed(btn_increase)
             elif GPIO.input(btn_submit) == 1:
                btn_guess_pressed(btn_submit)
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    pass


# Setup Pins
def setup():
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)
    # Setup regular GPIO
    GPIO.setup(LED_value[0], GPIO.OUT)
    GPIO.setup(LED_value[1], GPIO.OUT)
    GPIO.setup(LED_value[2], GPIO.OUT)
    GPIO.setup(LED_accuracy, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(btn_increase, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(btn_submit, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
    # Setup PWM channels
    pwm1 = GPIO.PWM(LED_accuracy, 100)  
    pwm2 = GPIO.PWM(buzzer, 100)
    # Setup debouncing and callbacks
   
    GPIO.add_event_detect(10,GPIO.FALLING, callback=btn_increase, bouncetime=200)
    GPIO.add_event_detect(10,GPIO.FALLING, callback=btn_submit, bouncetime=200)
    
    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = eeprom.read_byte(self, 0)
    # Get the scores
    # convert the codes back to ascii
    scores = []
    for i in range(1, score_count+1):
        score = eeprom.read_block(self, i, 4)
        for letter in score[0]:
                scores.append(chr(letter))
        scores.append(score[1])
        #score1= score[0]
        #score2= score[1]
        #score3= score[2]
        #score4= score[3]
        #outputScore= chr(score1)+ chr(score2)+ chr(score3)+ chr(score4)
        #scores.append(outputScore)
    # return back the results
    return score_count, scores


# Save high scores
def save_scores():
    # fetch scores
    scorecount,scoreArray =fetch_scores()
    # include new score
    eeprom.write_block(0, [scoreCount+1])
     Name= input("Enter name with 3 bits or less")
     inputScore = [[Name, scoreCount]]
    scoreArray.append(inputScore)
    scoreArray.sort(key=lambda x: x[1])
    data_to_write = []
    for Writescore in scoreArray:
        # get the string
        for letter in Writescore[0]:
            data_to_write.append(ord(letter))
        data_to_write.append(Writescore[1])
        eeprom.write_block(1, data_to_write)
    # sort
    # update total amount of scores
    # write new scores
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    # Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess
    
   
            cnt += 1 
            GPIO.output(LED_value[0], cnt & 0x01) #set bit 0
            GPIO.output(LED_value[1], cnt & 0x02)
            GPIO.output(LED_value[2], cnt & 0x04)
            
            
                
    pass


# Guess button
def btn_guess_pressed(channel):
   
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs

        if (guessnum!= value):
            
                    scoreCount+=1
                
                    
                    accuracy_leds() # Change the PWM LED
                    if (abs(value)-abs(guessnum)<=3):
                        trigger_buzzer()
        else:
             GPIO.output(LED_value, GPIO.low)
             GPIO.output(Buzzer, GPIO.low)
             
             
             save_scores()
             
        
               
        
            
    # if it's close enough, adjust the buzzer
       
        
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    pass


# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    if (guessnum< value):
        dc= guessnum/value *100
        pwm1.ChangeDutyCycle(dc);
       
    else:
        dc= ((8-guess)/(8-value))*100
        pwm1.ChangeDutyCycle(dc);
    
    pass

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    pwm2.start(50)
    if abs(guessnum-value)== 1:
        pwd2.ChangeFrequency(4)
    if abs(guessnum-value)== 2:
        pwd2.ChangeFrequency(2)
    if abs(guessnum-value)== 3:
        pwd2.ChangeFrequency(1)
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
