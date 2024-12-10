import json
from PySide6.QtCore import QObject, Signal
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import socket


class Client(QObject):
    on_connect = Signal(int, int, object)
    on_connect_fail = Signal()
    on_subscribe = Signal(int, list)
    on_message = Signal(str, object, int, bool, object)
    on_publish = Signal(int, int)
    on_unsubscribe = Signal(int, list)
    on_disconnect = Signal(int, int)

    def __init__(self, client_id="", clean_session=None, userdata=None, protocol=mqtt.MQTTv5, transport="tcp", reconnect_on_failure=True, manual_ack=False, parent=None):
        super().__init__(parent)
        self.__mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id, clean_session, userdata, protocol, transport, reconnect_on_failure, manual_ack)

        self.__mqtt.on_connect = self.__on_connect
        self.__mqtt.on_connect_fail = self.__on_connect_fail
        self.__mqtt.on_subscribe = self.__on_subscribe
        self.__mqtt.on_message = self.__on_message
        self.__mqtt.on_publish = self.__on_publish
        self.__mqtt.on_unsubscribe = self.__on_unsubscribe
        self.__mqtt.on_disconnect = self.__on_disconnect
        
    def __del__(self):
        if self.__mqtt.is_connected():
            self.disconnect()
    
    def connection(self, host, port=1883, keepalive=60, bind_address="", bind_port=0, clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY, session_expiry_interval=60, request_problem_information=True, username=None, password=None):
        try:
            connect_properties = Properties(PacketTypes.CONNECT)
            connect_properties.SessionExpiryInterval = session_expiry_interval
            connect_properties.RequestProblemInformation = request_problem_information
            
            self.__mqtt.username_pw_set(username, password)
            self.__mqtt.connect(host, port, keepalive, bind_address, bind_port, clean_start, connect_properties)
            self.__mqtt.loop_start()
        except socket.gaierror:
            if not self.__mqtt.on_connect:
                raise ValueError("Unknown host")
            else:
                self.__mqtt.on_connect(None, None, None, 3, None)
                
    def disconnection(self, reasoncode=None, properties=None):
        self.__mqtt.loop_stop()
        self.__mqtt.disconnect(reasoncode, properties)

    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        self.__mqtt.publish(topic, json.dumps(payload), qos, retain, properties)

    def subscribe(self, topic, qos=0, options=None, properties=None):
        self.__mqtt.subscribe(topic, qos, options, properties)
    
    def unsubscribe(self, topic, properties=None):
        self.__mqtt.unsubscribe(topic, properties)
    
    def will_set(self, topic, payload=None, qos=0, retain=False, properties=None):
        self.__mqtt.will_set(topic, payload, qos, retain, properties)
    
    def will_clear(self):
        self.__mqtt.will_clear()
    
    def __on_connect(self, client, userdata, flags, reason_code, properties):
        self.on_connect.emit(flags, reason_code, properties)
    
    def __on_connect_fail(self, client, userdata):
        self.on_connect_fail.emit()
    
    def __on_subscribe(self, client, userdata, mid, reason_code_list, properties):
        self.on_subscribe.emit(mid, reason_code_list)
    
    def __on_message(self, client, userdata, message):
        self.on_message.emit(message.topic, json.loads(message.payload), message.qos, message.retain, message.properties)
    
    def __on_publish(self, client, userdata, mid, reason_code, properties):
        self.on_publish.emit(mid, reason_code)
    
    def __on_unsubscribe(self, client, userdata, mid, reason_code_list, properties):
        self.on_unsubscribe.emit(mid, reason_code_list)
    
    def __on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        self.on_disconnect.emit(disconnect_flags, reason_code)
        