"""Script to set the correct public IP address in the Digicel Router """

import logging
import os
import time

import requests
import schedule
from dotenv import load_dotenv

from driver import (
    check_port_forwarding_rule,
    get_driver,
    load_port_forwarding_page,
    load_router_page,
    parse_port_forwarding_table,
    perform_update_to_port_forwarding_rule,
)


def perform_vpn_port_forwarding(use_edge=False):
    logger.info("Starting VPN Port Forwarding Check...")
    public_ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
    logger.info("Public IP fetched from external service: %s", public_ip)
    driver = get_driver(use_edge=use_edge)
    load_router_page(driver, ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD)
    load_port_forwarding_page(driver, ROUTER_IP)
    forward_rules_table_items = parse_port_forwarding_table(driver)
    row_to_edit = check_port_forwarding_rule(
        public_ip, VPN_SERVER_IP, forward_rules_table_items
    )
    if row_to_edit is not None:
        perform_update_to_port_forwarding_rule(driver, public_ip, VPN_SERVER_IP)
        logger.info("Updated Forwarding Rule Successfully")
    else:
        logger.info("No changes needed")
    driver.close()
    logger.info("VPN Port Forwarding Check Completed")


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S"
)

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))
ROUTER_IP = os.getenv("ROUTER_IP")
ROUTER_USERNAME = os.getenv("ROUTER_USERNAME")
ROUTER_PASSWORD = os.getenv("ROUTER_PASSWORD")
VPN_SERVER_IP = os.getenv("VPN_SERVER_IP")

if not ROUTER_IP or not ROUTER_USERNAME or not ROUTER_PASSWORD or not VPN_SERVER_IP:
    logger.error(
        "Please set the environment variables ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD and VPN_SERVER_IP"
    )
    exit(1)

logger.info("Checking interval set to %s minutes", CHECK_INTERVAL)
schedule.every(CHECK_INTERVAL).minutes.do(perform_vpn_port_forwarding)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
