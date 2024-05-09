from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time, random
import speech_recognition as sr
import pydub



def speech_to_text():
    
    # Convert MP3 to WAV (using pydub)
    sound = pydub.AudioSegment.from_mp3("byp.mp3")
    sound.export("converted.wav", format="wav")

    text = ''
    # Use SpeechRecognition for text conversion
    with sr.AudioFile('converted.wav') as source:
        r = sr.Recognizer()
        audio = r.record(source)

        text = r.recognize_google(audio)
    return text


# takes selenium driver
def solveRe(driver):
    #define max waiting time for selenium wait
    wait = WebDriverWait(driver, 10) 
    
    # locate recaptcha iframe and click on it
    iframe1 = driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
    iframe1.click()      
    
    try:
        time.sleep(1)
        iframe1.find_element(By.CLASS_NAME, 'recaptcha-checkbox-checkmark')
        print('oui')
        return 
    except:
        pass
    # locate recaptcha challenge iframe and pause for a random # of seconds
    iframe2 = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']")))
    time.sleep(random.randrange(1, 4))           
    
    # switch to the challenge iframe
    driver.switch_to.frame(iframe2)   
    
    # get the audio challenge
    driver.find_element(By.ID, 'recaptcha-audio-button').click()  
    
    time.sleep(random.randrange(1, 4))
    
    # get audio link and save it to byp.mp3 file
    audio_link = driver.find_element(By.CSS_SELECTOR, '#rc-audio > div.rc-audiochallenge-tdownload > a').get_attribute('href')
    audio_link = requests.get(audio_link, allow_redirects=True)
    open('byp.mp3', 'wb').write(audio_link.content)
    
    # transcribe audio
    response = speech_to_text()
    
    # submit response and press enter
    driver.find_element(By.ID, 'audio-response').send_keys(response + Keys.RETURN)
    
    # swtich back to the default page (out of the iframe)
    driver.switch_to.default_content()
    
