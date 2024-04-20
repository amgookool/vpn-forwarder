# VPN-Forwarder Script

This script is used to port forward the wireguard VPN server to the internet through the Digicel router.

The script uses selenium to automate the process of port forwarding on the Digicel router.

## Requirements

- Python 3
- Environment Variables
  - `ROUTER_IP`: The IP address of the Digicel router in the format `http://` followed by the IP address.
  - `ROUTER_USERNAME`: The username of the Digicel router.
  - `ROUTER_PASSWORD`: The password of the Digicel router.
  - `VPN_SERVER_IP`: The Internal IP address of the VPN server.
  - `CHECK_INTERVAL`: The interval in minutes to check if the port forwarding is still active.

## Usage

1. Install the required packages by running `pip install -r requirements.txt`.
2. Set the environment variables by creating a `.env` file.
3. Run the script by running `python main.py`.

## Docker Usage

1. Build the docker image by running `docker build -t vpn-forwarder .`.
2. Run the docker container by running `docker run -d --name vpn-forwarder -e ROUTER_IP=<ROUTER_IP> -e ROUTER_USERNAME=<ROUTER_USERNAME> -e ROUTER_PASSWORD=<ROUTER_PASSWORD> -e VPN_SERVER_IP=<VPN_SERVER_IP> -e CHECK_INTERVAL=<integer> vpn-forwarder`.
