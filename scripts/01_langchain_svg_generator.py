# 01_langchain_svg_generator.py
"""
LangChain-based SVG Generator
Generates SVG diagrams from concept prompts using multiple LLM providers.
"""

from langchain.chat_models import ChatOpenAI, ChatAnthropic, ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
import re

class SVGGenerator:
    """Generate SVG diagrams using LangChain and various LLM providers."""
    
    def __init__(self):
        # Initialize supported LLM providers
        self.providers = {
            "openai": ChatOpenAI(temperature=0.7),
            "claude": ChatAnthropic(),
            "ollama": ChatOllama(model="llama3")
        }
        
        self.svg_prompt_template = """
Create an SVG diagram that represents the following concept:

{concept}

Requirements:
- Use standard SVG elements (rect, circle, path, text, etc.)
- Include appropriate colors and styling
- Ensure the diagram is clear and readable
- Add proper text labels
- Use viewBox="0 0 800 600" for dimensions
- Wrap the entire SVG in <svg> tags
- Do not include any explanation, just the SVG code

SVG Diagram:
"""

    async def generate_svg(self, concept, provider="claude", max_retries=2):
        """Generate an SVG diagram based on a concept."""
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")
        
        llm = self.providers[provider]
        prompt = self.svg_prompt_template.format(concept=concept)
        
        for attempt in range(max_retries + 1):
            try:
                messages = [HumanMessage(content=prompt)]
                response = await llm.agenerate([messages])
                
                svg_text = response.generations[0][0].text
                
                # Validate it's proper SVG
                if "<svg" in svg_text and "</svg>" in svg_text:
                    svg_match = re.search(r'(<svg[\\s\\S]*?</svg>)', svg_text, re.DOTALL)
                    if svg_match:
                        return svg_match.group(1)
                    return svg_text
                else:
                    if attempt < max_retries:
                        continue
                    raise ValueError("Generated content is not valid SVG.")
            
            except Exception as e:
                if attempt < max_retries:
                    continue
                raise RuntimeError(f"Failed after {max_retries} attempts: {str(e)}")
        
        raise RuntimeError("SVG generation failed after retries.")

