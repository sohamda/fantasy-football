import base64
from pathlib import Path
from typing import List, Generator

def encode_image_to_base64(image_path: Path) -> str:
    """
    Encode image file to base64 string
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string of the image
    """
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def get_image_files_from_directory(base_dir: Path, pattern: str = '**/*.jpeg') -> Generator[Path, None, None]:
    """
    Get all image files from a directory
    
    Args:
        base_dir: Base directory to search
        pattern: File pattern to match (default: **/*.jpeg)
        
    Yields:
        Path objects for each matching image file
    """
    if not base_dir.exists():
        raise FileNotFoundError(f"Directory does not exist: {base_dir}")
    
    for img_file in base_dir.glob(pattern):
        if img_file.is_file():
            yield img_file

def validate_image_file(image_path: Path) -> bool:
    """
    Validate that the image file exists and is readable
    
    Args:
        image_path: Path to the image file
        
    Returns:
        True if file is valid, False otherwise
    """
    try:
        return image_path.exists() and image_path.is_file() and image_path.stat().st_size > 0
    except Exception:
        return False

def get_image_data_url(image_path: Path, mime_type: str = "image/jpeg") -> str:
    """
    Get data URL for an image
    
    Args:
        image_path: Path to the image file
        mime_type: MIME type of the image
        
    Returns:
        Data URL string
    """
    image_b64 = encode_image_to_base64(image_path)
    return f"data:{mime_type};base64,{image_b64}"
