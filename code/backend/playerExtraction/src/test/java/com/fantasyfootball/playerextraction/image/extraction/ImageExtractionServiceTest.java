package com.fantasyfootball.playerextraction.image.extraction;

import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.io.Resource;

@SpringBootTest
public class ImageExtractionServiceTest {

    private static final Logger logger = LoggerFactory.getLogger(ImageExtractionServiceTest.class);

    @Autowired
    private ImageExtractionService imageExtractionService;

    @Value("classpath:/testdata/screenshot-1.jpeg")
	private Resource testImageResource;

    @Test
    void testExtractPlayerFromImage() {
        
        try {
            var player = imageExtractionService.extractPlayerFromImage(testImageResource.getFile());
            Assertions.assertThat(player != null).isTrue();
            logger.info("Extracted Player: {}", player);
        } catch (Exception e) {
            Assertions.fail("Exception occurred during image extraction test", e);
        }
    }

}
