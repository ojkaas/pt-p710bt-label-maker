import paho.mqtt.client as mqtt

import subprocess
import os
import app_args_mqtt

from config import set_defaults, get_defaults
from label_maker import bad_options, get_printer_info, make_label, connect_bluetooth, get_media_height
from image_generator import text_to_image, calculate_font_size

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("label/print")

def on_message(client, userdata, msg):
    text = msg.payload.decode()
    print("Print message: " + text)
    
    socket = connect_bluetooth(userdata.bt_address, userdata.bt_channel);
    get_printer_info(socket);
    height = get_media_height();
    print("Media height: " + str(height))
    image = text_to_image(text,height)
    image.save("text.png")

    #subprocess.run(["convert", "-size", "300x70", "xc:none", "-gravity", "Center",
    #                "-pointsize", "35", "-annotate", "0",
    #                f"{text}", "result.png"])
    make_label(userdata)
    #os.system('python3.9 label_maker.py CHANGETODEVICEMACADDRESS --image result.png')

def connect_and_listen(options):
    client = mqtt.Client(userdata=options)
    client.on_connect = on_connect
    client.on_message = on_message

    if options.mqtt_user and options.mqtt_password:
        client.username_pw_set(options.mqtt_user, options.mqtt_password)

    client.connect(options.mqtt_host, options.mqtt_port, 60)
    client.loop_forever()



def main():
    options = app_args_mqtt.parse()
    defaults = get_defaults()

    if options.set_default:
        if not options.bt_address:
            bad_options('You must provide a BT address to set as default')
        if not options.mqtt_host:
            bad_options('You must provide a MQTT host to set as default')
        if not options.mqtt_port:
            bad_options('You must provide a MQTT port to set as default')

        else:
            set_defaults(options.bt_address,options.mqtt_host,options.mqtt_port,options.mqtt_password,options.mqtt_user)
            print(f"{options.bt_address} set as default BT address")
            print(f"{options.mqtt_host} set as default MQTT host")
            print(f"{options.mqtt_port} set as default MQTT port")

            if options.mqtt_user:
                print(f"{options.mqtt_user} set as default MQTT User")
            if options.mqtt_password:
                print(f"{options.mqtt_password} set as default MQTT Password")

    if not options.bt_address:        
        if not 'default_bt' in defaults:
            bad_options("BT Address is required. If you'd like to remember it use --set-default")
        options.bt_address = defaults['default_bt'];
        print(f"Using BT Address of {options.bt_address}")
    
    if not options.mqtt_host:
        if not 'host' in defaults:
            bad_options("MQTT Host is required. If you'd like to remember it use --set-default")
        options.mqtt_host = defaults['host'];
        print(f"Using MQTT Host of {options.mqtt_host}")

    if not options.mqtt_port:
        if not 'port' in defaults:
            bad_options("MQTT Port is required. If you'd like to remember it use --set-default")
        options.mqtt_port = defaults['port'];
        print(f"Using MQTT Port of {options.mqtt_port}")

    if not options.mqtt_user:
        if 'username' in defaults:
            options.mqtt_user = defaults['username'];
            print(f"Using MQTT User of {options.mqtt_user}")
    
    if not options.mqtt_password:
        if 'password' in defaults:
            options.mqtt_password = defaults['password'];
            print(f"Using MQTT Password of {options.mqtt_password}")
        
    if options.info:
        get_printer_info(options.bt_address, options.bt_channel)
        exit(0)
    
    connect_and_listen(options)

if __name__ == "__main__":
    main()