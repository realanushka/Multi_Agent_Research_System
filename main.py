import os
import sys
import json
from dotenv import load_dotenv
from agents.query_processor import QueryProcessor
from agents.data_collector import DataCollector
from agents.content_analyzer import ContentAnalyzer
from agents.report_generator import ReportGenerator

# Load environment variables
load_dotenv()

class ResearchSystem:
    def __init__(self):
        self.query_processor = QueryProcessor()
        self.data_collector = DataCollector()
        self.content_analyzer = ContentAnalyzer()
        self.report_generator = ReportGenerator()
    
    def run_research(self, original_query: str):
        """
        Run the complete research pipeline
        """
        print(f"Starting research on: {original_query}")
        
        # Step 1: Decompose query
        print("Step 1: Processing query...")
        sub_queries = self.query_processor.decompose_query(original_query)
        print(f"Generated sub-queries: {sub_queries}")
        
        # Step 2: Collect data
        print("Step 2: Collecting data...")
        all_data = []
        for sub_query in sub_queries:
            print(f"Researching: {sub_query}")
            data = self.data_collector.search_and_scrape(sub_query)
            all_data.extend(data)
        
        print(f"Collected {len(all_data)} sources")
        
        # Step 3: Analyze content
        print("Step 3: Analyzing content...")
        synthesized_content = self.content_analyzer.synthesize_content(
            original_query, sub_queries, all_data
        )
        
        # Save synthesized content for debugging
        with open("synthesized_content.json", "w") as f:
            json.dump(synthesized_content, f, indent=2)
        
        # Step 4: Generate report
        print("Step 4: Generating report...")
        report_path = self.report_generator.generate_pdf_report(
            original_query, synthesized_content
        )
        
        print(f"Research complete! Report saved to: {report_path}")
        return report_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"Your research query here\"")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_actual_groq_api_key_here":
        print("Warning: GROQ_API_KEY not found in environment variables.")
        print("The system will use fallback methods for query decomposition and content analysis.")
        print("For full functionality, please set your Groq API key in a .env file.")
    
    # Run the research system
    system = ResearchSystem()
    system.run_research(query)

if __name__ == "__main__":
    main()