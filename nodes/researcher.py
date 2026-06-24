from langchain_core.messages import SystemMessage, HumanMessage
from state import GraphState
from utils.llm import get_llm

def researcher_node(state: GraphState):
    """
    Simula la búsqueda de fuentes de información y la generación de notas.
    """
    topic = state.get("topic", "")
    
    llm = get_llm()
    
    system_prompt = """Eres un investigador experto. Tu tarea es encontrar información detallada 
    sobre el tema proporcionado y listar al menos 4 fuentes (pueden ser URLs simuladas, libros o artículos) 
    relevantes de donde "obtuviste" la información. 
    Devuelve un breve resumen de tu investigación."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Tema a investigar: {topic}")
    ]
    
    response = llm.invoke(messages)
    
    usage = getattr(response, 'usage_metadata', {})
    tokens = usage.get('total_tokens', len(response.content) // 4) if usage else len(response.content) // 4
    
    # Mock de fuentes de investigación (estático)
    mock_sources = [
        f"https://ejemplo.com/articulo-1-{topic.replace(' ', '-')}",
        f"https://ejemplo.com/estudio-2-{topic.replace(' ', '-')}",
        "Libro: Fundamentos Avanzados",
        "Paper: Análisis de tendencias 2024"
    ]
    

    return {
        "research_notes": response.content,
        "sources": mock_sources,
        "token_cost": tokens,
        "decision_log": [f"[Researcher] Búsqueda completada. ({tokens} tokens)"]
    }
