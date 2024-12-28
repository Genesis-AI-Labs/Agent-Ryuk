# AI Research Bot

A Python-based automated bot that collects the latest AI research papers and trends. Currently focused on collecting research paper data from multiple sources (arXiv and Papers With Code) and storing it efficiently. The bot will analyze and post trending AI research on Twitter.

## Current Features

- Automatic paper collection from arXiv and Papers With Code
- Local SQLite database storage
- Asynchronous data fetching
- Error handling and logging
- Data deduplication
- Efficient schema for research papers

## Detailed Setup Guide

### Prerequisites

- Python 3.8 or higher
  ```bash
  # Check your Python version
  python3 --version  # Should show 3.8 or higher
  ```
- SQLite3 (comes with Python)
  ```bash
  # Verify SQLite installation
  sqlite3 --version
  ```

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone [repository-url]
   cd ai_research_bot
   ```

2. **Create and activate virtual environment**

   ```bash
   # Create virtual environment
   python3 -m venv venv

   # Activate it:
   # On Mac/Linux:
   source venv/bin/activate
   # On Windows:
   .\venv\Scripts\activate

   # You should see (venv) in your terminal prompt
   ```

3. **Install dependencies**

   ```bash
   # Make sure you're in the project root and venv is activated
   pip install -r requirements.txt
   ```

4. **Set up environment**

   ```bash
   # Create .env file and add:
   DATABASE_URL=sqlite:///data/research.db
   ```

5. **Create database directory**

   ```bash
   # Create data directory for SQLite database
   mkdir -p data

   # Database file (research.db) will be created automatically
   # when you first run the collector
   ```

### Running the Bot

1. **Collect papers**

   ```bash
   # Make sure your virtual environment is activated
   python -m src.collectors
   ```

2. **View collected data using SQLite**

   ```bash
   # Access the database
   sqlite3 data/research.db

   # Inside SQLite:
   # Make output readable
   .mode column
   .headers on

   # View all papers
   SELECT * FROM research_items;

   # Count papers by source
   SELECT source, COUNT(*) FROM research_items GROUP BY source;

   # Exit SQLite
   .quit
   ```

### Database Note

The `data/research.db` file is not included in the repository and will be created locally when you first run the collector. This ensures:

- Each user has their own clean database
- No conflicts with shared database files
- Fresh data collection for each setup

If you need to reset your database:

```bash
# Remove existing database
rm data/research.db

# Run collector again to create fresh database
python -m src.collectors
```

### Troubleshooting

1. **No such module found**

   ```bash
   # Make sure you're in project root
   # Make sure venv is activated
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

2. **Database issues**

   ```bash
   # Make sure data directory exists
   mkdir -p data

   # Reset database
   sqlite3 data/research.db
   sqlite> DROP TABLE IF EXISTS research_items;
   sqlite> VACUUM;
   sqlite> .quit

   # Run collector again
   python -m src.collectors
   ```

3. **Virtual environment issues**
   ```bash
   # Deactivate and reactivate
   deactivate
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   ```

### Next Steps

1. **Processing Layer**

   - [ ] Implement text extraction from papers
   - [ ] Add content analysis system
   - [ ] Develop trend detection algorithm
   - [ ] Create content summarization using AI models

2. **Decision Layer**

   - [ ] Build relevance scoring system
   - [ ] Implement intelligent content selection
   - [ ] Create optimal posting schedule algorithm
   - [ ] Add agentic decision-making capabilities

3. **Publishing Layer**
   - [ ] Set up Twitter API integration
   - [ ] Implement tweet composition system
   - [ ] Add media generation for tweets
   - [ ] Create automated posting mechanism

## License

MIT
