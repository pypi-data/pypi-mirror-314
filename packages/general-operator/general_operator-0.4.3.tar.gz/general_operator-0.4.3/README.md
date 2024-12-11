# node_object_module version 2.3.3

* API node rule
  1. API node 包含四張表(node, node_base, device_info, third_dimension_instance)一對一關係
  2. 只能透過API node的update去修改或新增device_info和third_dimension_instance這兩張表
  3. node只能有一個parent node, 可以有多個child nodes
  4. 跟node groups的關係是多對多
  5. 刪除node會連同底下所有的child nodes和所有此node和child nodes底下的object都刪除
     ![node_delete.png](image/node_delete.png)
* API object rule
  1. API object 包含四張表(object, object_base, fake_data_config, fake_data_config_base)一對一關係
  2. 只能透過API object的update去修改或新增其他一對一的表
  3. object只能綁定一個node
  4. 跟object groups的關係是多對多
  5. insert object的value會完全取代原本的value, 只修改redis的表, 不修改sql
* API object value
  1. history value儲存在influxDB
  2. latest value存redis和influxDB
  3. 取得history value從influxDB讀取
  4. 取得latest value從redis取
  5. 取得即時有改變的資料使用websocket連線(ws://{host}:{port}/ws/)
* API control href group
  1. create 可以創建group 和 item
  2. update 如果item有帶id就是修改, 如果沒有帶id就是創建新的item, 如果帶負數id會刪除此item
  3. delete 會連同底下item一起刪除

## Design

![design.png](image/design.png)

### General Table Operate CRUD

Read Data
![Read.png](image/Read.png)

Create Data
![Create.png](image/Create.png)

Update Data
![Update.png](image/Update.png)

Delete Data
![Delete.png](image/Delete.png)

## DB diagram

[DB schemas](https://dbdiagram.io/d/63073decf1a9b01b0fdf20a3)

![db_node_object.png](image/db_node_object.png)

## Deploy

#### 1. Use docker-compose

1. install mysql, redis and influxdb

   `docker pull mssql`

   `docker pull redis`

    `docker pull influxdb`
2. start docker-compose.yaml

   `docker-compose up --build -d`

#### 2. Use Dockerfile

需要先啟動mysql, redis, influxdb
可用環境變數db_host, redis_host去改變sql和redis的連線ip

1. build docker image "node_object"

   `docker build -t node_object:latest .`
2. run node_object image

   `docker run --name node_object --network="host" -p 9330:9330 node_object:latest`

    有環境變數
   `docker run --name node_object --network="host" -e db_host=192.168.1.11 -e redis_host=192.168.1.11 -e influx_host=192.168.1.11 -p 9330:9330 -d node_object:latest`

## Swagger API Document

http://{host}:{port}/docs
![swagger.png](image/swagger.png)
