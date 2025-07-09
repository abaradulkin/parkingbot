from selenium import webdriver
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import time, sleep

start = time()
driver = webdriver.Chrome('./chromedriver')
driver.get("https://1xbet.com/en/line/Football/")
close_btn = (By.ID, "help_popup")
#if driver.find_element(*close_btn):
#    print close_btn
wait = WebDriverWait(driver, 30)
wait.until(EC.visibility_of_element_located(close_btn))
action = action_chains.ActionChains(driver)
action.send_keys(keys.Keys.ESCAPE)
action.perform()
print "press escape"

driver and driver.quit()
print time() - start
#action = action_chains.ActionChains(driver)
#action.send_keys(keys.Keys.ESCAPE)
#action.perform()
