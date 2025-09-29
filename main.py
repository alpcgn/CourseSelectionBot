from asyncio import wait
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException , NoSuchElementException

courses = [ 
    ["ENG301", "05"], # PAY ATTENTION TO THE SYNTAX
    ["SE321", "02"],
    ["CMPE325", "01"],
    ]
username = "" 
password = ""
botisworking = False  # Global flag for bot status


def login(_username,_password):
    username = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[3]/div/div[1]/div[2]/div[1]/input')
    username.send_keys(_username)
    password = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/input')
    password.send_keys(_password)
    button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[3]/div/div[4]/div/span')
    button.click()
    try:
        error_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-toast-error')]//p[contains(text(),'Geçersiz Kullanıcı adı veya şifre')]"))
        )
        if error_element.is_displayed():
            print("Username or password is incorrect !")
            return False
    except TimeoutException:
            pass
    return True  

def inside(week="firstweek"):
    
    wait = WebDriverWait(driver, 9999)  # default long sec delay
    menu = wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Ders Kayıt ve Mezuniyet İşlemlerim')]"))
    )
    menu.click()
    time.sleep(1)

    if week == "adddrop": 
        menu_item = driver.find_element(By.XPATH, "//a[@href='DersKayitIslem/AddDropOgr']//label[contains(text(),'Ders Ekle/Bırak İşlemlerim')]")
        menu_item.click()    
    elif week == "firstweek":
        menu_item = driver.find_element(By.XPATH, "//a[@href='DersKayitIslem/FiltreOgr']//label[contains(text(),'Ders Kaydı İşlemlerim')]")
        menu_item.click()
    while True:
        try:
            element = driver.find_element(By.XPATH, "//button[normalize-space()='Tamam']")
            break
        except NoSuchElementException:                                                                 
            driver.refresh()
            time.sleep(10)   # waiting for page open time can be adjust 
    element.click()
    element = driver.find_element(By.XPATH, "/html/body/ul/li/div/button")
    element.click()

def courseSelection(courses):
    selectedlength = len(courses)

    while selectedlength > 0 and botisworking:
        for course_code, section in courses:
            full_code = courseCodeConvertor(course_code, section)
            try:
                label = driver.find_element(By.XPATH, f'//label[contains(text(),"{full_code}")]')
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
                driver.execute_script("arguments[0].click();", label)
            except Exception as e:
                print(f"{full_code} course couldn't find continue for other ones.. {e}")
                courses.remove([course_code, section])
                continue 
            try:
                time.sleep(0.2)                                                                                        #course adding 
                button = driver.find_element(By.XPATH, f'//button[contains(@onclick,"{course_code}")]')
                button.click()
                try:
                    error_box = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'message-error')]/div[@class='messenger-message-inner']"))
                    )
                    print(f"❌ {full_code} couldn't add, will try later..")
                    close_btn = driver.find_element(By.XPATH, "//div[contains(@class,'message-error')]//button[@class='messenger-close']")
                    close_btn.click()
                    continue                                                                            # skip to the next courses
                except TimeoutException:
                    print(f"✅ {course_code} SEC{section} added successfully.")
                    courses.remove([course_code, section])
            except Exception as e:
                continue

            if driver.find_elements(By.XPATH, "/html/body/ul/li[1]/div/button"):                        #success popup closing 
                element = driver.find_element(By.XPATH, "/html/body/ul/li[1]/div/button")
                element.click()
            print(f"{course_code} SEC{section} added to basket.")
            selectedlength -= 1

def courseCodeConvertor(course, section):
    return f"{course} ({course}-SEC-{section})"

def run_interface(username, password, week):
    global driver, botisworking
    botisworking = True  # Set bot as working
    driver = webdriver.Chrome() #driver type, check this site for other drivers https://pypi.org/project/selenium/              
    driver.get('https://atacs.atilim.edu.tr/')  
    driver.maximize_window()
    time.sleep(2)
    
    if not botisworking:  # Check if stopped before login
        driver.quit()
        return None
        
    if login(username, password) == True:
        if not botisworking:  # Check if stopped after login
            driver.quit()
            return None
            
        inside(week)
        time.sleep(2)
        
        if not botisworking:  # Check if stopped before course selection
            driver.quit()
            return None
            
        courseSelection(courses)
        return driver
    else:
        driver.quit()
        return False

def stop_bot():
    global botisworking
    botisworking = False
   

