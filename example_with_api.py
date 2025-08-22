"""
Example of how to use the Multi-Agent Research System with a real API key
"""

import os
from dotenv import load_dotenv
from agents.query_processor import QueryProcessor
from agents.data_collector import DataCollector
from agents.content_analyzer import ContentAnalyzer
from agents.report_generator import ReportGenerator

# Load environment variables
load_dotenv()

def run_research_with_api(original_query: str):
    """
    Run research with full API functionality
    """
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_actual_groq_api_key_here":
        print("Error: GROQ_API_KEY not found in environment variables.")
        print("Please set your Groq API key in a .env file to use full functionality.")
        return None
    
    print(f"Starting research on: {original_query}")
    
    # Initialize agents
    query_processor = QueryProcessor()
    data_collector = DataCollector()
    content_analyzer = ContentAnalyzer()
    report_generator = ReportGenerator()
    
    # Step 1: Decompose query
    print("Step 1: Processing query...")
    sub_queries = query_processor.decompose_query(original_query)
    print(f"Generated sub-queries: {sub_queries}")
    
    # Step 2: Collect data
    print("Step 2: Collecting data...")
    all_data = []
    for sub_query in sub_queries:
        print(f"Researching: {sub_query}")
        data = data_collector.search_and_scrape(sub_query)
        all_data.extend(data)
    
    print(f"Collected {len(all_data)} sources")
    
    # Step 3: Analyze content
    print("Step 3: Analyzing content...")
    synthesized_content = content_analyzer.synthesize_content(
        original_query, sub_queries, all_data
    )
    
    # Step 4: Generate report
    print("Step 4: Generating report...")
    report_path = report_generator.generate_pdf_report(
        original_query, synthesized_content
    )
    
    print(f"Research complete! Report saved to: {report_path}")
    return report_path

# Example usage (uncomment to run):
# report_path = run_research_with_api("The future of renewable energy technologies")