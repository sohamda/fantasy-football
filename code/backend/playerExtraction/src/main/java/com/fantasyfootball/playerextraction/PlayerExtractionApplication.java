package com.fantasyfootball.playerextraction;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.azure.spring.data.cosmos.repository.config.EnableCosmosRepositories;

@SpringBootApplication
@EnableCosmosRepositories
public class PlayerExtractionApplication {

    public static void main(String[] args) {
        SpringApplication.run(PlayerExtractionApplication.class, args);
    }
}