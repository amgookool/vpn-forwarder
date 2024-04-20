"""Script to set the correct public IP address in the Digicel Router """

import os
import time
from typing import List

import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

public_ip = requests.get("https://api.ipify.org?format=json").json()["ip"]

ROUTER_IP = os.getenv("ROUTER_IP")
ROUTER_USERNAME = os.getenv("ROUTER_USERNAME")
ROUTER_PASSWORD = os.getenv("ROUTER_PASSWORD")


service = Service(ChromeDriverManager().install())
options = Options()
# # options.add_experimental_option("detach", True)
# # options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)
driver.get(ROUTER_IP)

account_element = driver.find_element(by=By.ID, value="txt_Username")
password_element = driver.find_element(by=By.ID, value="txt_Password")
login_button_element = driver.find_element(by=By.ID, value="button")
account_element.send_keys(ROUTER_USERNAME)
password_element.send_keys(ROUTER_PASSWORD)
login_button_element.click()

driver.implicitly_wait(5)
driver.get(f"{ROUTER_IP}/html/bbsp/pcp/pcp.asp")

forward_rules_tab_element = driver.find_element(by=By.ID, value="PcpConfigList_tbl")
forward_rules_table_items: List[WebElement] = forward_rules_tab_element.find_elements(
    by=By.TAG_NAME, value="tr"
)

row_to_edit = None
for e in forward_rules_table_items[1:]:
    row_data = e.find_elements(by=By.TAG_NAME, value="td")
    for rd in row_data:
        for r in rd.find_elements(by=By.TAG_NAME, value="tr")[1:]:
            data_elements = r.find_elements(by=By.TAG_NAME, value="td")
            if data_elements[1].text == "Manual" and data_elements[2].text == public_ip:
                #     # print("Already set")
                #     # break
                row_to_edit = r
                print(row_to_edit.text)
                row_to_edit.click()
                time.sleep(10)
                edit_box = driver.find_element(
                    by=By.ID, value="RequiredExternalAddress"
                )
                print(edit_box.text)
                edit_box.clear()
                time.sleep(5)
                edit_box.send_keys(public_ip)
            # else:
            #     row_to_edit = r
            #     print(row_to_edit.text)

        break
    break
