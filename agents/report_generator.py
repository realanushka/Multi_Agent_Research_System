from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import Dict
import os

class ReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_pdf_report(self, original_query: str, synthesized_content: Dict) -> str:
        """
        Create a polished PDF report from the synthesized content
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{original_query.replace(' ', '_')}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            # Create the PDF document
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                alignment=TA_LEFT
            )
            
            content_style = ParagraphStyle(
                'CustomContent',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=12,
                alignment=TA_LEFT,
                firstLineIndent=20
            )
            
            # Build the document content
            story = []
            
            # Title page
            story.append(Paragraph(synthesized_content.get('title', 'Research Report'), title_style))
            story.append(Spacer(1, 0.5*inch))
            story.append(Paragraph(f"Original Query: {original_query}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(PageBreak())
            
            # Table of contents would go here in a more advanced version
            
            # Main content sections
            for section in synthesized_content.get('sections', []):
                story.append(Paragraph(section['heading'], heading_style))
                story.append(Spacer(1, 0.1*inch))
                
                # Split content into paragraphs
                paragraphs = section['content'].split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para.strip(), content_style))
                        story.append(Spacer(1, 0.1*inch))
                
                # Add sources
                if section.get('sources'):
                    sources_text = "<br/>".join([f"• <link href='{url}'>{url}</link>" for url in section['sources']])
                    story.append(Paragraph(f"<b>Sources:</b><br/>{sources_text}", styles['Normal']))
                    story.append(Spacer(1, 0.2*inch))
            
            # Conclusion
            conclusion = synthesized_content.get('conclusion')
            if conclusion:
                story.append(Paragraph("Conclusion", heading_style))
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph(conclusion, content_style))
            
            # Build PDF
            doc.build(story)
            return filepath
            
        except Exception as e:
            print(f"Error generating PDF report: {e}")
            # Fallback to simple text report
            return self._generate_text_report(original_query, synthesized_content, filepath)
    
    def _generate_text_report(self, original_query: str, synthesized_content: Dict, filepath: str) -> str:
        """
        Fallback method to generate a simple text report if PDF generation fails
        """
        text_filepath = filepath.replace('.pdf', '.txt')
        try:
            with open(text_filepath, 'w', encoding='utf-8') as f:
                f.write(f"RESEARCH REPORT\\n")
                f.write(f"Title: {synthesized_content.get('title', 'Research Report')}\\n")
                f.write(f"Original Query: {original_query}\\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                f.write("=" * 50 + "\\n\\n")
                
                for section in synthesized_content.get('sections', []):
                    f.write(f"{section['heading']}\\n")
                    f.write("-" * len(section['heading']) + "\\n")
                    f.write(f"{section['content']}\\n\\n")
                    
                    if section.get('sources'):
                        f.write("Sources:\\n")
                        for url in section['sources']:
                            f.write(f"  • {url}\\n")
                        f.write("\\n")
                
                conclusion = synthesized_content.get('conclusion')
                if conclusion:
                    f.write("CONCLUSION\\n")
                    f.write("-" * 10 + "\\n")
                    f.write(f"{conclusion}\\n")
            
            return text_filepath
        except Exception as e:
            print(f"Error generating text report: {e}")
            return None