"""This module contains the driver class for the web scraper."""

import time
from typing import List
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

logger = logging.getLogger(__name__)

def get_driver(use_edge: bool = False):
    logger.info("Getting web driver")
    if not use_edge:
        service = Service(ChromeDriverManager().install())
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        return webdriver.Chrome(service=service, options=options)
    else:
        service = Service(EdgeChromiumDriverManager().install())
        options = EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        return webdriver.Edge(service=service, options=options)


def load_router_page(
    driver: WebDriver, router_ip: str, router_username: str, router_password: str
):
    logger.info("Loading router Login page")
    driver.get(router_ip)
    account_element = driver.find_element(by=By.ID, value="txt_Username")
    password_element = driver.find_element(by=By.ID, value="txt_Password")
    login_button_element = driver.find_element(by=By.ID, value="button")
    account_element.send_keys(router_username)
    password_element.send_keys(router_password)
    login_button_element.click()
    return driver.implicitly_wait(3)


def load_port_forwarding_page(driver: WebDriver, router_ip: str):
    logger.info("Loading port forwarding page")
    driver.get(f"{router_ip}/html/bbsp/pcp/pcp.asp")
    return driver.implicitly_wait(5)


def parse_port_forwarding_table(driver: WebDriver):
    logger.info("Parsing port forwarding table")
    forward_rules_tab_element = driver.find_element(by=By.ID, value="PcpConfigList_tbl")
    forward_rules_table_items: List[WebElement] = (
        forward_rules_tab_element.find_elements(by=By.TAG_NAME, value="tr")
    )
    return forward_rules_table_items


def check_port_forwarding_rule(
    public_ip: str,
    vpn_server_ip: str,
    forward_rules_table_items: List[WebElement],
):
    logger.info("Checking port forwarding rule")
    row_to_edit = None
    for e in forward_rules_table_items[1:]:
        row_data = e.find_elements(by=By.TAG_NAME, value="td")
        for rd in row_data:
            for r in rd.find_elements(by=By.TAG_NAME, value="tr")[1:]:
                data_elements = r.find_elements(by=By.TAG_NAME, value="td")
                if (
                    data_elements[1].text == "Manual"
                    and data_elements[2].text == public_ip
                    and data_elements[6].text == vpn_server_ip
                ):
                    logger.info("Port forwarding rule found is up to date")
                    return None
                else:
                    row_to_edit = r
                    row_to_edit.click()
                    return row_to_edit


def perform_update_to_port_forwarding_rule(
    driver: WebDriver, public_ip: str, vpn_server_ip: str
):
    logger.info("Performing update to port forwarding rule")
    edit_box = driver.find_element(by=By.ID, value="RequiredExternalAddress")
    print(edit_box.text)
    edit_box.clear()
    time.sleep(1)
    edit_box.send_keys(public_ip)
    applyButton = driver.find_element(by=By.ID, value="ButtonApp")
    applyButton.click()
    return driver.implicitly_wait(3)
