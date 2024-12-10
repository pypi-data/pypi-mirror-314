import subprocess
import shutil
from pathlib import Path
from typing import Optional
import os

from . import logger

def run_repopack(directory: Path, output_file: Path) -> None:
    """
    Run Repopack on a directory using the CLI command.
    
    Args:
        directory (Path): The directory to process
        output_file (Path): The output file path for the packed content
        
    Raises:
        RuntimeError: If repopack is not installed or if the command fails
        FileNotFoundError: If the directory doesn't exist
    """
    # Verify repopack is installed
    if not shutil.which('repopack'):
        raise RuntimeError(
            "Repopack CLI not found. Please install it with: pip install repopack"
        )
    
    # Verify directory exists
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    try:
        logger.debug(f"Packing codebase from {directory} to {output_file}")
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Run repopack command
        result = subprocess.run(
            [
                "repopack",
                str(directory),
                "-o",
                str(output_file)
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Verify output file was created
        if not output_file.exists():
            raise RuntimeError(f"Repopack did not generate output file: {output_file}")
            
        logger.success(f"Successfully packed codebase into {output_file}")
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Repopack command failed: {e.stderr}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e
        
    except Exception as e:
        error_msg = f"Failed to run Repopack: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e

def read_file(path: Path) -> str:
    """
    Read and return the contents of a file.
    
    Args:
        path (Path): Path to the file to read
        
    Returns:
        str: The contents of the file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        RuntimeError: If there's an error reading the file
    """
    try:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
            
        logger.debug(f"Reading file: {path}")
        content = path.read_text(encoding='utf-8')
        logger.debug(f"Successfully read {len(content)} characters from {path}")
        return content
        
    except Exception as e:
        error_msg = f"Failed to read file {path}: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e

def write_file(path: Path, content: str) -> None:
    """
    Write content to a file.
    
    Args:
        path (Path): Path where to write the file
        content (str): Content to write to the file
        
    Raises:
        RuntimeError: If there's an error writing the file
    """
    try:
        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.debug(f"Writing {len(content)} characters to {path}")
        path.write_text(content, encoding='utf-8')
        logger.debug(f"Successfully wrote content to {path}")
        
    except Exception as e:
        error_msg = f"Failed to write file {path}: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e