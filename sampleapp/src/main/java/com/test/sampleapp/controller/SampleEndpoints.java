package com.test.sampleapp.controller;


import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;


@Controller
@RequestMapping("/sample")
@Slf4j
public class SampleEndpoints {


    @GetMapping("/getData")
    public ResponseEntity<String> getData() {
        return ResponseEntity.ok().body("Success got data");
    }

    @PostMapping("/postData")
    public ResponseEntity<String> createUser(@RequestBody String value) {
        log.info(value);
        return ResponseEntity.ok().body("Successfully posted data: "+value);
    }
}
