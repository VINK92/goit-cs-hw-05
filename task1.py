import os
import shutil
import asyncio
import aiofiles
import logging
from pathlib import Path
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = ArgumentParser(description="Sort files based on their extension.")
parser.add_argument('source', type=str, help='Source folder to read files from.')
parser.add_argument('destination', type=str, help='Destination folder to copy files to.')
args = parser.parse_args()

source_path = Path(args.source)
destination_path = Path(args.destination)


async def read_folder(path: Path):
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            files.append(Path(root) / filename)
    return files


async def copy_file(file: Path, destination: Path):
    try:
        extension = file.suffix.lstrip('.')
        dest_folder = destination / extension
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_file = dest_folder / file.name
        async with aiofiles.open(file, 'rb') as fsrc:
            async with aiofiles.open(dest_file, 'wb') as fdst:
                await fdst.write(await fsrc.read())
        logger.info(f"Copied {file} to {dest_file}")
    except Exception as e:
        logger.error(f"Failed to copy {file}: {e}")


async def main(source: Path, destination: Path):
    try:
        files = await read_folder(source)
        tasks = [copy_file(file, destination) for file in files]
        await asyncio.gather(*tasks)
        logger.info(f"Successfully sorted {len(files)} files.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main(source_path, destination_path))
