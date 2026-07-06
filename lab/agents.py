from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm import get_llm
import random
import re
import json

# ==========================================
# PERSONALIDAD DE LOS AGENTES (prompts + LLM)
# Estas funciones NO conocen LangGraph ni el Estado.
# Solo reciben datos, consultan al LLM y retornan texto.
# ==========================================

def call_researcher_agent(topic: str) -> str:
    """Investigador: Genera notas de investigación sobre el tema dado."""
    llm = get_llm()
    system_prompt = """Eres un investigador experto. Tu tarea es encontrar información detallada 
    sobre el tema proporcionado. Devuelve un breve resumen de tu investigación."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Tema a investigar: {topic}")
    ]
    return llm.invoke(messages)


def call_reviewer_agent(topic: str, notes: str, sources: list):
    """Revisor: Evalúa la fiabilidad de las notas de investigación (0-100)."""
    llm = get_llm(temperature=0)
    system_prompt = f"""Eres un auditor estricto. Revisa las notas de investigación sobre '{topic}' 
    y verifica que se apoyen lógicamente en algo sólido. Evalúa la fiabilidad del 0 al 100.
    Sé muy crítico y meticuloso. Solo devuelve un número entero del 0 al 100 sin texto adicional."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Notas: {notes}\nFuentes citadas: {sources}")
    ]
    try:
        return llm.invoke(messages)
    except Exception:
        return None


def call_writer_agent(notes: str, score: int):
    """Redactor: Da formato final al reporte con la métrica de fiabilidad."""
    llm = get_llm()
    system_prompt = """Eres un redactor profesional experto en crear reportes formales listos para revisión humana.
    Toma las notas crudas de investigación y dales formato de artículo o reporte final.
    IMPORTANTE: Al final del documento, expón sutilmente la métrica de fiabilidad obtenida en la auditoría."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Notas a redactar: {notes}\nMétrica de fiabilidad: {score}/100")
    ]
    return llm.invoke(messages)


def call_publisher_agent(content: str):
    """
    Publicador (A2A): Recibe un contenido estructurado y genera metadatos SEO.
    Simula un agente externo que recibe un payload y retorna un resultado JSON estricto.
    """
    llm = get_llm(temperature=0.2)
    system_prompt = """Eres el Agente Publicador (Publisher API).
    Tu tarea es recibir contenido en markdown, generar metadatos SEO y devolver
    estrictamente un JSON válido con esta estructura (sin bloques de código):
    {
      "url": "https://miblog.com/slug-generado",
      "seo_tags": ["tag1", "tag2"],
      "status": "PUBLICADO",
      "resumen_seo": "Descripción corta de 1-2 líneas para buscadores."
    }"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Contenido a publicar:\n{content}")
    ]
    return llm.invoke(messages)


def extract_tokens(response) -> int:
    """Extrae el total de tokens usados de la respuesta del LLM."""
    usage = getattr(response, 'usage_metadata', {})
    if usage:
        return usage.get('total_tokens', len(response.content) // 4)
    return len(response.content) // 4
