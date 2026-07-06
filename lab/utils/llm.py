import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

def get_llm(provider: str = "gemini", temperature: float = 0):
    """
    Retorna la instancia del LLM configurada.
    Por defecto usa Gemini, pero está preparado para cambiar a Claude fácilmente.
    """
    if provider == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY no encontrada en las variables de entorno.")
        # Usamos gemini-1.5-flash como modelo base rápido y económico
        return ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=temperature)
    
    elif provider == "claude":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY no encontrada en las variables de entorno.")
        return ChatAnthropic(model="claude-3-haiku-20240307", temperature=temperature)
    
    else:
        raise ValueError(f"Proveedor LLM no soportado: {provider}")
