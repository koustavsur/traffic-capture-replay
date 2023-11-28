import binascii
import fileinput
from confluent_kafka import Producer
import constants
import sys
from common import log
from requestType import RequestType
from config import config_properties
import base64
import time


class Publisher:

    def __init__(self, config):
        self.config = config
        self.delivered_records = 0
        self.blocked_request_ids = set()

    @staticmethod
    def find_end_of_headers(byte_data):
        """
        Finds where the header portion ends and the content portion begins.
        """
        return byte_data.index(constants.EMPTY_LINE) + 4

    def acknowledged(self, err, msg):
        if err is not None:
            log("Failed to deliver message={}".format(err))
        else:
            self.delivered_records += 1
            log(
                "Produced record to topic={} , partition=[{}] , offset={} , Total delivered={}".format(
                    msg.topic(), msg.partition(), msg.offset(), self.delivered_records
                )
            )

    def isPublishAllowed(self, metadata, header):
        request_id = self.getRequestId(metadata)
        log('RequestId={}'.format(request_id))
        request_type_id = int(metadata.split(b' ')[0])

        if request_type_id == RequestType.Request.value:
            if self.isEndpointBlocked(header):
                self.blocked_request_ids.add(request_id)
                return False

        elif request_type_id == RequestType.Original_Response.value and request_id in self.blocked_request_ids:
            self.blocked_request_ids.discard(request_id)
            return False

        return True

    def isEndpointBlocked(self, header):
        if self.config.getFilters() == "" or self.config.getFilters() is None:
            return False
        filter_content = self.config.getFilters().split(',')
        stripped_content = [s.strip() for s in filter_content]
        endpoint = str(header.split(b' ')[1])
        if any(ext in endpoint for ext in stripped_content):
            log('Blocking_Request={}'.format(endpoint))
            return True

    def clearRequestSetIfNeeded(self):
        if len(self.blocked_request_ids) > 1000:
            self.blocked_request_ids.clear()

    @staticmethod
    def logRequestType(metadata):
        log('===================================')
        request_type_id = int(metadata.split(b' ')[0])
        log('Request type={}'.format(RequestType(request_type_id).name))
        log('===================================')

    @staticmethod
    def getRequestId(metadata):
        # Get the request id and request type from metadata b'1 8f5a1f907f0000017c3474ef 1646023571803175588 0'
        # RequestID: b'8f5a1f907f0000017c3474ef'
        # Request type: b'1'
        return str(metadata.split(b' ')[1])[2:-1]

    def publishToKafka(self, producer, message):

        producer.produce(self.config.getTopicName(), message,
                         callback=self.acknowledged)
        producer.poll(0)
        producer.flush()

    def splitHeaderPayload(self, payload):
        headers_pos = self.find_end_of_headers(payload)
        raw_headers = payload[:headers_pos]
        raw_content = payload[headers_pos:]
        return raw_headers, raw_content

    @staticmethod
    def encodeOutput(data):
        encoded = binascii.hexlify(data).decode('ascii')
        sys.stdout.write(encoded + '\n')
        sys.stdout.flush()


    def publish(self):
        log("Topic={}".format(self.config.getTopicName()))

        producer = Producer(self.config.getKafkaConfig())
        log("producer initialized")
        """
        Process STDIN and output to STDOUT
        """
        for raw_line in fileinput.input():
            line = raw_line.rstrip()
            # Decode base64 encoded line
            decoded = bytes.fromhex(line)
            # Split into metadata and payload, the payload is headers + body
            (raw_metadata, payload) = decoded.split(b'\n', 1)
            # Split into headers and payload
            raw_headers, raw_content = self.splitHeaderPayload(payload)
            self.logRequestType(raw_metadata)

            try:
                self.clearRequestSetIfNeeded()

                if not self.isPublishAllowed(raw_metadata, raw_headers):
                    continue

                data = raw_metadata + b'\n' + raw_headers + raw_content
                # base64 encoding of the captured request/response
                encoded_data = base64.b64encode(data)
                self.publishToKafka(producer, encoded_data)

                self.encodeOutput(data)

            except Exception as e:  # lgtm[py/conflicting-attributes]
                log("Exception while publishing record, EX_TOPIC={} ,EX_PUBLISH_RECORD={}".
                    format(self.config.getTopicName(), e))
                continue

        return self.delivered_records
