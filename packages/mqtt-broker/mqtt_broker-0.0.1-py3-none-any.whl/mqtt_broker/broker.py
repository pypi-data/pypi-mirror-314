import os
import logging

from dotenv import load_dotenv
import paho.mqtt.client as mqtt

class Broker:

    def __init__(self, topic, client_id):

        load_dotenv()

        self.broker_hostname = os.environ.get('BROKER_HOSTNAME')
        self.port = int(os.environ.get('BROKER_PORT',8883))
        self.username = os.environ.get('BROKER_USERNAME')
        self.password = os.environ.get('BROKER_PASSWORD')
        self.cert_location = os.environ.get('CERTIFICATE_LOCATION')
        self.topic = topic
        self.client_id = client_id

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id, False)
        self.client.failed_connect = False


        def on_connect(client, userdata, flags, return_code, properties):
            if return_code == 0:
                logging.info("connected")
                
            else:
                logging.error("could not connect, return code:", return_code)
                self.client.failed_connect = True
            return client

        self.client.tls_set(ca_certs=self.cert_location)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        self.client.connect(self.broker_hostname, self.port)
        self.client.loop_start()

