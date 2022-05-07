from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import argparse
import pickle

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument("disable-gpu")
global driver
driver = webdriver.Chrome('chromedriver', options=chrome_options)

def login_page(url,email,password):
    try:
        driver.get(url)
        # get_login_email = driver.find_element_by_xpath("//input[@name='email']")
        get_login_email = driver.find_element(by=By.XPATH, value="//input[@name='email']")
        get_login_email.send_keys(email)
        time.sleep(2)
        # get_login_pass = driver.find_element_by_xpath("//input[@name='pass']")
        get_login_pass = driver.find_element(by=By.XPATH, value="//input[@name='pass']")
        get_login_pass.send_keys(password)
        time.sleep(2)
        # get_login_btn = driver.find_element_by_xpath("//input[@name='input']")
        get_login_btn = driver.find_element(by=By.XPATH, value="//input[@value='Log In']")
        get_login_btn.click()

        get_cookies = driver.get_cookies() 
        pickle.dump( get_cookies , open("cookiesFB.pkl","wb"))

        return get_cookies
    except Exception as e:
        print(e)
        return False

def get_message_link(url,cookies):
    driver.get(url)

    for cookie in cookies:
        driver.add_cookie(cookie)

    time.sleep(10)
    driver.get(url + "/messages")

    store_link = []
    try:
        list_table_messages = driver.find_elements(by=By.XPATH, value="//section[1]/div[1]/table") # /tbody/tr/td/header/h3[1]/a
        for llink in range(len(list_table_messages)):
            message_link = driver.find_element(by=By.XPATH, value=f"//section[1]/div[1]/table[{llink+1}]//header/h3[1]/a").get_attribute('href')
            store_link.append(message_link)
    except:
        store_link = 0
    return store_link

def check_more_messages():
    pass

def do_delete_message(link):
    driver.get(link)

    try:
        get_msg_username = driver.find_element(By.XPATH, value="//div[@id='objects_container']//div/span").text
        driver.find_element(By.XPATH, value="//form/div/input[@value='Delete']").click()
        time.sleep(3)
        driver.find_element(By.XPATH, value="//div[@id='objects_container']//div[2]/a[text()='Delete']").click()

        return get_msg_username
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":

    main_url = "https://mbasic.facebook.com"

    parser = argparse.ArgumentParser(description="Facebook Message Delete (for lazy person)")
    parser.add_argument('--email', dest='email', type=str, required=True)
    parser.add_argument('--pwd', dest='pwd', type=str, required=True)

    args = parser.parse_args()

    email = args.email
    password = args.pwd

    try:
        login = pickle.load(open("cookiesFB.pkl", "rb"))
        print("Using Cookies", login)
    except:
        print("login session started")
        login = login_page(main_url,email,password)        
    
    if len(login) > 0:
        print("now getting message url")
        msglink = get_message_link(main_url, login)
        print(msglink)

        if len(msglink) > 0:
            print("\n")
            print("deleting message")
            for delmsg in msglink:
                do_delete = do_delete_message(delmsg)
                if do_delete:
                    print(f"Message from {do_delete} deleted successfully")
        else:
            print("there is no messages left")

    driver.close()