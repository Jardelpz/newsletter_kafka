`docker-compose -f docker-compose.yml up`


docker exec -it kafka /bin/sh


cd opt/kafka_2.13-2.8.1/bin
to test: kafka-topics.sh --zookeeper zookeeper:2181 --list
see messages: kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic testtopic --from-beginning