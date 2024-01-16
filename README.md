# MQTT-to-ThingsBoard-Temp-Humi-
Đoạn mã Python này là một ứng dụng đơn giản sử dụng thư viện Paho MQTT và Requests để kết nối và tương tác với một broker MQTT (esp32) và ThingsBoard thông qua giao thức MQTT và HTTP API. Dưới đây là mô tả tổng quan của mã nguồn:

1. **Thiết lập thông tin kết nối MQTT và ThingsBoard:**
    - Địa chỉ và cổng của broker MQTT (`mqtt_broker_host`, `mqtt_broker_port`).
    - Các chủ đề MQTT cho nhiệt độ và độ ẩm (`mqtt_temperature_topic`, `mqtt_humidity_topic`).
    - Địa chỉ và token xác thực của ThingsBoard (`thingsboard_host`, `thingsboard_access_token`).

2. **Biến toàn cục cho dữ liệu nhiệt độ và độ ẩm:**
    - `current_temperature` và `current_humidity` được sử dụng để lưu trữ giá trị nhiệt độ và độ ẩm từ thông điệp MQTT.

3. **Hàm xử lý sự kiện khi kết nối đến MQTT broker (`on_connect`):**
    - In thông báo khi kết nối thành công.
    - Đăng ký đăng ký theo dõi các chủ đề nhiệt độ và độ ẩm.

4. **Hàm xử lý sự kiện khi nhận thông điệp từ MQTT broker (`on_message`):**
    - Giải mã thông điệp và gán giá trị cho biến `current_temperature` hoặc `current_humidity` tùy thuộc vào chủ đề.
    - Nếu cả hai giá trị đã được nhận, thì gửi dữ liệu lên ThingsBoard qua HTTP API.
    - In ra thông báo khi dữ liệu được gửi thành công hoặc thông báo lỗi nếu quá trình gửi thất bại.

5. **Thiết lập MQTT Client:**
    - Tạo một đối tượng MQTT client và gán các hàm xử lý sự kiện (`on_connect` và `on_message`) cho client.

6. **Kết nối đến MQTT Broker và lặp vô hạn:**
    - Kết nối đến broker MQTT với địa chỉ, cổng và thời gian giữ kết nối được thiết lập trước.
    - Bắt đầu một vòng lặp vô hạn để duy trì kết nối và xử lý sự kiện nhận thông điệp từ broker.

Tổng quan, đoạn mã này nhận dữ liệu nhiệt độ và độ ẩm từ thiết bị esp32 thông qua MQTT, sau đó gửi dữ liệu này lên ThingsBoard thông qua HTTP API.

# CHI TIẾT XEM BÊN DƯỚI

