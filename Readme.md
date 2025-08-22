# Multi-Agent Research System

This project is a **Multi-Agent Research System** implemented in Python. It leverages a language learning model (LLM) and web scraping techniques to generate detailed research reports from broad user queries. The system decomposes queries, collects and synthesizes information from the web, and produces professional PDF reports.

## Features

- Query decomposition into focused sub-queries
- Web scraping from multiple sources
- Content synthesis and analysis
- Professional PDF report generation

## Prerequisites

- Python 3.8+
- Groq API key (free tier available)

## Installation

1. Clone the repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```
   (Get your free API key at https://console.groq.com/)

## Usage

```python
python main.py "Your research query here"
```

Example:
```python
python main.py "Impact of AI in healthcare"
```

## How It Works

The system consists of four specialized agents working together:

1. **Query Processor**: Decomposes broad queries into focused sub-queries using LLM
2. **Data Collector**: Gathers information from web sources through scraping
3. **Content Analyzer**: Synthesizes and structures the collected data using LLM
4. **Report Generator**: Creates a professional PDF report with ReportLab

## Technical Stack

- **LLM Provider**: Groq API (free tier available)
- **Web Scraping**: BeautifulSoup, requests
- **PDF Generation**: ReportLab
- **Programming Language**: Python

## Fallback Mechanisms

When the Groq API key is not provided or web scraping fails, the system gracefully degrades to fallback mechanisms:
- Rule-based query decomposition
- Basic content synthesis from available data
- PDF generation with available content

## Output

The system generates:
1. A timestamped PDF report in the `reports/` directory
2. A `synthesized_content.json` file with the structured content

## Configuration

- The system will work without an API key using fallback methods
- For full functionality, obtain a free Groq API key and add it to your `.env` file