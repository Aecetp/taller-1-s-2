# ============================================================
# LAB S2: ARCHIVO PARA COMPLETAR EN VIVO
#
# Base: Ya conocemos nodos, aristas y estado (S1).
# Nuevo en S2:
#   - publisher_node (nodo A2A)
#   - token_cost y decision_log en CADA nodo (Governance)
#   - Checkpointing con MemorySaver
#   - interrupt_before=["publisher"] para HITL
# ============================================================

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
# ==========================================
# Patrón idéntico a S1, pero ahora cada nodo
# también retorna 'token_cost' y 'decision_log'.

def researcher_node(state: GraphState):
    """Nodo Investigador: igual que S1 + registra tokens y log."""
    topic = state.get("topic", "")

    # TODO 1: Llamar al agente investigador
    #         Función: call_researcher_agent(topic) → devuelve response (objeto LLM)
    response = ...

    # TODO 2: Extraer tokens de la respuesta
    #         Función: extract_tokens(response) → int
    tokens = ...

    mock_sources = [
        f"https://ejemplo.com/articulo-1-{topic.replace(' ', '-')}",
        f"https://ejemplo.com/estudio-2-{topic.replace(' ', '-')}",
        "Libro: Fundamentos Avanzados",
        "Paper: Análisis de tendencias 2024"
    ]

    # TODO 3: Retornar el estado actualizado incluyendo:
    #         research_notes, sources, token_cost, decision_log
    return ...


def reviewer_node(state: GraphState):
    """Nodo Revisor: igual que S1 + registra tokens y log."""
    topic   = state.get("topic", "")
    notes   = state.get("research_notes", "")
    sources = state.get("sources", [])

    # TODO 4: Llamar al agente revisor
    #         Función: call_reviewer_agent(topic, notes, sources) → response o None
    response = ...

    reliability = 0
    tokens = 0
    if response:
        # TODO 5: Extraer tokens y parsear el puntaje numérico de response.content
        tokens = ...
        match = re.search(r'\d+', response.content.strip())
        reliability = int(match.group()) if match else random.randint(50, 90)
    else:
        reliability = random.randint(50, 90)

    retries = state.get("revision_retries", 0) + 1

    # TODO 6: Retornar reliability_score, revision_retries, token_cost, decision_log
    return ...


def writer_node(state: GraphState):
    """Nodo Redactor: igual que S1 + prepara publisher_payload para A2A."""
    is_aborted = state.get("is_aborted", False)
    topic = state.get("topic", "")

    # Caso de aborto — ya dado, no modificar
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

    # TODO 7: Llamar al agente redactor
    #         Función: call_writer_agent(notes, score) → response
    response = ...

    # TODO 8: Extraer tokens
    tokens = ...

    # TODO 9: Retornar final_draft, publisher_payload, token_cost, decision_log
    #         publisher_payload = {"content": response.content, "title": topic}
    return ...


def publisher_node(state: GraphState):
    """
    [A2A] Nodo Publicador: recibe SOLO el publisher_payload (no todo el estado).
    Simula un agente externo especializado que genera metadatos SEO.
    """
    # TODO 10: Obtener el publisher_payload del estado y extraer 'content'
    payload = ...
    content = ...

    if not content:
        return {
            "published_result": "❌ Error: payload vacío.",
            "decision_log": ["[Publicador] Error: no se recibió contenido."]
        }

    # TODO 11: Llamar al agente publicador
    #          Función: call_publisher_agent(content) → response
    response = ...

    # TODO 12: Extraer tokens
    tokens = ...

    # Parsear el JSON que devuelve el agente (ya dado)
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

    # TODO 13: Retornar published_result, token_cost, decision_log
    return ...


def abort_node(state: GraphState):
    """Marca el estado como abortado — ya dado."""
    return {
        "is_aborted": True,
        "decision_log": ["[Sistema] Flujo abortado por baja fiabilidad repetida."]
    }


# ==========================================
# 2. ARISTA CONDICIONAL (igual que S1)
# ==========================================

def check_reliability(state: GraphState):
    """Decide el siguiente nodo según fiabilidad e intentos."""
    score   = state.get("reliability_score", 0)
    retries = state.get("revision_retries", 0)

    # TODO 14: Lógica de decisión (mismo que S1)
    #   score >= 70  → "writer"
    #   retries < 3  → "researcher"
    #   else         → "abort"
    ...


# ==========================================
# 3. CONSTRUCCIÓN DEL GRAFO
# ==========================================

def create_graph():
    """
    Construye el StateGraph.
    DIFERENCIAS respecto a S1:
      - Se añade el nodo 'publisher'
      - Se usa MemorySaver para checkpointing
      - Se compila con interrupt_before=["publisher"] para HITL
    """
    builder = StateGraph(GraphState)

    # TODO 15: Registrar los 5 nodos
    #   researcher, reviewer, writer, publisher, abort_node
    ...

    # Punto de entrada (igual que S1)
    builder.set_entry_point("researcher")

    # TODO 16: Aristas estáticas
    #   researcher → reviewer
    #   abort_node → writer
    #   writer     → publisher      ← NUEVA (en S1 iba directo a END)
    #   publisher  → END
    ...

    # TODO 17: Arista condicional desde "reviewer" (igual que S1)
    ...

    # TODO 18: Instanciar MemorySaver y compilar con checkpointer e interrupt_before
    #   memory = MemorySaver()
    #   graph  = builder.compile(checkpointer=memory, interrupt_before=["publisher"])
    memory = ...
    graph  = ...

    return graph