# Import những thư viện cần thiết "paho.mqtt.client" cho MQTT
```sh
import paho.mqtt.client as mqtt
```
# Thư viện "requests" cho HTTP 
```sh
import request
```
# Thư viện "json" để làm việc với kiểu dữ liệu json 
```sh
import json
```
# Đặt thông tin kết nối cho MQTT broker, bao gồm địa chỉ và cổng broker, cũng như các chủ để MQTT cho nhiệt độ và độ ẩm 
```sh
mqtt_broker_host = "192.168.1.148"
mqtt_broker_port = 1884
mqtt_temperature_topic = "esp32/temperature" // chủ đề mà sensor gửi tới 
mqtt_humidity_topic = "esp32/humidity" // chủ đề mà sensor gửi tới
```
# Đặt thông tin kết nối cho thingsboard, bao gồm địa chỉ và token truy cập 
```sh
thingsboard_host = "http://localhost:8080" // tùy địa chỉ thingsboard sử dụng
thingsboard_access_token = "nhập access token của device"
```
# Khởi tạo biến lưu trữ nhiệt độ và độ ẩm hiện tại, ban đầu đặt là none 
```sh
current_temperature = None
current_humidity = None
```
# Định nghĩa hàm xử lý sự kiện khi kết nối đến MQTT broker thành công. In thông báo và đăng ký theo dõi các chủ đề nhiệt độ và độ ẩm
```sh
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code" + str(rc))
    client.subcribe([mqtt_temperature_topic, 0), (mqtt_humidity_topic, 0)])
```
- Hàm `on_connect` được gọi khi MQTT client kết nối thành công đến MQTT broker. Ở trong trường hợp này nó được sử dụng để hiển thị thông báo kết nối thành công và đăng ký theo dõi các chủ đề client muốn theo dõi 
- Định nghĩa hàm `on_connect` với bốn tham số `client` là đối tượng MQTT client
- Tham số `userdata` là dữ liệu người dùng (có thể được đặt khi tạo client, nhưng không được sử dụng ở đây )
- Tham số `flags` là cờ (không được sử dụng ở đây)
- Tham số `rc` là mã kết quả của quá trình kết nối.
- `print("Connected to MQTT Broker with result code " + str(rc))` : In ra thông báo cho biết client đã kết nối thành công đến MQTT broker và hiển thị mã kết quả (`rc`), `str(rc)` được sử dụng để chuyển đổi mã kết quả thành chuỗi để nó có thể được kết nối với chuỗi thông báo.
- `client.subscribe([(mqtt_temperature_topic, 0), (mqtt_humidity_topic, 0)])` : Sử dụng phuontw thức `subcribe` của đối tượng MQTT client để đăng ký theo dõi chủ đề, `mqtt_temperature_topic` và `mqtt_humidity_topic` là hai biến chứa tên của chủ đề nhiệt độ và độ ẩm đã được thiết lập trước đó.
- Mức độ chất lượng (`QoS`) được thiết lập là 0 cho cả 2 chủ đề, đồng nghĩa với việc chỉ gửi mỗi thông điệp một lần và không cần xác nhận.
# Định nghĩa hàm xử lý sự kiện khi nhận được thông tin từ MQTT broker. Xử lý dữ liệu nhận được từ thông điệp, lưu trữ nó trong biến toàn cục. Nếu cả hai giá trị nhiệt độ và độ ẩm đều được nhận, thì sau đó gửi chúng lên thingsboard thông qua HTTP API
```sh
def on_message(client, userdata, msg): //"on_mesage" Hàm gọi mỗi khi nhận được một thông điệp mới từ MQTT broker
global current_temperature, current_humidity  //Khai báo sử dụng biến toàn cục, vì chúng sẽ được cập nhật hàm này và sử dụng sau đó
```
- `gobal current_temperature, current_humidity` : Khai báo rằng các biến `current_temperature` và `current_humidity` sẽ được sử dụng trong hàm này là biến toàn cục. Các biến toàn cục có thể được thay đổi và truy cập từ bất kỳ nơi nào trong chương trình.
```sh
try:
print(f"Received MQTT message: {msg.payload}") 
value = float(msg.payload.decode()) // Nơi xử lý thông điệp nhận được từ broker MQTT
```
- `tryy:` : Bắt đầu mooit khối try-except để xử lý các ngoại lệ (lỗi) có thể xảy ra trong quá trình xử lý thông điệp.
- `print...` In ra màn hình nội dung của thông điệp MQTT mà client vừa nhận được, điều này giúp theo dõi và kiểm tra thông điệp.
- `value = float(msg.payload.decode())` : giải mã nội dung của thông điệp từ dạng bytes sang chuỗi và sau dó chuyển đổi thành số thực `float`
- `float()` chuyển đổi chuỗi thành số thực (float). Giải sử rằng dữ liệu trong thông điệp là một giá trị số, VD: "25.5" 
- `msg.payload` Nội dung của thông điệp nhận được từ MQTT broker. Trong trường hợp này giả sử nó chứa dữ liệu về nhiệt độ hoặc độ ẩm
- `decode()` chuyển đổi dữ liệu từ dạng bytes sang chuỗi. Dữ liệu trong thông điệp thường được truyền dưới dạng bytes, vì vậy ta cần phải giải mã để có thể xử lý
```sh
if msg.topic == mqtt_temperature_topic:
   current_temperature = value
elif msg.topic == mqtt_humidity_topic:
   current_humidity = value
```
-  Kiểm tra chủ đề của thông điệp MQTT `msg.topic` và dựa vào chủ đề đó, gán giá trị `value` cho biến tương ứng `current_temperature` hoặc `current_humidity` 
- `if msg.topic == mqtt_temperature_topic:` So sánh chủ đề của thông điệp `msg.topic` với chủ đề của nhiệt độ `mqtt_temperature_topic` 
-  Nếu chủ đề của thông điệp là chủ đề nhiệt độ, thì gán giá trị của nhiệt độ `value` vào biến `current_temperature`. 
-  `elif msg.topic == mqtt_humidity_topic:
     current_humidity = value: ` Nếu chủ đề của thông điệp là chủ đề độ ẩm `mqtt_humidity_topic` thì gán giá trị của độ ẩm `value` vào biến `current_humidity` 
-  Sử dụng `elif` để đảm bảo rằng chỉ có một trong hai điều kiện trên được thực hiện ( Nếu chủ đề không phải nhiệt độ thì chắc chắn là độ ẩm ) 
# Kiểm tra thông điệp thuộc chủ đề nhiệt độ (`mqtt_temperature_topic`) hay độ ẩm (`mqtt_humidity_topic`). Dựa vào chủ đề, giá trị của thông điệp sẽ được gán vào biến tương ứng (`current_temperature` hoặc `current_humidity`). 
```sh
 if current_temperature is not None and current_humidity is not None:
            # Gửi dữ liệu lên ThingsBoard qua HTTP API
            thingsboard_url = f"{thingsboard_host}/api/v1/{thingsboard_access_token}/telemetry"
            payload = {"temperature": current_temperature, "humidity": current_humidity}
            headers = {"Content-Type": "application/json"}
            response = requests.post(thingsboard_url, data=json.dumps(payload), headers=headers)
```
#1. Kiểm tra chủ đề là nhiệt độ 
`if msg.topic == mqtt_temperature_topic: 
      current_temperature = value ` 
