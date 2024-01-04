# traffic-capture-replay
Capture traffic (Request/Response) via Go replay-> publish to kafka topic -> consume from kafka topic

Local Setup of traffic replay (MAC):
1. Check for homebrew :
   Command: which brew 
   Expected result: /opt/homebrew/bin/brew
   If not present -> Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Install Kafka:
    brew install kafka

3. Start zookeeper and kafka services in local from terminal:
    brew services start zookeeper
    brew services start kafka
    N.B : Kafka will be running on server port 9092.

4. To get the list of topics present in kafka: 
    kafka-topics --list --bootstrap-server localhost:9092 (if kafka-topics is not detected use /opt/homebrew/bin/kafka-topics)

5. Create a topic in kafka:
    kafka-topics --create --bootstrap-server localhost:9092 --topic test_topic

6. To test kafka topic :
    Producer: kafka-console-producer --topic test_topic --bootstrap-server localhost:9092 (Publish message)
    Consumer: kafka-console-consumer --topic test_topic --bootstrap-server localhost:9092 (Consume message from a different terminal)

7. Clone the repo: https://github.com/koustavsur/traffic-capture-replay
    git clone : git@github.com:koustavsur/traffic-capture-replay.git

8.  Run GOR in local:
    Extract gor_1.3.3_mac.tar.gz
    Run from gor-middleware directory: sudo -E ./gor --input-raw :8081 --middleware "middleware/middleware.py" --input-raw-track-response --output-http "http://localhost:8082";

9. Build and Run the consumer/replay service:
    From intellij: Open the replay project and Click on Build and run.(service will be running in port 8083)
    From command line: Go to replay folder
    mvn clean install -DskipTests -> To generate the jar file
    java -jar <target_path_jar_file>.jar -> Run the jar

10. Build and Run the sample app 
    From intellij: Open the sampleapp project and Click on Build and run.(service will be running in port 8081)
    From command line: Go to sampleapp folder
    mvn clean install -DskipTests -> To generate the jar file
    java -jar <target_path_jar_file>.jar -> Run the jar

Our application is running on port 8081. Exposed endpoints are : GET (http://localhost:8081/sample/getData) and POST(http://localhost:8081/sample/postData)
Sample curl command:

GET call:
curl --location 'http://localhost:8081/sample/getData'

POST call: 
curl --location 'http://localhost:8081/sample/postData' \
--header 'Content-Type: text/plain' \
--data '{
    "body"
}'

Whenever you will make call to any of the endpoints traffic will be getting captured and consumed in the replay service, and logged. Which can be further extended to replay/analyse/monitor.
