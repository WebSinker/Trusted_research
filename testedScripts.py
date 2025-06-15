#!/usr/bin/env python3
"""
Test script for trusted sources research
"""

from trusted_sources_researcher import TrustedSourcesResearcher

def test_individual_sources():
    """Test each source individually"""
    
    researcher = TrustedSourcesResearcher(model_name="mistral:7b-instruct-q4_0")
    query = "artificial intelligence"
    
    print("🧪 Testing Individual Sources")
    print("="*50)
    
    # Test arXiv
    print("\n📚 Testing arXiv...")
    arxiv_results = researcher.search_arxiv(query, 2)
    for result in arxiv_results:
        print(f"   ✅ {result['title'][:50]}...")
    
    # Test Wikipedia
    print("\n📖 Testing Wikipedia...")
    wiki_results = researcher.search_wikipedia(query)
    for result in wiki_results:
        print(f"   ✅ {result['title'][:50]}...")
    
    # Test Semantic Scholar
    print("\n🎓 Testing Semantic Scholar...")
    scholar_results = researcher.search_semantic_scholar(query, 2)
    for result in scholar_results:
        print(f"   ✅ {result['title'][:50]}...")
    
    # Test GitHub
    print("\n💻 Testing GitHub...")
    github_results = researcher.search_github(query, 2)
    for result in github_results:
        print(f"   ✅ {result['title'][:50]}...")
    
    # Test Reddit
    print("\n💬 Testing Reddit...")
    reddit_results = researcher.search_reddit(query, 2)
    for result in reddit_results:
        print(f"   ✅ {result['title'][:50]}...")

def test_full_research():
    """Test complete research workflow"""
    
    researcher = TrustedSourcesResearcher(model_name="tinyllama")
    
    print("\n🚀 Testing Full Research Workflow")
    print("="*50)
    
    # Test with academic focus
    print("\n📚 Academic Research Test:")
    academic_report = researcher.conduct_research(
        query="machine learning neural networks",
        categories=['academic'],
        max_sources_per_category=2
    )
    
    if academic_report:
        print("✅ Academic research successful!")
        lines = academic_report.split('\n')
        print(f"   Report length: {len(lines)} lines")
        print(f"   Max line width: {max(len(line) for line in lines)} chars")
    
    # Test with mixed sources
    print("\n🌐 Mixed Sources Test:")
    mixed_report = researcher.conduct_research(
        query="renewable energy trends",
        categories=['academic', 'general'],
        max_sources_per_category=1
    )
    
    if mixed_report:
        print("✅ Mixed research successful!")

def compare_approaches():
    """Compare old vs new approach"""
    
    print("\n📊 APPROACH COMPARISON")
    print("="*50)
    
    print("\n❌ OLD APPROACH (Google scraping):")
    print("   • Gets blocked by bot detection")
    print("   • Hits paywalls and cookie walls")
    print("   • Random quality sources")
    print("   • Low success rate")
    
    print("\n✅ NEW APPROACH (Trusted APIs):")
    print("   • Direct API access")
    print("   • Open access sources")
    print("   • High quality, verified content")
    print("   • No bot detection issues")
    
    print("\n🎯 TRUSTED SOURCES:")
    print("   • arXiv - Open access research papers")
    print("   • Semantic Scholar - Academic abstracts")
    print("   • Wikipedia - Reliable encyclopedia")
    print("   • GitHub - Open source projects")
    print("   • Reddit - Community discussions")

def quick_demo():
    """Quick demonstration"""
    
    researcher = TrustedSourcesResearcher(model_name="mistral:7b-instruct-q4_0")
    
    print("\n⚡ QUICK DEMO")
    print("="*40)
    
    query = input("Enter research topic: ").strip()
    if not query:
        query = "artificial intelligence"
    
    print(f"\n🔍 Researching: {query}")
    
    report = researcher.conduct_research(
        query=query,
        categories=['academic', 'general'],
        max_sources_per_category=1
    )
    
    if report:
        print("\n📄 REPORT PREVIEW:")
        print("-" * 40)
        lines = report.split('\n')
        for line in lines[:20]:  # Show first 20 lines
            print(line)
        
        if len(lines) > 20:
            print("... (truncated)")
        
        print(f"\n📊 Report stats:")
        print(f"   • Total lines: {len(lines)}")
        print(f"   • Max line width: {max(len(line) for line in lines)}")
        print(f"   • Files saved with timestamp")

if __name__ == "__main__":
    print("🔬 TRUSTED SOURCES RESEARCH TESTER")
    print("="*60)
    
    print("\nWhat would you like to test?")
    print("1. Individual sources")
    print("2. Full research workflow")
    print("3. Compare approaches")
    print("4. Quick demo")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        test_individual_sources()
    elif choice == "2":
        test_full_research()
    elif choice == "3":
        compare_approaches()
    elif choice == "4":
        quick_demo()
    else:
        print("Invalid choice, running quick demo...")
        quick_demo()
    
    print("\n✅ Testing completed!")