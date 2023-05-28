from fastapi import FastAPI
from init import init
from routers import *
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig

init()

app = FastAPI()
app.include_router(user.router)
app.include_router(tools.router)
app.include_router(auth.router)
app.include_router(budget.router)
mqtt_config = MQTTConfig(host="192.168.25.110", port=1883, keepalive=60)
mqtt = FastMQTT(config=mqtt_config)
mqtt.init_app(app)

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/room105/sensors/class_here")
    print("Connected: ", client, flags, rc, properties)
    return 0

@mqtt.on_message()
async def message(client, topic, payload: bytes, qos, properties):
    print(type(qos))
    print("Received message: ",topic, payload.decode(), qos, properties)
    return 0

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")