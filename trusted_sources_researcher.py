import requests
import time
import json
from datetime import datetime
from bs4 import BeautifulSoup
import ollama
import urllib.parse
import re

class TrustedSourcesResearcher:
    def __init__(self, model_name="tinyllama"):
        self.model_name = model_name
        
        # Trusted, accessible sources by category
        self.trusted_sources = {
            "academic": {
                "arxiv": {
                    "name": "arXiv",
                    "search_url": "http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5",
                    "type": "xml_api",
                    "description": "Open access research papers"
                },
                "pubmed": {
                    "name": "PubMed Central (Open Access)",
                    "search_url": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={query}&retmax=5&retmode=json",
                    "type": "ncbi_api",
                    "description": "Medical research papers"
                },
                "semantic_scholar": {
                    "name": "Semantic Scholar",
                    "search_url": "https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=5&fields=title,url,abstract,openAccessPdf",
                    "type": "json_api",
                    "description": "Academic papers with abstracts"
                }
            },
            "news": {
                "wikipedia": {
                    "name": "Wikipedia",
                    "search_url": "https://en.wikipedia.org/api/rest_v1/page/summary/{query}",
                    "type": "wiki_api",
                    "description": "Encyclopedia articles"
                },
                "reuters": {
                    "name": "Reuters RSS",
                    "search_url": "https://www.reuters.com/arc/outboundfeeds/rss/category/technology/?outputType=xml",
                    "type": "rss_feed",
                    "description": "Technology news"
                },
                "bbc": {
                    "name": "BBC RSS Technology",
                    "search_url": "http://feeds.bbci.co.uk/news/technology/rss.xml",
                    "type": "rss_feed", 
                    "description": "BBC Technology news"
                }
            },
            "tech": {
                "github": {
                    "name": "GitHub Repositories",
                    "search_url": "https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=5",
                    "type": "github_api",
                    "description": "Open source projects"
                },
                "stackoverflow": {
                    "name": "Stack Overflow",
                    "search_url": "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={query}&site=stackoverflow",
                    "type": "stack_api",
                    "description": "Programming Q&A"
                }
            },
            "general": {
                "reddit": {
                    "name": "Reddit",
                    "search_url": "https://www.reddit.com/search.json?q={query}&sort=relevance&limit=5",
                    "type": "reddit_api",
                    "description": "Community discussions"
                }
            }
        }
    
    def search_arxiv(self, query, max_results=3):
        """Search arXiv for academic papers"""
        results = []
        try:
            import xml.etree.ElementTree as ET
            
            search_url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&start=0&max_results={max_results}"
            
            print(f"🔍 Searching arXiv for: {query}")
            response = requests.get(search_url, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                    title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
                    summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
                    link = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
                    
                    # Clean up the summary
                    summary = re.sub(r'\s+', ' ', summary)
                    
                    results.append({
                        'title': title,
                        'url': link,
                        'content': summary,
                        'source': 'arXiv',
                        'type': 'academic_paper'
                    })
                    
                print(f"✅ Found {len(results)} arXiv papers")
                
        except Exception as e:
            print(f"❌ Error searching arXiv: {e}")
        
        return results
    
    def search_wikipedia(self, query):
        """Search Wikipedia for articles"""
        results = []
        try:
            # First, search for articles
            search_url = f"https://en.wikipedia.org/api/rest_v1/page/search/{urllib.parse.quote(query)}"
            
            print(f"🔍 Searching Wikipedia for: {query}")
            response = requests.get(search_url, timeout=10)
            
            if response.status_code == 200:
                search_data = response.json()
                
                # Get details for top results
                for item in search_data.get('pages', [])[:3]:
                    page_title = item['title']
                    
                    # Get page summary
                    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(page_title)}"
                    summary_response = requests.get(summary_url, timeout=10)
                    
                    if summary_response.status_code == 200:
                        summary_data = summary_response.json()
                        
                        results.append({
                            'title': summary_data.get('title', page_title),
                            'url': summary_data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                            'content': summary_data.get('extract', ''),
                            'source': 'Wikipedia',
                            'type': 'encyclopedia'
                        })
                
                print(f"✅ Found {len(results)} Wikipedia articles")
                
        except Exception as e:
            print(f"❌ Error searching Wikipedia: {e}")
        
        return results
    
    def search_semantic_scholar(self, query, max_results=3):
        """Search Semantic Scholar for academic papers"""
        results = []
        try:
            search_url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(query)}&limit={max_results}&fields=title,url,abstract,openAccessPdf,authors"
            
            print(f"🔍 Searching Semantic Scholar for: {query}")
            response = requests.get(search_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for paper in data.get('data', []):
                    if paper.get('abstract'):  # Only include papers with abstracts
                        results.append({
                            'title': paper.get('title', 'No title'),
                            'url': paper.get('url', ''),
                            'content': paper.get('abstract', ''),
                            'source': 'Semantic Scholar',
                            'type': 'academic_paper',
                            'authors': [author.get('name', '') for author in paper.get('authors', [])]
                        })
                
                print(f"✅ Found {len(results)} Semantic Scholar papers")
                
        except Exception as e:
            print(f"❌ Error searching Semantic Scholar: {e}")
        
        return results
    
    def search_github(self, query, max_results=3):
        """Search GitHub for relevant repositories"""
        results = []
        try:
            search_url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc&per_page={max_results}"
            
            print(f"🔍 Searching GitHub for: {query}")
            response = requests.get(search_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for repo in data.get('items', []):
                    description = repo.get('description', '')
                    readme_content = self.get_github_readme(repo.get('full_name', ''))
                    
                    content = f"{description}\n\n{readme_content}" if readme_content else description
                    
                    results.append({
                        'title': f"{repo.get('name', 'No name')} - {repo.get('full_name', '')}",
                        'url': repo.get('html_url', ''),
                        'content': content[:1000],  # Limit content length
                        'source': 'GitHub',
                        'type': 'repository',
                        'stars': repo.get('stargazers_count', 0)
                    })
                
                print(f"✅ Found {len(results)} GitHub repositories")
                
        except Exception as e:
            print(f"❌ Error searching GitHub: {e}")
        
        return results
    
    def get_github_readme(self, repo_full_name):
        """Get README content from GitHub repository"""
        try:
            readme_url = f"https://api.github.com/repos/{repo_full_name}/readme"
            response = requests.get(readme_url, timeout=5)
            
            if response.status_code == 200:
                readme_data = response.json()
                
                # Decode base64 content
                import base64
                content = base64.b64decode(readme_data['content']).decode('utf-8')
                
                # Remove markdown formatting for cleaner text
                content = re.sub(r'[#*`\[\]()]', '', content)
                content = re.sub(r'\n+', '\n', content)
                
                return content[:500]  # First 500 chars
                
        except:
            pass
        
        return ""
    
    def search_reddit(self, query, max_results=3):
        """Search Reddit for discussions"""
        results = []
        try:
            search_url = f"https://www.reddit.com/search.json?q={urllib.parse.quote(query)}&sort=relevance&limit={max_results}"
            
            headers = {'User-Agent': 'ResearchBot/1.0'}
            
            print(f"🔍 Searching Reddit for: {query}")
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for post in data.get('data', {}).get('children', []):
                    post_data = post.get('data', {})
                    
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')
                    url = f"https://reddit.com{post_data.get('permalink', '')}"
                    
                    # Combine title and content
                    content = f"{title}\n\n{selftext}" if selftext else title
                    
                    if len(content) > 50:  # Only include substantial posts
                        results.append({
                            'title': title,
                            'url': url,
                            'content': content[:800],  # Limit content
                            'source': 'Reddit',
                            'type': 'discussion',
                            'subreddit': post_data.get('subreddit', '')
                        })
                
                print(f"✅ Found {len(results)} Reddit discussions")
                
        except Exception as e:
            print(f"❌ Error searching Reddit: {e}")
        
        return results
    
    def conduct_research(self, query, categories=['academic', 'general'], max_sources_per_category=2):
        """
        Conduct research using trusted sources
        
        Args:
            query (str): Research query
            categories (list): Categories to search in
            max_sources_per_category (int): Max sources per category
        """
        print(f"🚀 Starting trusted source research for: {query}")
        print("=" * 60)
        
        all_results = []
        
        # Search each category
        for category in categories:
            if category == 'academic':
                print(f"\n📚 Searching Academic Sources...")
                
                # arXiv
                arxiv_results = self.search_arxiv(query, max_sources_per_category)
                all_results.extend(arxiv_results)
                
                # Semantic Scholar
                scholar_results = self.search_semantic_scholar(query, max_sources_per_category)
                all_results.extend(scholar_results)
                
            elif category == 'general':
                print(f"\n🌐 Searching General Sources...")
                
                # Wikipedia
                wiki_results = self.search_wikipedia(query)
                all_results.extend(wiki_results)
                
                # Reddit
                reddit_results = self.search_reddit(query, max_sources_per_category)
                all_results.extend(reddit_results)
                
            elif category == 'tech':
                print(f"\n💻 Searching Tech Sources...")
                
                # GitHub
                github_results = self.search_github(query, max_sources_per_category)
                all_results.extend(github_results)
        
        # Analyze results with AI
        print(f"\n🤖 Analyzing {len(all_results)} sources...")
        analyzed_results = []
        
        for result in all_results:
            if result.get('content') and len(result['content']) > 100:
                analysis = self.analyze_with_ollama(result['content'], query)
                
                analyzed_results.append({
                    'title': result['title'],
                    'url': result['url'],
                    'source': result['source'],
                    'type': result.get('type', 'unknown'),
                    'content': result['content'][:500] + "..." if len(result['content']) > 500 else result['content'],
                    'analysis': analysis
                })
                
                print(f"✅ Analyzed: {result['title'][:50]}...")
        
        # Generate final report
        if analyzed_results:
            final_report = self.create_trusted_sources_report(query, analyzed_results)
            self.save_report(query, final_report, analyzed_results)
            
            print(f"\n✅ Research completed! Found {len(analyzed_results)} quality sources.")
            return final_report
        else:
            print("❌ No suitable sources found.")
            return None
    
    def analyze_with_ollama(self, content, query):
        """Analyze content using Ollama with fallback models"""
        models_to_try = ["tinyllama", "phi", "mistral:7b-instruct-q4_0"]
        
        prompt = f"""
        Analyze this content for the research query: "{query}"
        
        Content: {content[:1500]}
        
        Provide key insights, facts, and how this relates to the query.
        Keep it concise and focused.
        """
        
        for model in models_to_try:
            try:
                response = ollama.chat(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response['message']['content']
            except Exception as e:
                if "memory" in str(e).lower():
                    continue
                else:
                    break
        
        return f"Content summary: {content[:300]}..."
    
    def create_trusted_sources_report(self, query, results):
        """Create a structured report from trusted sources"""
        from datetime import datetime
        
        report = f"""
{'='*80}
TRUSTED SOURCES RESEARCH REPORT
{'='*80}

Query: {query}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Sources: {len(results)} trusted sources

{'='*80}

EXECUTIVE SUMMARY
-----------------
This report analyzes {len(results)} sources from trusted platforms including
academic databases, Wikipedia, and verified repositories to provide reliable
information about {query}.

SOURCE BREAKDOWN
----------------
"""
        
        # Count sources by type
        source_counts = {}
        for result in results:
            source = result.get('source', 'Unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        for source, count in source_counts.items():
            report += f"• {source}: {count} sources\n"
        
        report += "\n"
        
        # Key findings from each source
        report += """
KEY FINDINGS
------------
"""
        
        for i, result in enumerate(results, 1):
            title = result.get('title', f'Source {i}')
            source = result.get('source', 'Unknown')
            analysis = result.get('analysis', 'No analysis available')
            
            # Wrap text properly
            import textwrap
            wrapped_analysis = textwrap.fill(analysis, width=75, initial_indent='', subsequent_indent='   ')
            
            report += f"""
{i}. [{source}] {title}
   {wrapped_analysis}

"""
        
        # Detailed sources
        report += """
DETAILED SOURCES
----------------
"""
        
        for i, result in enumerate(results, 1):
            title = result.get('title', f'Source {i}')
            url = result.get('url', 'No URL')
            source = result.get('source', 'Unknown')
            content = result.get('content', 'No content')
            
            # Format URL for readability
            display_url = url[:60] + "..." if len(url) > 60 else url
            
            import textwrap
            wrapped_content = textwrap.fill(content, width=75, initial_indent='', subsequent_indent='   ')
            
            report += f"""
Source {i}: {title}
Platform: {source}
URL: {display_url}

Content Summary:
{wrapped_content}

"""
        
        report += f"""
{'='*80}
Report generated using trusted, accessible sources
Avoiding paywalls and bot-detection issues
{'='*80}
"""
        
        return report
    
    def save_report(self, query, report, research_data):
        """Save the research report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save text report
        report_filename = f"trusted_research_{timestamp}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save JSON data
        data_filename = f"trusted_data_{timestamp}.json"
        with open(data_filename, 'w', encoding='utf-8') as f:
            json.dump({
                'query': query,
                'timestamp': timestamp,
                'sources': research_data,
                'report': report
            }, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Report saved as: {report_filename}")
        print(f"💾 Data saved as: {data_filename}")

# Usage example
if __name__ == "__main__":
    # Initialize researcher
    researcher = TrustedSourcesResearcher(model_name="tinyllama")
    
    # Test queries
    test_queries = [
        "artificial intelligence healthcare",
        "machine learning algorithms",
        "renewable energy storage",
        "quantum computing applications"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing: {query}")
        print(f"{'='*60}")
        
        # Research using academic and general sources
        report = researcher.conduct_research(
            query=query,
            categories=['academic', 'general'],
            max_sources_per_category=2
        )
        
        if report:
            print("✅ Research completed successfully!")
        else:
            print("❌ Research failed")
        
        # Add delay between queries
        time.sleep(2)