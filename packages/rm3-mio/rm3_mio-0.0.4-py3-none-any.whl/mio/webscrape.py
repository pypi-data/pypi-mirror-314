from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

# SELENIUM DOCS
# https://www.selenium.dev/documentation/webdriver/

# create selenium web driver
def makeDriver(headless=True):
    options = Options()
    if headless: options.add_argument("--headless")
    driver = Firefox(options=options)
    return driver

# check if HTML element exists
def elementExist(driver,by,value):
    return (len(driver.find_elements(by, value)) > 0)

# check if HTML element has a certain attribute
def elementHas(element, attribute, name):
    attrs = element.get_attribute(attribute)
    if attrs == None:
        return False
    else:
        return name in attrs.split()

# wait for DOM to fully load/update
def waitForDOM(driver, timeout=5):
    driver.implicitly_wait(timeout) 

# wait for element with specific class to appear (blocking function)
def waitForLoad(driver, className):
    sleep(0.2)
    loadMasks = driver.find_elements(By.CLASS_NAME, className)
    while len(loadMasks)!=0:
        sleep(0.05)
        loadMasks = driver.find_elements(By.CLASS_NAME, className)
    return

# scroll to HTML element
def scrollToElement(driver, element):
        x = element.location['x']
        y = element.location['y']
        scroll_by_coord = f'window.scrollTo({x},{y});'
        scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
        driver.execute_script(scroll_by_coord)
        driver.execute_script(scroll_nav_out_of_way)


# scroll to specific text on page
def scrollToText(driver, text):
    element = driver.find_element("xpath", f"//*[text()[contains(., '{text}')]]")
    scrollToElement(driver, element)

# get preceeding element in HTML tree
def next(element):
    return element.find_element(By.XPATH, "./following-sibling::*")

# example Selenium usage
if __name__=="__main__":
    driver = makeDriver(headless=False)
    driver.get("https://google.com")

    e = driver.find_element(By.CLASS_NAME, "class_name") # class="class_name"
    e = driver.find_element(By.ID_NAME, "id_name") # id="id_name"
    eText = elem.text
    e.click()
    rows = e.find_elements(By.TAG_NAME, "tr")

    input()
    driver.quit()

