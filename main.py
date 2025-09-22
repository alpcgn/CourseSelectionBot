from asyncio import wait
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

courses = [
    ["CMPE323", "SEC-01"], # PAY ATTENTION TO THE SYNTAX DON'T WRITE WITHOUT WITH , 
    ["MATH276", "SEC-02"]
    ]
username = "" #etc:  "your atacs username"
password = ""
driver = webdriver.Chrome() #driver type, check this site for other drivers https://pypi.org/project/selenium/

def login(_username,_password):
    username = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[3]/div/div[1]/div[2]/div[1]/input')
    username.send_keys(_username)
    password = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/input')
    password.send_keys(_password)
    button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[3]/div/div[4]/div/span')
    button.click()
    try:
            error_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-toast-error')]//p[contains(text(),'Geçersiz Kullanıcı adı veya şifre')]"))
            )
            if error_element.is_displayed():
                print("Username or password is incorrect !")
                return False
    except TimeoutException:
            pass
    return True  

def inside():
    
    wait = WebDriverWait(driver, 9999)  # default infininite sec delay, idk which one for long time waiting would be better i choose to wait until page is open.

    menu = wait.until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Ders Kayıt ve Mezuniyet İşlemlerim')]"))
    )
    menu.click()
    time.sleep(1)
    menu_item = driver.find_element(By.XPATH, "//a[@href='DersKayitIslem/FiltreOgr']//label[contains(text(),'Ders Kaydı İşlemlerim')]")
    menu_item.click()
    element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Tamam']"))
    )
    element.click()
    element = driver.find_element(By.XPATH, "/html/body/ul/li/div/button")
    element.click()

def courseSelection(courses):
    for course_code, section in courses:
        full_code = courseCodeConvertor(course_code, section)

        try:
            label = driver.find_element(By.XPATH, f'//label[contains(text(),"{full_code}")]')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
            driver.execute_script("arguments[0].click();", label)
        except Exception as e:
            print(f"{full_code} course couldn't find continue for other ones.. {e}")
            continue 
        try:
            button = driver.find_element(By.XPATH, f'//button[contains(@onclick,"{course_code}")]')
            button.click()
        except Exception as e:
            print(f" {full_code} button couldn't find or clicked contine for other ones.. {e}")

        print(f"{course_code} {section} added to basket.")
        time.sleep(1)


def courseCodeConvertor(course, section):
    return f"{course} ({course}-{section})"


def run_bot(username, password):
                    

    driver.get('https://atacs.atilim.edu.tr/')  
    driver.maximize_window()

    time.sleep(2)
    if username == "" or password == "":
        print("ENTER USERNAME AND PASSWORD FROM LINE 13")
    else:
        if login(username,password) == True:
            inside()
            time.sleep(2)
            courseSelection(courses)
            return driver
        else:
            quit
   

