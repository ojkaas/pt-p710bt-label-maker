import paho.mqtt.client as mqtt
import subprocess
import os
import app_args_mqtt

from config import set_defaults, get_defaults
from label_maker import bad_options, get_printer_info, make_label


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("label/print")

def on_message(client, userdata, msg):
    text = msg.payload.decode()
    print("Print message: " + text)
    #subprocess.run(["convert", "-size", "300x70", "xc:none", "-gravity", "Center",
    #                "-pointsize", "35", "-annotate", "0",
    #                f"{text}", "result.png"])
    make_label(userdata)
    #os.system('python3.9 label_maker.py CHANGETODEVICEMACADDRESS --image result.png')

def connect_and_listen(options):
    client = mqtt.Client(userdata=options)
    client.on_connect = on_connect
    client.on_message = on_message

    if options.setdefault and options:
        client.username_pw_set("username", "password")

    client.connect(options.mqtt_host, options.mqtt_port, 60)
    client.loop_forever()

def main():
    options = app_args_mqtt.parse()
    defaults = get_defaults()

    if not options.info and not options.image:
        bad_options('Image path required')

    if options.set_default:
        if not options.bt_address:
            bad_options('You must provide a BT address to set as default')
        if not options.mqtt_host:
            bad_options('You must provide a MQTT host to set as default')
        if not options.mqtt_port:
            bad_options('You must provide a MQTT port to set as default')

        else:
            set_defaults(options.bt_address,options.mqtt_host,options.mqtt_port,options.mqtt_user,options.mqtt_password)
            print(f"{options.bt_address} set as default BT address")
            print(f"{options.mqtt_host} set as default BT address")
            print(f"{options.mqtt_port} set as default BT address")

            if options.mqtt_user:
                print(f"{options.mqtt_user} set as default BT address")

    if not options.bt_address:        
        if not defaults['default_bt']:
            bad_options("BT Address is required. If you'd like to remember it use --set-default")
        options.bt_address = defaults['default_bt'];
        print(f"Using BT Address of {options.bt_address}")
    
    if not options.mqtt_host:
        if not defaults['host']:
            bad_options("MQTT Host is required. If you'd like to remember it use --set-default")
        options.mqtt_host = defaults['host'];
        print(f"Using MQTT Host of {options.mqtt_host}")

    if not options.mqtt_port:
        if not defaults['port']:
            bad_options("MQTT Port is required. If you'd like to remember it use --set-default")
        options.mqtt_port = defaults['port'];
        print(f"Using MQTT Port of {options.mqtt_port}")

    if not options.mqtt_user:
        if defaults['user']:
            options.mqtt_user = defaults['user'];
            print(f"Using MQTT User of {options.mqtt_user}")
    
    if not options.mqtt_password:
        if defaults['password']:
            options.mqtt_password = defaults['password'];
            print(f"Using MQTT Password of {options.mqtt_password}")
        
    if options.info:
        get_printer_info(options.bt_address, options.bt_channel)
        exit(0)