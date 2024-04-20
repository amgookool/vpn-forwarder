# VPN-Forwarder Script

This script is used to port forward the wireguard VPN server to the internet through the Digicel router.

The script uses selenium to automate the process of port forwarding on the Digicel router.

## Requirements

- Python 3
- Environment Variables
  - `ROUTER_IP`: The IP address of the Digicel router in the format `http://` followed by the IP address.
  - `ROUTER_USERNAME`: The username of the Digicel router.
  - `ROUTER_PASSWORD`: The password of the Digicel router.
