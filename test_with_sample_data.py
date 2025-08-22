import os
import json
from agents.query_processor import QueryProcessor
from agents.data_collector import DataCollector
from agents.content_analyzer import ContentAnalyzer
from agents.report_generator import ReportGenerator

def test_with_sample_data():
    """
    Test the system with sample data to demonstrate functionality
    """
    print("Testing Multi-Agent Research System with sample data...")
    
    # Initialize agents
    query_processor = QueryProcessor()
    content_analyzer = ContentAnalyzer()
    report_generator = ReportGenerator()
    
    # Sample data
    original_query = "Impact of AI in healthcare"
    sub_queries = [
        "AI applications in medical diagnosis",
        "Machine learning in patient care",
        "Ethical considerations of healthcare AI"
    ]
    
    sample_data = [
        {
            "url": "https://example.com/ai-medical-diagnosis",
            "title": "AI in Medical Diagnosis",
            "content": "Artificial intelligence is revolutionizing medical diagnosis by enabling faster and more accurate detection of diseases. Machine learning algorithms can analyze medical images such as X-rays, MRIs, and CT scans to identify abnormalities that might be missed by human radiologists. AI systems have shown promising results in detecting cancers, cardiovascular diseases, and neurological disorders. These technologies not only improve diagnostic accuracy but also reduce the time required for diagnosis, leading to earlier treatment and better patient outcomes."
        },
        {
            "url": "https://example.com/ml-patient-care",
            "title": "Machine Learning in Patient Care",
            "content": "Machine learning is transforming patient care by enabling personalized treatment plans and predictive analytics. Healthcare providers are using ML algorithms to analyze patient data and predict potential health risks before they become critical. This proactive approach to healthcare allows for early interventions and more effective treatment strategies. Additionally, ML-powered chatbots and virtual assistants are improving patient engagement and providing 24/7 support for non-emergency inquiries."
        },
        {
            "url": "https://example.com/ethical-ai-healthcare",
            "title": "Ethical Considerations in Healthcare AI",
            "content": "The implementation of AI in healthcare raises several ethical concerns that need to be addressed. Privacy and data security are paramount, as AI systems require access to sensitive patient information. There are also concerns about algorithmic bias, which could lead to disparities in healthcare delivery. Transparency and explainability of AI decisions are crucial for maintaining trust between patients and healthcare providers. Additionally, the potential for job displacement in the healthcare sector is a significant concern that policymakers need to consider."
        }
    ]
    
    print(f"Original query: {original_query}")
    print(f"Sub-queries: {sub_queries}")
    
    # Analyze content with sample data
    print("Analyzing content...")
    synthesized_content = content_analyzer.synthesize_content(
        original_query, sub_queries, sample_data
    )
    
    # Save synthesized content
    with open("sample_synthesized_content.json", "w") as f:
        json.dump(synthesized_content, f, indent=2)
    
    print("Generated sample synthesized content")
    
    # Generate report
    print("Generating PDF report...")
    report_path = report_generator.generate_pdf_report(
        original_query, synthesized_content
    )
    
    print(f"Sample test complete! Report saved to: {report_path}")

if __name__ == "__main__":
    test_with_sample_data()