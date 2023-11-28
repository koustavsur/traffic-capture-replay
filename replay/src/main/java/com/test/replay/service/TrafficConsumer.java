package com.test.replay.service;


import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.util.Base64;


@Service
public class TrafficConsumer {
    @KafkaListener(topics = "test_topic", groupId = "replay-group")
    public void cabLocation(String traffic) {
        byte[] decoded = Base64.getDecoder().decode(traffic);
        String decodedStr = new String(decoded, StandardCharsets.UTF_8);
        System.out.println(decodedStr);
        // Do whatever you want to do with the decoded request and response.
    }
}
