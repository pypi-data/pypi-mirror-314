# src/quill/generator.py
import tempfile
import shutil
from pathlib import Path
from typing import Optional
import os
import traceback
import google.generativeai as genai
from contextlib import nullcontext

from . import logger
from .config import Config
from .utils import run_repopack, read_file, write_file

class ReadmeGenerator:
    """Generator class for creating README files using Repopack and Gemini."""

    def __init__(self, config: Config):
        """Initialize the generator with configuration."""
        self.config = config
        self.setup_gemini()
        
    def setup_gemini(self) -> None:
        """Initialize the Gemini API client."""
        if self.config.gemini_api_key is None:
            raise ValueError("GEMINI_API_KEY is not configured")
            
        logger.debug("Setting up Gemini client...")
        try:
            genai.configure(api_key=self.config.gemini_api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            logger.debug("Gemini client configured successfully")
        except Exception as e:
            logger.error(f"Failed to configure Gemini client: {str(e)}", exc_info=True)
            raise

    def generate_prompt(self, codebase_content: str) -> str:
        """Generate the prompt for Gemini."""
        logger.debug("Generating Gemini prompt...")
        prompt = f"""You are a technical documentation expert. I will provide you with the contents of a codebase, and I need you to generate 
a comprehensive README.md file that will help developers understand and work with this project.

The README should include:
1. Project title and brief description
2. Key features
3. Technologies used
4. Prerequisites
5. Detailed step-by-step installation guide
6. Usage examples
7. Configuration (if applicable)
8. Project structure explanation
9. Contributing guidelines (if found in the codebase)
10. License information (if found in the codebase)

Important guidelines:
- Be specific and detailed in the installation steps
- Include any environment variables that need to be set
- List all dependencies that need to be installed
- If there are scripts in package.json or requirements.txt, explain their purposes
- If there are configuration files, explain their options
- Keep the tone professional but friendly
- Use proper markdown formatting
- Include usage examples for key features
- If the project has a CLI, include command examples
- Explain any error messages users might encounter

Here is the codebase content:

{codebase_content}

Please generate a comprehensive README.md based on this information."""
        logger.debug("Prompt generated successfully")
        return prompt

    def generate_readme(self, codebase_content: str) -> str:  # Remove async here
        """Generate README content using Gemini."""
        logger.debug("Generating README content with Gemini...")
        try:
            prompt = self.generate_prompt(codebase_content)
            logger.debug("Sending prompt to Gemini...")
            response = self.model.generate_content(prompt)  # Remove await here
            logger.debug("README content generated successfully")
            return response.text
        except Exception as e:
            error_msg = f"Failed to generate README: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise RuntimeError(error_msg) from e

    async def process_directory(self, 
                            directory: str, 
                            output_file: Optional[str] = None,
                            readme_file: Optional[str] = None,
                            keep_packed: bool = False,
                            temp_dir: Optional[str] = None) -> None:
        """Process a directory to generate README."""
        try:
            directory_path = Path(directory).resolve()
            output_file = output_file or self.config.default_output
            readme_file = readme_file or self.config.default_readme
            
            logger.debug(f"Processing directory: {directory_path}")
            logger.debug(f"Output file: {output_file}")
            logger.debug(f"README file: {readme_file}")
            logger.debug(f"Keep packed: {keep_packed}")
            logger.debug(f"Using temp directory: {temp_dir or 'auto-generated'}")
            
            if not directory_path.is_dir():
                raise ValueError(f"Directory not found: {directory_path}")

            with logger.get_progress() as progress:
                # Use provided temp directory or create a new one
                temp_context = (
                    tempfile.TemporaryDirectory() if temp_dir is None 
                    else nullcontext(temp_dir)
                )
                
                with temp_context as temp_path:
                    try:
                        # Run Repopack
                        task_id = progress.add_task(
                            "Packing codebase with Repopack...",
                            total=None
                        )
                        output_path = Path(temp_path) / output_file
                        run_repopack(directory_path, output_path)
                        logger.debug(f"Repopack output saved to: {output_path}")
                        progress.remove_task(task_id)

                        # Read packed content
                        task_id = progress.add_task(
                            "Reading packed content...",
                            total=None
                        )
                        codebase_content = read_file(output_path)
                        logger.debug(f"Read {len(codebase_content)} characters from packed file")
                        progress.remove_task(task_id)

                        # Generate README
                        task_id = progress.add_task(
                            "Generating README with Gemini...",
                            total=None
                        )
                        readme_content = self.generate_readme(codebase_content)  # Remove await here
                        logger.debug(f"Generated README content ({len(readme_content)} characters)")
                        progress.remove_task(task_id)

                        # Write README
                        task_id = progress.add_task(
                            "Writing README file...",
                            total=None
                        )
                        readme_path = directory_path / readme_file
                        write_file(readme_path, readme_content)
                        logger.debug(f"Wrote README to: {readme_path}")
                        progress.remove_task(task_id)

                        # Copy packed file if requested
                        if keep_packed:
                            kept_output = directory_path / output_file
                            shutil.copy2(output_path, kept_output)
                            logger.success(f"Packed codebase saved at: {kept_output}")

                        logger.success(f"Successfully generated README at: {readme_path}")

                    except Exception as e:
                        error_msg = f"Failed to process directory: {str(e)}"
                        logger.error(error_msg, exc_info=True)
                        raise RuntimeError(error_msg) from e

        except Exception as e:
            if logger.is_verbose():
                logger.error(f"Stack trace:", exc_info=True)
            raise