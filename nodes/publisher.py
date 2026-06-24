from langchain_core.messages import SystemMessage, HumanMessage
from state import GraphState
from utils.llm import get_llm
import json

def publisher_node(state: GraphState):
    """
    [A2A] Agente Externo simulado.
    Recibe un payload altamente estructurado (Context Engineering) y 
    realiza una acción destructiva (ej. Publicar en Web).
    """
    payload = state.get("publisher_payload", {})
    if not payload:
        return {"published_result": "Error: No payload provided to publisher", "decision_log": ["[Publisher] Error: Payload vacío"]}

    # El payload es el único contexto. No se pasa toda la historia del grafo.
    content = payload.get("content", "")
    
    llm = get_llm(temperature=0.2)
    
    system_prompt = """Eres el Agente Publicador (Publisher API). 
    Tu tarea es recibir un contenido final en formato markdown, generar metadatos SEO 
    (slug, tags, descripción corta) y devolver estrictamente un JSON válido con esta estructura:
    {
      "url": "https://miblog.com/generado-slug",
      "seo_tags": ["tag1", "tag2"],
      "status": "PUBLICADO",
      "html_preview": "..."
    }
    No incluyas markdown como ```json, solo el objeto JSON puro.
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Contenido a publicar:\n{content}")
    ]
    
    try:
        # TODO 3: Invocar al LLM, extraer el JSON (limpiando ```json si es necesario)
        # y retornar el diccionario con 'published_result', 'token_cost' y 'decision_log'.
        
        # Simulamos respuesta de error temporalmente para evitar crash:
        return {
            "published_result": "❌ No implementado",
            "token_cost": 0,
            "decision_log": ["[Publisher] Falta implementación"]
        }
    except Exception as e:
        return {
            "published_result": f"❌ Error en publicación: {str(e)}",
            "decision_log": [f"[Publisher] Fallo en la serialización JSON o API: {str(e)}"]
        }
