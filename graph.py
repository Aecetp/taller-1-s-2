from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state import GraphState
from agents import (
    call_researcher_agent, call_reviewer_agent,
    call_writer_agent, call_publisher_agent, extract_tokens
)
import random
import re
import json

# ==========================================
# 1. NODOS DEL GRAFO
# Cada nodo: lee del estado → llama al agente → retorna el diff del estado.
# ==========================================

def researcher_node(state: GraphState):
    """Lee el tema, llama al investigador y actualiza notas y fuentes."""
    topic = state.get("topic", "")
    response = call_researcher_agent(topic)
    tokens = extract_tokens(response)

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
        "decision_log": [f"[Investigador] Búsqueda completada. ({tokens} tokens)"]
    }


def reviewer_node(state: GraphState):
    """Lee las notas, llama al revisor y actualiza la puntuación de fiabilidad."""
    topic = state.get("topic", "")
    notes = state.get("research_notes", "")
    sources = state.get("sources", [])

    response = call_reviewer_agent(topic, notes, sources)

    reliability = 0
    tokens = 0
    if response:
        tokens = extract_tokens(response)
        # response.content puede ser str (Gemini) o lista de bloques (Claude)
        raw = response.content if isinstance(response.content, str) else str(response.content)
        match = re.search(r'\d+', raw.strip())
        reliability = int(match.group()) if match else random.randint(50, 90)
    else:
        reliability = random.randint(50, 90)

    retries = state.get("revision_retries", 0) + 1

    return {
        "reliability_score": reliability,
        "revision_retries": retries,
        "token_cost": tokens,
        "decision_log": [f"[Revisor] Fiabilidad: {reliability}/100. Intento {retries}. ({tokens} tokens)"]
    }


def writer_node(state: GraphState):
    """Lee las notas y el puntaje, llama al redactor y genera el borrador final."""
    is_aborted = state.get("is_aborted", False)
    topic = state.get("topic", "")

    if is_aborted:
        draft = (f"**Reporte Abortado**\n\n**Tema:** {topic}\n\n"
                 f"Tras múltiples intentos, el sistema no puede garantizar "
                 f"información confiable sobre este tema.")
        return {
            "final_draft": draft,
            "publisher_payload": {"content": draft, "title": f"Abortado: {topic}"},
            "decision_log": ["[Redactor] Reporte de aborto generado."]
        }

    notes = state.get("research_notes", "")
    score = state.get("reliability_score", 0)
    response = call_writer_agent(notes, score)
    tokens = extract_tokens(response)

    return {
        "final_draft": response.content,
        "publisher_payload": {"content": response.content, "title": topic},
        "token_cost": tokens,
        "decision_log": [f"[Redactor] Borrador final generado. ({tokens} tokens)"]
    }


def publisher_node(state: GraphState):
    """
    [A2A] Recibe el payload estructurado del writer y lo 'publica'.
    Simula la comunicación Agent-to-Agent: recibe solo el payload, no todo el estado.
    """
    payload = state.get("publisher_payload", {})
    content = payload.get("content", "")

    if not content:
        return {
            "published_result": "❌ Error: payload vacío.",
            "decision_log": ["[Publicador] Error: no se recibió contenido."]
        }

    response = call_publisher_agent(content)
    tokens = extract_tokens(response)

    # Intentar parsear el JSON retornado por el agente
    try:
        raw = response.content.strip().replace("```json", "").replace("```", "")
        result_data = json.loads(raw)
        result_text = (
            f"✅ Publicado en: {result_data.get('url', 'N/A')}\n"
            f"   Tags SEO: {', '.join(result_data.get('seo_tags', []))}\n"
            f"   Estado: {result_data.get('status', 'N/A')}\n"
            f"   Resumen: {result_data.get('resumen_seo', '')}"
        )
    except Exception:
        result_text = f"⚠️ Publicado (respuesta no-JSON): {response.content[:200]}"

    return {
        "published_result": result_text,
        "token_cost": tokens,
        "decision_log": [f"[Publicador] Acción A2A completada. ({tokens} tokens)"]
    }


def abort_node(state: GraphState):
    """Marca el estado como abortado para que el writer genere un reporte de fallo."""
    return {
        "is_aborted": True,
        "decision_log": ["[Sistema] Flujo abortado por baja fiabilidad repetida."]
    }


# ==========================================
# 2. ARISTA CONDICIONAL
# ==========================================

def check_reliability(state: GraphState):
    """Decide el siguiente nodo según la fiabilidad y los reintentos."""
    score = state.get("reliability_score", 0)
    retries = state.get("revision_retries", 0)

    if score >= 70:
        return "writer"
    elif retries < 3:
        return "researcher"
    else:
        return "abort"


# ==========================================
# 3. CONSTRUCCIÓN Y COMPILACIÓN DEL GRAFO
# ==========================================

def create_graph():
    """
    Construye el StateGraph con:
    - Checkpointing (MemorySaver) para persistencia entre ejecuciones.
    - interrupt_before=["publisher"] para aprobación humana (HITL).
    """
    builder = StateGraph(GraphState)

    # Agregar nodos
    builder.add_node("researcher", researcher_node)
    builder.add_node("reviewer", reviewer_node)
    builder.add_node("writer", writer_node)
    builder.add_node("publisher", publisher_node)
    builder.add_node("abort_node", abort_node)

    # Punto de entrada
    builder.set_entry_point("researcher")

    # Aristas estáticas
    builder.add_edge("researcher", "reviewer")
    builder.add_edge("abort_node", "writer")
    builder.add_edge("writer", "publisher")
    builder.add_edge("publisher", END)

    # Arista condicional desde el revisor
    builder.add_conditional_edges(
        "reviewer",
        check_reliability,
        {
            "writer": "writer",
            "researcher": "researcher",
            "abort": "abort_node"
        }
    )

    # Checkpointing: persiste el estado en memoria entre ejecuciones
    memory = MemorySaver()

    # Compilar con checkpointer e interrupción antes del publisher (HITL)
    graph = builder.compile(
        checkpointer=memory,
        interrupt_before=["publisher"]
    )

    return graph
