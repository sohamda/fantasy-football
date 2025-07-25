from pathlib import Path
from typing import List
from models.player_models import Player, ProcessingResult
from services.image_extraction_service import ImageExtractionService
from services.validation_service import ValidationService
from services.cosmos_service import CosmosService
from services.bing_service import BingService
from utils.logging_utils import LogAnalyticsLogger
from utils.image_utils import get_image_files_from_directory

class ImageProcessor:
    """Main processor for handling image extraction workflow"""
    
    def __init__(
        self,
        extraction_service: ImageExtractionService,
        validation_service: ValidationService,
        cosmos_service: CosmosService,
        bing_service: BingService,
        logger: LogAnalyticsLogger,
        validation_threshold: int = 8,
        max_retries: int = 3
    ):
        self.extraction_service = extraction_service
        self.validation_service = validation_service
        self.cosmos_service = cosmos_service
        self.bing_service = bing_service
        self.logger = logger
        self.validation_threshold = validation_threshold
        self.max_retries = max_retries
    
    async def process_single_image(
        self,
        image_path: Path,
        extraction_prompt: str,
        validation_prompt: str,
        extraction_schema: dict,
        validation_schema: dict
    ) -> ProcessingResult:
        """
        Process a single image with extraction and validation
        
        Args:
            image_path: Path to the image file
            extraction_prompt: Prompt for extraction
            validation_prompt: Prompt for validation
            extraction_schema: Schema for extraction response
            validation_schema: Schema for validation response
            
        Returns:
            ProcessingResult object
        """
        self.logger.log_info(f"Processing image: {str(image_path)}")
        
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                # Extract player information
                players = self.extraction_service.extract_info_from_image(
                    image_path, extraction_prompt, extraction_schema
                )
                
                if not players:
                    self.logger.log_warning(f"No players extracted from image: {str(image_path)}")
                    return ProcessingResult(
                        success=False,
                        error_message="No players extracted from image"
                    )
                
                # Validate extraction
                validation_result = self.validation_service.validate_image_extraction(
                    players, image_path, validation_prompt, validation_schema
                )
                
                if not validation_result:
                    self.logger.log_warning(f"Validation failed for image: {str(image_path)}")
                    retry_count += 1
                    continue
                
                self.logger.log_info(
                    f"Validation completed with score: {validation_result.score}",
                    image_path=str(image_path),
                    score=validation_result.score
                )
                
                # Check if validation score is acceptable
                if self.validation_service.is_validation_score_acceptable(
                    validation_result.score, self.validation_threshold
                ):
                    self.logger.log_info(f"Validation passed for image: {str(image_path)}")
                    
                    # Validate and enhance players with Bing search
                    validated_players = await self._validate_players_with_bing(players)
                    
                    return ProcessingResult(
                        success=True,
                        players=validated_players,
                        validation_score=validation_result.score
                    )
                else:
                    self.logger.log_warning(
                        f"Validation score too low ({validation_result.score}), retrying...",
                        image_path=str(image_path)
                    )
                    retry_count += 1
                    
            except Exception as e:
                self.logger.log_error(f"Error processing image: {e}", image_path=str(image_path))
                retry_count += 1
        
        return ProcessingResult(
            success=False,
            error_message=f"Failed after {self.max_retries} retries"
        )
    
    async def process_all_images_in_directory(
        self,
        base_dir: Path,
        extraction_prompt: str,
        validation_prompt: str,
        extraction_schema: dict,
        validation_schema: dict,
        store_in_cosmos: bool = False
    ) -> List[Player]:
        """
        Process all images in a directory
        
        Args:
            base_dir: Directory containing images
            extraction_prompt: Prompt for extraction
            validation_prompt: Prompt for validation
            extraction_schema: Schema for extraction response
            validation_schema: Schema for validation response
            store_in_cosmos: Whether to store results in Cosmos DB
            
        Returns:
            List of all successfully extracted players
        """
        self.logger.log_info(f"Starting batch processing in directory: {str(base_dir)}")
        
        all_extracted_players = []
        
        try:
            image_files = list(get_image_files_from_directory(base_dir))
            self.logger.log_info(f"Found {len(image_files)} images to process")
            
            for img_file in image_files:
                result = await self.process_single_image(
                    img_file,
                    extraction_prompt,
                    validation_prompt,
                    extraction_schema,
                    validation_schema
                )
                
                if result.success and result.players:
                    all_extracted_players.extend(result.players)
                    self.logger.log_info(
                        f"Successfully processed {str(img_file)} - extracted {len(result.players)} players"
                    )
                else:
                    self.logger.log_error(
                        f"Failed to process {str(img_file)}: {result.error_message}"
                    )
            
            # Store in Cosmos DB if requested
            if store_in_cosmos and all_extracted_players:
                self._store_players_with_ids(all_extracted_players)
            
            self.logger.log_info(
                f"Batch processing completed. Total players extracted: {len(all_extracted_players)}"
            )
            
        except Exception as e:
            self.logger.log_error(f"Error during batch processing: {e}")
        
        return all_extracted_players
    
    def _store_players_with_ids(self, players: List[Player]) -> None:
        """
        Store players in Cosmos DB with generated IDs
        
        Args:
            players: List of Player objects to store
        """
        for idx, player in enumerate(players):
            if not player.id:
                player.id = self.cosmos_service._generate_player_id(player, idx)
        
        stored_count = self.cosmos_service.store_players_batch(players)
        self.logger.log_info(f"Stored {stored_count}/{len(players)} players in Cosmos DB")
    
    async def _validate_players_with_bing(self, players: List[Player]) -> List[Player]:
        """
        Validate and enhance players using Bing search
        
        Args:
            players: List of Player objects to validate
            
        Returns:
            List of validated Player objects
        """
        try:
            self.logger.log_info(f"Starting Bing validation for {len(players)} players")
            
            # Option 1: Use batch validation (finalize_extraction_with_bing)
            validated_players = await self.bing_service.finalize_extraction_with_bing(players)
            
            # Option 2: Individual validation (uncomment if preferred)
            # validated_players = []
            # for player in players:
            #     validated_player = await self.bing_service.validate_individual_player(player)
            #     validated_players.append(validated_player)
            
            self.logger.log_info(f"Bing validation completed for {len(validated_players)} players")
            return validated_players
            
        except Exception as e:
            self.logger.log_error(f"Bing validation failed: {e}")
            # Return original players if Bing validation fails
            return players
