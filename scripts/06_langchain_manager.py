# LangChain Manager
# 06_langchain_manager.py
"""
LangChain Manager
Handles LLM client initialization and prompt-based SVG generation.
"""

from langchain.chat_models import ChatOpenAI, ChatAnthropic, ChatOllama
from langchain.schema import HumanMessage
import re

class LangChainManager:
    """Manage different LLM providers via LangChain."""
    
    def __init__(self, default_provider="claude"):
        self.providers = {
            "openai": ChatOpenAI(temperature=0.7),
            "claude": ChatAnthropic(),
            "ollama": ChatOllama(model="llama3")
        }
        self.default_provider = default_provider

        self.svg_prompt_template = """
Create an SVG diagram that represents the following concept:

{concept}

Requirements:
- Use standard SVG elements (rect, circle, path, text, etc.)
- Include appropriate colors and styling
- Add proper labels
- Use viewBox="0 0 800 600"
- Output only SVG code, no explanations.

SVG Diagram:
"""

    def set_provider(self, provider_name):
        """Change default LLM provider."""
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not available.")
        self.default_provider = provider_name
        print(f"✅ Default provider set to: {provider_name}")

    async def generate_svg(self, concept, provider=None, max_retries=2):
        """Generate SVG from a concept using a specified or default provider."""
        provider = provider or self.default_provider
        if provider not in self.providers:
            raise ValueError(f"Provider '{provider}' not recognized.")

        llm = self.providers[provider]
        prompt = self.svg_prompt_template.format(concept=concept)

        for attempt in range(max_retries + 1):
            try:
                messages = [HumanMessage(content=prompt)]
                response = await llm.agenerate([messages])

                svg_text = response.generations[0][0].text

                if "<svg" in svg_text and "</svg>" in svg_text:
                    svg_match = re.search(r'(<svg[\\s\\S]*?</svg>)', svg_text, re.DOTALL)
                    if svg_match:
                        return svg_match.group(1)
                    return svg_text
                else:
                    if attempt < max_retries:
                        continue
                    raise ValueError("Generated content does not contain valid SVG.")

            except Exception as e:
                if attempt < max_retries:
                    continue
                raise RuntimeError(f"LLM generation failed after retries: {str(e)}")

        raise RuntimeError("SVG generation ultimately failed.")

