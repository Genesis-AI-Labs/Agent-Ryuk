import aiohttp
from datetime import datetime
from ..models.research_item import ResearchItem
from typing import List
import logging

logger = logging.getLogger(__name__)

class PapersWithCodeCollector:
    def __init__(self):
        self.base_url = "https://paperswithcode.com/api/v1"
        self.papers_endpoint = f"{self.base_url}/papers/"

    async def collect(self) -> List[ResearchItem]:
        """Collect papers from Papers With Code"""
        try:
            async with aiohttp.ClientSession() as session:
                papers = []
                
                # Get papers from the API
                async with session.get(
                    self.papers_endpoint,
                    params={
                        'ordering': '-published',
                        'topics': 'artificial-intelligence,machine-learning,deep-learning'
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for paper in data.get('results', []):
                            try:
                                # Handle potential None published date
                                if paper.get('published'):
                                    published_date = datetime.fromisoformat(
                                        paper['published'].replace('Z', '+00:00')
                                    )
                                else:
                                    published_date = datetime.utcnow()  # Use current time as fallback
                                
                                # Handle potential missing fields with defaults
                                item = ResearchItem(
                                    id=f"pwc_{paper.get('id', 'unknown')}",
                                    title=paper.get('title', 'Untitled'),
                                    authors=paper.get('authors', []),
                                    abstract=paper.get('abstract', ''),
                                    url=paper.get('url', ''),
                                    published_date=published_date,
                                    source="papers_with_code",
                                    tags=paper.get('topics', []),
                                    citation_count=paper.get('citations')
                                )
                                papers.append(item)
                                logger.info(f"Processed Papers With Code paper: {item.id}")
                            except Exception as e:
                                paper_id = paper.get('id', 'unknown')
                                logger.error(f"Error processing paper {paper_id}: {str(e)}")
                                continue
                
                logger.info(f"Collected {len(papers)} papers from Papers With Code")
                return papers

        except Exception as e:
            logger.error(f"Error collecting from Papers With Code: {str(e)}")
            return []

    async def _get_paper_implementations(self, paper_id: str) -> List[str]:
        """Get implementation URLs for a paper"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.papers_endpoint}{paper_id}/repositories/"
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [repo['url'] for repo in data.get('results', [])]
        except Exception:
            return []