- Kiểm tra xem chủ đề của thông điệp `msg.topic` có trùng với chủ đề nhiệt độ (`mqtt_temperature_topic`) không. Nếu có, thì gnas giá trị `value` vào biến `current_temperature`

#2. Kiểm tra chủ đề là độ ẩm
`elif msg.topic == mqtt_humidity_topic:
      current_humidity = value `
- Nếu điều trên không được thực hiện (chủ đề không phải nhiệt độ), thì kiểm tra xem chủ đề có trùng với chủ đề độ ẩm (`mqtt_humidity_topic`) không.
- Nếu có, thì gán giá trị (`calue`) vào biến `current_humidity` .
- Sử dụng `elif` để đảm bảo rằng chỉ một trong hai điều kiện trên được thực hiện. Nếu chủ đề đó không phải nhiệt độ, chắc chắn là độ ẩm.

#3. Những dòng này cung cấp cách phân biệt giữa dữ liệu nhiệt độ và độ ẩm dựa trên chủ đề của thông điệp MQTT và sau đó lưu trữ giá trị tương ứng vào các biến `currrent_temperature` hoặc `current_humidity`. 

# Kiểm tra kết quả của yêu cầu HTTP (`response.status_code`). Nếu mã trạng thái là 200, tức là thành công: 
```sh
 if response.status_code == 200:
                print(f"Data sent to ThingsBoard: {payload}")
                # Reset values after sending data
                current_temperature = None
                current_humidity = None
```
- `print(f"Data sent to ThingsBoard: {payload}")` : In thông điệp xác nhận việc gửi dữ liệu lên ThingsBoard.
- Đặt lại giá trị của `current_temperature` và `current_humidity` về `None` để chuẩn bị nhận dữ liệu mới. 
```sh
print(f"Failed to send data to ThingsBoard. Status code: {response.status_code}")` 
```
- Nếu yêu cầu không thành công ( mã trạng thái không phải 200), in thông điệp lỗi và mã trạng thái để ghi log lỗi.
```sh
 except Exception as e:
        print(f"Error processing MQTT message: {e}")
```
- Bao lấy toàn bộ xử lý trong một khối `try...except` để bắt các ngoại lệ có thể xảy ra trong quá trình xử lý thông điệp từ MQTT broker. Nếu có lỗi, in thông báo lỗi.

# Thiết lập và cấu hình MQTT client để kết nối và tương tác với broker MQTT. 

#1. Tạo đối tượng MQTT client: 
```sh
mqtt_client = mqtt.Client()
```
- Tạo một đối tượng MQTT client thông qua việc khởi tạo lớp `mqtt.Client()`
- Đối tượng này sẽ được sử dụng để thiết lập và duy trì kết nối với MQTT brokerm cũng như đăng ký các hàm xử lý sự kiện.
```sh
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
```
- Gán hàm xử lý sự kiện `on_connect` cho sự kiện kết nối. Hàm này được gọi khi kết nối đến MQTT broker thành công.
- Gán hàm xử lý sự kiện `on_message` chờ sự kiện nhận thông điệp. Hàm này được gọi mỗi khi client nhận được một thông điệp từ broker.
- Đối tượng MQTT client này sẽ tự động gọi các hàm này khi có sự kiện tương ứng xảy ra trong quá trình thực hiện.

# Kết nối đến MQTT broker và sau đó bắt đầu một vòng lặp vô hạn để duy trì kết nối và xử lý các sự kiện nhận thông điệp từ broker. 
```sh
# Kết nối tới MQTT Broker
mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)
```
- Sử dụng phương thức `connect` của đối tượng MQTT client để kết nối đến MQTT broker.
- Truyền vào địa chỉ (`mqtt_broker_host`) và cổng (`mqtt_broker_port`) của broker
- Tham số thứ ba (`60`) là thời gian giữ kết nối (keep alive), đơn vị là giây
```sh
mqtt_client.loop_forever()
```
- Sử dụng phương thức `loop_forever` của đối tượng MQTT client để bắt đầu một vòng lặp vô hạn.
- Trong vòng lặp này, client sẽ liên tục lắng nghe và xủ lý các sự kiện nhận thông điệp, cũng như duy trì kết nối đến MQTT broker.
- Lệnh này sẽ chạy vô hạn, nên sau khi kết nối đến broker, client sẽ duy trì kết nối và thực hiện các xử lý khi có thông điệp mới. 
