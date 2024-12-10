import argparse
import asyncio
from typing import Optional
import sys

from . import __version__
from .config import Config
from .generator import ReadmeGenerator
from . import logger

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive README files using Repopack and Gemini",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to process"
    )
    parser.add_argument(
        "-o", "--output",
        help="Specify the Repopack output file name",
        default=Config.default_output
    )
    parser.add_argument(
        "-r", "--readme",
        help="Specify the README output file name",
        default=Config.default_readme
    )
    parser.add_argument(
        "-k", "--keep-packed",
        action="store_true",
        help="Keep the packed codebase file after generation"
    )
    parser.add_argument(
        "--temp-dir",
        help="Specify a custom temporary directory for processing",
        default=None
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"readme-generator-cli {__version__}"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    return parser.parse_args()

async def async_main() -> None:
    """Asynchronous main entry point for the CLI."""
    try:
        args = parse_args()
        
        if args.verbose:
            logger.set_verbose(True)
            logger.debug("Verbose logging enabled")
            
        logger.debug(f"Arguments: {args}")
        
        try:
            config = Config.from_env()
            logger.debug("Configuration loaded successfully")
        except ValueError as e:
            logger.error(str(e))
            sys.exit(1)
            
        logger.debug("Initializing generator...")
        generator = ReadmeGenerator(config)

        logger.debug(f"Processing directory: {args.directory}")
        await generator.process_directory(  # Add 'await' here!
            args.directory,
            args.output,
            args.readme,
            args.keep_packed,
            args.temp_dir
        )
        
    except KeyboardInterrupt:
        logger.error("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(str(e))
        if logger.is_verbose():
            logger.error("Traceback:", exc_info=True)
        sys.exit(1)

def main() -> None:
    """Synchronous entry point for the CLI."""
    try:
        if sys.platform == 'win32':
            # Set up proper async event loop for Windows
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        asyncio.run(async_main())
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        if logger.is_verbose():
            logger.error("Traceback:", exc_info=True)
        sys.exit(1)