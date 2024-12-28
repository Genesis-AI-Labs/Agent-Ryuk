import arxiv
from datetime import datetime
from ..models.research_item import ResearchItem
from typing import List
import logging

logger = logging.getLogger(__name__)

class ArxivCollector:
    def __init__(self):
        self.categories = [
            'cs.AI',    # Artificial Intelligence
            'cs.LG',    # Machine Learning
            'cs.CL',    # Computation and Language
            'cs.CV',    # Computer Vision
            'stat.ML'   # Statistics - Machine Learning
        ]

    async def collect(self) -> List[ResearchItem]:
        """Collect papers from arXiv"""
        try:
            # Create query string for categories
            category_query = ' OR '.join(f'cat:{cat}' for cat in self.categories)
            
            # Search papers
            search = arxiv.Search(
                query=category_query,
                max_results=100,  # Adjust as needed
                sort_by=arxiv.SortCriterion.SubmittedDate
            )

            papers = []
            for result in search.results():
                try:
                    # Categories are strings in the new version of arxiv package
                    categories = result.categories if isinstance(result.categories, list) else [result.categories]
                    
                    paper = ResearchItem(
                        id=f"arxiv_{result.entry_id.split('/')[-1]}",
                        title=result.title,
                        authors=[author.name for author in result.authors],
                        abstract=result.summary,
                        url=result.entry_id,
                        published_date=result.published,
                        source="arxiv",
                        tags=categories  # Using categories directly as tags
                    )
                    papers.append(paper)
                    logger.info(f"Processed arXiv paper: {paper.id}")
                except Exception as e:
                    logger.error(f"Error processing arXiv paper {result.entry_id}: {str(e)}")
                    continue

            logger.info(f"Collected {len(papers)} papers from arXiv")
            return papers

        except Exception as e:
            logger.error(f"Error collecting from arXiv: {str(e)}")
            return []