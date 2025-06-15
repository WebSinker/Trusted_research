# Trusted Sources Research Tool 🔬

An intelligent research tool that automates the collection and analysis of information from trusted academic and general sources using direct API access. This tool helps avoid common web scraping issues while ensuring high-quality, reliable research results.

## Features 🚀

### Multiple Source Categories 📚

#### Academic Sources
- **arXiv** - Open access research papers
- **PubMed Central** - Medical research papers
- **Semantic Scholar** - Academic papers with abstracts

#### News Sources
- **Wikipedia** - Encyclopedia articles
- **Reuters** - Technology news
- **BBC** - Technology news

#### Tech Sources
- **GitHub** - Open source repositories
- **Stack Overflow** - Programming Q&A

#### General Sources
- **Reddit** - Community discussions

### AI-Powered Analysis 🤖
- Utilizes multiple AI models for content analysis:
  - TinyLlama
  - Phi
  - Mistral
- Automatic fallback mechanism for model reliability
- Generates concise summaries and key insights

### Smart Output Generation 📊
- Structured research reports
- Source type breakdown
- Key findings summary
- Detailed content analysis
- JSON data export for further processing

## Installation 💻

1. Clone the repository
2. Install required dependencies:
```powershell
pip install requests beautifulsoup4 ollama
```

## Usage 🛠️

### Basic Usage
```python
from trusted_sources_researcher import TrustedSourcesResearcher

# Initialize the researcher
researcher = TrustedSourcesResearcher(model_name="mistral:7b-instruct-q4_0")

# Conduct research
report = researcher.conduct_research(
    query="your research topic",
    categories=['academic', 'general'],
    max_sources_per_category=2
)
```

### Testing Interface
Run the test script to explore different functionalities:
```powershell
python testedScripts.py
```

Available test options:
1. Test individual sources
2. Test full research workflow
3. Compare approaches
4. Quick demo

## Key Benefits 💡

### Improved Reliability
- Direct API access to trusted sources
- No bot detection issues
- Avoids paywalls and cookie walls
- High-quality, verified content

### Efficient Processing
- Parallel source querying
- Automatic content analysis
- Structured data output
- Clean, formatted reports

## Output Files 📁

The tool generates two types of files for each research query:

1. **Research Report** (`trusted_research_[timestamp].txt`)
   - Formatted research findings
   - Executive summary
   - Source breakdown
   - Key insights
   - Detailed source information

2. **Raw Data** (`trusted_data_[timestamp].json`)
   - Complete research data
   - Source content
   - AI analysis
   - Metadata

## Requirements 📋

- Python 3.x
- Internet connection
- Ollama (for AI analysis)
- API access to source platforms

## Best Practices 🎯

1. Use specific search queries for better results
2. Combine multiple source categories for comprehensive research
3. Adjust max_sources_per_category based on depth needed
4. Consider API rate limits for extensive research

## Notes ⚠️

- Respect API rate limits of different platforms
- Some sources may require API keys for extended access
- Internet connection quality affects research speed
- AI analysis quality depends on the selected model

## Contributing 🤝

Feel free to:
- Report issues
- Suggest new features
- Add new trusted sources
- Improve AI analysis

## License 📄

MIT License - Feel free to use and modify for your needs.
