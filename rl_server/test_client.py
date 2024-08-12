from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import requests
from time import sleep

import os

# NOTE: make sure to update sever url (localhost -> 100.64.0.1) in cached client (located in www/var/html) before running in mahimahi.
# curl -v -X POST http://100.64.0.1:8333 -H "Content-Type: application/json" -d '{"nextChunkSize":1,"Type":"BB","lastquality":1,"buffer":1,"bufferAdjusted":1,"bandwidthEst":1,"lastRequest":1,"RebufferTime":1,"lastChunkFinishTime":1628077200000,"lastChunkStartTime":1628077100000,"lastChunkSize":1}'

url = f"http://100.64.0.1/myindex_robustMPC.html"

display = Display(visible=1, size=(800,600))
display.start()

options=Options()
chrome_driver = '../abr_browser_dir/chromedriver'
options.add_argument('--user-data-dir=' + "/tmp/chrome_user_dir_real_exp_0")
options.add_argument('--ignore-certificate-errors')
options.add_argument("--autoplay-policy=no-user-gesture-required")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')
driver=webdriver.Chrome(options=options)

try:
    driver.get(url)
    sleep(30)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
    display.stop()
