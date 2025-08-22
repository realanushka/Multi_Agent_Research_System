import os
from groq import Groq
from typing import List, Dict

class ContentAnalyzer:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if api_key and api_key != "your_actual_groq_api_key_here":
            self.client = Groq(api_key=api_key)
        else:
            self.client = None
            print("Warning: Groq API key not found. Using fallback synthesis method.")
    
    def synthesize_content(self, original_query: str, sub_queries: List[str], collected_data: List[Dict]) -> Dict:
        """
        Synthesize collected data into coherent, structured summaries
        """
        # Use fallback if no API key
        if not self.client:
            print("Using fallback synthesis due to missing API key")
            return self._fallback_synthesis(original_query, collected_data)
        
        # Prepare the content for analysis
        content_summary = self._prepare_content_summary(collected_data)
        
        prompt = f"""
        Based on the following research data, create a comprehensive report that answers the original query:
        "{original_query}"
        
        Sub-queries that were researched:
        {sub_queries}
        
        Research data:
        {content_summary}
        
        Requirements:
        1. Organize the content into 3-4 main sections with clear headings
        2. Each section should have 3-5 paragraphs
        3. Include key findings and actionable insights
        4. Cite sources at the end of each section (just URLs)
        5. Maintain a professional, academic tone
        6. Format the response as JSON with the following structure:
        {{
            "title": "Report Title",
            "sections": [
                {{
                    "heading": "Section Heading",
                    "content": "Section content as a string",
                    "sources": ["url1", "url2"]
                }}
            ],
            "conclusion": "Overall conclusion"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192",
                temperature=0.3,
                max_tokens=4000,
            )
            
            # Extract the content and parse as JSON
            import json
            content = response.choices[0].message.content.strip()
            # Handle potential markdown code blocks
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            
            return json.loads(content)
            
        except Exception as e:
            print(f"Error in synthesize_content: {e}")
            # Fallback to basic synthesis
            return self._fallback_synthesis(original_query, collected_data)
    
    def _prepare_content_summary(self, collected_data: List[Dict]) -> str:
        """
        Prepare a summary of collected data for the LLM
        """
        summary_parts = []
        for i, data in enumerate(collected_data):
            part = f"Source {i+1} (URL: {data['url']})\nTitle: {data['title']}\nContent: {data['content'][:500]}..."
            summary_parts.append(part)
        
        return "\n\n".join(summary_parts)
    
    def _fallback_synthesis(self, original_query: str, collected_data: List[Dict]) -> Dict:
        """
        Fallback method if LLM fails
        """
        sections = []
        for i, data in enumerate(collected_data[:3]):  # Limit to 3 sections
            sections.append({
                "heading": f"Research Findings {i+1}",
                "content": data['content'][:800],  # Limit content length
                "sources": [data['url']]
            })
        
        return {
            "title": f"Research Report: {original_query}",
            "sections": sections,
            "conclusion": "This report provides a comprehensive overview of the research topic based on the analyzed sources."
        }