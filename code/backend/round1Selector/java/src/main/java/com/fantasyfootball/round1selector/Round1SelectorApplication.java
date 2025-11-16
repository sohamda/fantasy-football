package com.fantasyfootball.round1selector;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class Round1SelectorApplication {

    public static void main(String[] args) {
        SpringApplication.run(Round1SelectorApplication.class, args);
    }
}
