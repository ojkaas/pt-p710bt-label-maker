import argparse

import os

PATH = os.path.dirname(__file__)


def set_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Label Maker for PT-P710BT')
    parser.add_argument('bt_address', nargs='?', help='Bluetooth address of device (eg. "EC:79:49:63:2A:80")')
    parser.add_argument('--image', type=str, help='Path to image to print')
    parser.add_argument('--mqtt_host', type=str, help='URL to MQTT broker')
    parser.add_argument('--mqtt_port', type=int, help='Port to MQTT broker')
    parser.add_argument('--mqtt_user', type=str, help='User of MQTT broker')
    parser.add_argument('--mqtt_password', type=str, help='Password of MQTT broker')
    parser.add_argument('--bt-channel', type=int, default=1, help='Bluetooth Channel to use')
    parser.add_argument('--set-default', action='store_true', help='Store the `bt_address` value as the default for '
                                                                   'future executions of the script')
    parser.add_argument('-i', '--info', action='store_true', help="Fetch information from the printer")
    return parser


def parse():
    parser = set_args()
    return parser.parse_args()