import paho.mqtt.client as mqtt
import requests
import json

# Thiết lập thông tin kết nối MQTT
mqtt_broker_host = "192.168.1.148"
mqtt_broker_port = 1884
mqtt_temperature_topic = "esp32/temperature"
mqtt_humidity_topic = "esp32/humidity"

# Thiết lập thông tin kết nối ThingsBoard
thingsboard_host = "http://localhost:8080"
thingsboard_access_token = "IlBvTvKqEJgVQLcyHIeo"

current_temperature = None
current_humidity = None

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe([(mqtt_temperature_topic, 0), (mqtt_humidity_topic, 0)])

def on_message(client, userdata, msg):
    global current_temperature, current_humidity

    try:
        print(f"Received MQTT message: {msg.payload}")
        value = float(msg.payload.decode())

        if msg.topic == mqtt_temperature_topic:
            current_temperature = value
        elif msg.topic == mqtt_humidity_topic:
            current_humidity = value

        # Check if both temperature and humidity are received
        if current_temperature is not None and current_humidity is not None:
            # Gửi dữ liệu lên ThingsBoard qua HTTP API
            thingsboard_url = f"{thingsboard_host}/api/v1/{thingsboard_access_token}/telemetry"
            payload = {"temperature": current_temperature, "humidity": current_humidity}
            headers = {"Content-Type": "application/json"}
            response = requests.post(thingsboard_url, data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                print(f"Data sent to ThingsBoard: {payload}")
                # Reset values after sending data
                current_temperature = None
                current_humidity = None
            else:
                print(f"Failed to send data to ThingsBoard. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error processing MQTT message: {e}")

# Thiết lập MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Kết nối tới MQTT Broker
mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)

# Lặp vô hạn để đọc dữ liệu từ MQTT và gửi lên ThingsBoard
mqtt_client.loop_forever()
