package com.fantasyfootball.playerextraction.image.extraction;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;

import javax.annotation.PostConstruct;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.azure.openai.AzureOpenAiChatModel;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.core.io.InputStreamResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;
import org.springframework.util.MimeTypeUtils;

import com.fantasyfootball.playerextraction.model.Player;

@Service
public class ImageExtractionService {
    
    private static final Logger logger = LoggerFactory.getLogger(ImageExtractionService.class);
    
    private final AzureOpenAiChatModel chatModel;    

    @Value("classpath:prompts/imageExtraction.txt")
	private Resource imageExtractionPromptFile;

    @Value("classpath:prompts/validateImageExtraction.txt")
	private Resource validateImageExtractionPromptFile;

    private String imageExtractionPrompt;
    private String validateImageExtractionPrompt;   

    private ChatClient chatClient;

    public ImageExtractionService(AzureOpenAiChatModel chatModel) {
        this.chatModel = chatModel;
    }

    @PostConstruct
    public void init() throws IOException {
        imageExtractionPrompt = new String(Files.readAllBytes(imageExtractionPromptFile.getFile().toPath()));
        validateImageExtractionPrompt = new String(Files.readAllBytes(validateImageExtractionPromptFile.getFile().toPath()));
        chatClient = ChatClient.builder(chatModel).defaultAdvisors(new TokenUsageAdvisor()).build();
    }
    
    /**
     * Extract player information from an image using Spring AI
    */
    public List<Player> extractPlayerFromImage(File image) throws Exception {
        logger.info("Starting player extraction from image: {}", image.getAbsolutePath());
                 
        List<Player> playerList = null;
        Integer evaluator = 10;
        do {
            playerList = parseImage(image);
            evaluator = validateExtraction(image, playerList);
            logger.info("Extraction evaluation score: {}", evaluator);
            if(evaluator < 7) {
                logger.info("Re-extracting due to low evaluation score");
            }
        } while(evaluator < 7);

        logger.info("Final extracted response: {}", playerList);

        return playerList;
    }

    private List<Player> parseImage(File image) throws FileNotFoundException {
        InputStreamResource imageResource = new InputStreamResource(new FileInputStream(image));
        List<Player> playerList =  chatClient.prompt().user(u -> u
                        .text(imageExtractionPrompt)
                        .media(MimeTypeUtils.IMAGE_JPEG, imageResource))
                    .call()
                    .entity((new ParameterizedTypeReference<List<Player>>() {}));
        return playerList;
    }

    private int validateExtraction(File image, List<Player> jsonExtracted) throws FileNotFoundException   {
        InputStreamResource imageResource = new InputStreamResource(new FileInputStream(image));
        String rawResponse =  chatClient.prompt().user(u -> u
                    .text(validateImageExtractionPrompt)
                    .param("json_extracted", jsonExtracted)
                    .media(MimeTypeUtils.IMAGE_JPEG, imageResource))
                .call().content();
        return Integer.parseInt(rawResponse.trim());
    }
}