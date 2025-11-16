package com.fantasyfootball.playerextraction.cosmosdb;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.azure.cosmos.CosmosClientBuilder;
import com.azure.spring.data.cosmos.config.AbstractCosmosConfiguration;

@Configuration
public class CosmosDbConfiguration extends AbstractCosmosConfiguration {
    
    @Value("${azure.cosmos.uri}")
    private String uri;
    
    @Value("${azure.cosmos.key}")
    private String key;
    
    @Value("${azure.cosmos.database}")
    private String dbName;
    
    @Bean
    public CosmosClientBuilder getCosmosClientBuilder() {
        return new CosmosClientBuilder()
                .endpoint(uri)
                .key(key);
    }
    
    @Override
    protected String getDatabaseName() {
        return dbName;
    }
}