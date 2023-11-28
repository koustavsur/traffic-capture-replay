#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import constants
from common import log
from publisher import Publisher
from config.config import Config
from config import config_properties


if __name__ == '__main__':

    try:
        # Get Topic from environment
        topic = os.environ.get(constants.KAFKA_TOPIC)
        # Get filters to block from environment
        filters = os.environ.get(constants.FILTER)

        if topic is None:
            topic = config_properties.KAFKA_TOPIC
        if filters is None:
            filters = ""

        log("Topic={}, Filters={}".format(topic, filters))

        config = Config(topic, config_properties.KAFKA_CONFIG, filters)
        log("Config Set. Filter={}".format(config.getFilters()))

        log("Before publish")
        publisher = Publisher(config)
        delivered_records = publisher.publish()
        log("messages produced={} , topic={}".format(delivered_records, config.getTopicName()))

    except Exception as ex:  # lgtm[py/conflicting-attributes]
        log("Exception during initialization. Exception={}".format(ex))
