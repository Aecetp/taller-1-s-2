from langchain_core.messages import SystemMessage, HumanMessage
from state import GraphState
from utils.llm import get_llm

def writer_node(state: GraphState):
    """
    Formatea la investigación en un documento final si pasó la revisión.
    Si fue abortada por baja calidad, genera un reporte indicando la falla.
    """
    is_aborted = state.get("is_aborted", False)
    topic = state.get("topic", "")
    
    if is_aborted:
        # Mensaje de falla estático en caso de aborto
        draft = (f"**Reporte de Investigación Abortado**\n\n"
                 f"**Tema:** {topic}\n\n"
                 f"Tras múltiples intentos de investigación y revisión cruzada, "
                 f"el modelo concluye que no está preparado para dar información verídica "
                 f"y 100% confiable sobre este tema aún.\n"
                 f"Se requiere intervención y revisión humana profunda antes de publicar resultados.")
        return {
            "final_draft": draft,
            "decision_log": ["[Writer] Reporte abortado generado."],
            "publisher_payload": {"content": draft, "title": f"Abortado: {topic}"}
        }
        
   
    notes = state.get("research_notes", "")
    score = state.get("reliability_score", 0)
    
    llm = get_llm()
    
    system_prompt = """Eres un redactor profesional experto en crear reportes formales listos para revisión humana (HITL).
    Toma las notas crudas de investigación y dales formato de artículo o reporte final.
    IMPORTANTE: Al final del documento, expón sutilmente la métrica de fiabilidad obtenida en la auditoría."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Notas a redactar: {notes}\nMétrica de fiabilidad de los datos: {score}/100")
    ]
    response = llm.invoke(messages)
    
    usage = getattr(response, 'usage_metadata', {})
    tokens = usage.get('total_tokens', len(response.content) // 4) if usage else len(response.content) // 4

    # Retornar el reporte final redactado ('final_draft') y el Context Payload para el A2A.
    return {
        "final_draft": response.content,
        "token_cost": tokens,
        "decision_log": [f"[Writer] Borrador final generado. ({tokens} tokens)"],
        "publisher_payload": {"content": response.content, "title": topic}
    }
