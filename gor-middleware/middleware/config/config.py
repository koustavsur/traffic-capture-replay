class Config:

    def __init__(self, topic_name, kafka_config,
                 filters):
        self.topic_name = topic_name
        self.kafka_config = kafka_config
        self.filters = filters

    def setConfig(self, topic_name, kafka_config):
        self.topic_name = topic_name
        self.kafka_config = kafka_config

    def getTopicName(self):
        return self.topic_name

    def getKafkaConfig(self):
        return self.kafka_config

    def getFilters(self):
        return self.filters
