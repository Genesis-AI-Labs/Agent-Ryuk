import asyncio
from . import DataCollector
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        collector = DataCollector()
        items = await collector.collect_all()
        logger.info(f"Successfully collected {len(items)} items")
    except Exception as e:
        logger.error(f"Error during collection: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())