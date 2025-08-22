import os
from groq import Groq
from typing import List

class QueryProcessor:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if api_key and api_key != "your_actual_groq_api_key_here":
            self.client = Groq(api_key=api_key)
        else:
            self.client = None
            print("Warning: Groq API key not found. Using fallback decomposition method.")
    
    def decompose_query(self, query: str) -> List[str]:
        """
        Decompose a broad query into 3-5 focused sub-queries
        """
        if not self.client:
            print("Using fallback decomposition due to missing API key")
            return self._fallback_decomposition(query)
            
        prompt = f"""
        Decompose the following broad research query into 3-5 focused sub-queries:
        "{query}"
        
        Requirements:
        - Each sub-query should be specific and researchable
        - Sub-queries should collectively cover the main topic comprehensively
        - Avoid overlapping or duplicate sub-queries
        - Format the response as a JSON array of strings
        
        Example:
        Input: "Impact of AI in healthcare"
        Output: ["AI applications in medical diagnosis", "Machine learning in patient care", "Ethical considerations of healthcare AI"]
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
                temperature=0.5,
                max_tokens=200,
            )
            
            # Extract the content and parse as JSON
            import json
            content = response.choices[0].message.content.strip()
            # Handle potential markdown code blocks
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            
            sub_queries = json.loads(content)
            return sub_queries[:5]  # Limit to 5 sub-queries maximum
            
        except Exception as e:
            print(f"Error in decompose_query: {e}")
            # Fallback to manual decomposition
            return self._fallback_decomposition(query)
    
    def _fallback_decomposition(self, query: str) -> List[str]:
        """
        Fallback method if LLM fails
        """
        # Simple heuristic-based decomposition
        base_query = query.lower()
        if "ai" in base_query or "artificial intelligence" in base_query:
            return [
                f"What are the applications of {query}?",
                f"What are the benefits of {query}?",
                f"What are the challenges of {query}?",
                f"What is the future of {query}?"
            ]
        elif "machine learning" in base_query:
            return [
                f"What are the types of {query}?",
                f"What are the applications of {query}?",
                f"What are the challenges in {query}?",
                f"What are recent advances in {query}?"
            ]
        elif "data science" in base_query:
            return [
                f"What are the tools used in {query}?",
                f"What are the career opportunities in {query}?",
                f"What are the key skills for {query}?",
                f"How is {query} evolving?"
            ]
        else:
            return [
                f"What are the key aspects of {query}?",
                f"What are the impacts of {query}?",
                f"What are the challenges related to {query}?",
                f"What are recent developments in {query}?"
            ]