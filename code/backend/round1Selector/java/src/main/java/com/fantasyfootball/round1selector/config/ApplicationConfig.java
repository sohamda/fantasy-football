package com.fantasyfootball.round1selector.config;

import com.azure.cosmos.CosmosClient;
import com.azure.cosmos.CosmosClientBuilder;
import org.springframework.ai.chat.ChatClient;
import org.springframework.ai.openai.OpenAiChatModel;
import org.springframework.ai.openai.api.OpenAiApi;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.concurrent.Executor;

@Configuration
@EnableAsync
public class ApplicationConfig {

    @Value("${spring.ai.openai.api-key}")
    private String openaiApiKey;

    @Value("${azure.cosmos.uri}")
    private String cosmosUri;

    @Value("${azure.cosmos.key}")
    private String cosmosKey;

    @Bean
    public ChatClient chatClient() {
        var openAiApi = new OpenAiApi(openaiApiKey);
        var chatModel = new OpenAiChatModel(openAiApi);
        return ChatClient.builder(chatModel).build();
    }

    @Bean
    public CosmosClient cosmosClient() {
        return new CosmosClientBuilder()
                .endpoint(cosmosUri)
                .key(cosmosKey)
                .buildClient();
    }

    @Bean
    public WebClient.Builder webClientBuilder() {
        return WebClient.builder();
    }

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(8);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("PlayerAnalysis-");
        executor.initialize();
        return executor;
    }
}
