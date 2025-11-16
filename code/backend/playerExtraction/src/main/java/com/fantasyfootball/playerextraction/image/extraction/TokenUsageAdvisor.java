package com.fantasyfootball.playerextraction.image.extraction;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClientRequest;
import org.springframework.ai.chat.client.ChatClientResponse;
import org.springframework.ai.chat.client.advisor.api.CallAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAdvisorChain;

public class TokenUsageAdvisor implements CallAdvisor{

    private static final Logger logger = LoggerFactory.getLogger(TokenUsageAdvisor.class);

    @Override
    public String getName() {
        return this.getClass().getSimpleName();
    }

    @Override
    public int getOrder() {
        return 0;
    }

    @Override
    public ChatClientResponse adviseCall(ChatClientRequest chatClientRequest, CallAdvisorChain callAdvisorChain) {
        logger.info("TokenUsageAdvisor - Before call");

        ChatClientResponse chatClientResponse = callAdvisorChain.nextCall(chatClientRequest);

		logger.info("TokenUsageAdvisor - After call: {}", chatClientResponse.chatResponse().getMetadata().getUsage().getTotalTokens());

		return chatClientResponse;
    }

}
