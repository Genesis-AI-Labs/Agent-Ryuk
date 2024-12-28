import asyncio
import logging
from typing import List
from ..models.research_item import ResearchItem
from ..database.manager import DatabaseManager
from .arxiv import ArxivCollector
from .papers_with_code import PapersWithCodeCollector

logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self):
        self.db = DatabaseManager()
        self.collectors = [
            ArxivCollector(),
            PapersWithCodeCollector()
        ]

    async def collect_all(self) -> List[ResearchItem]:
        """Collect data from all sources"""
        try:
            # Create tasks for all collectors
            tasks = [collector.collect() for collector in self.collectors]
            
            # Run all collectors concurrently
            results = await asyncio.gather(*tasks)
            
            # Flatten results and store in database
            all_items = []
            for items in results:
                for item in items:
                    try:
                        self.db.add_item(item)
                        all_items.append(item)
                    except Exception as e:
                        logger.error(f"Error storing item {item.id}: {str(e)}")
                        continue

            logger.info(f"Successfully collected {len(all_items)} items from all sources")
            return all_items

        except Exception as e:
            logger.error(f"Error in collect_all: {str(e)}")
            return []

def main():
    """Main entry point for data collection"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create collector and run
    collector = DataCollector()
    asyncio.run(collector.collect_all())

if __name__ == "__main__":
    main()