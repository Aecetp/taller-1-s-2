from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state import GraphState
from nodes.researcher import researcher_node
from nodes.reviewer import reviewer_node
from nodes.writer import writer_node
from nodes.publisher import publisher_node

def check_reliability(state: GraphState):
    """
    Arista condicional que decide el siguiente paso tras la revisión.
    """
    score = state.get("reliability_score", 0)
    retries = state.get("revision_retries", 0)
    
    # Esta impresión la pasaremos a logs del main luego, pero es útil mantenerla
    # print(f"\n[Evaluación] Fiabilidad: {score}% | Intento: {retries}/3")
    
    
    if score >= 70:
        return "writer"
    elif retries < 3:
        return "researcher"
    else:
        return "abort"

def create_graph():
    """
    Construye y compila el StateGraph conectando todos los nodos.
    Agrega soporte de checkpointing e interrupciones (HITL).
    """

    builder = StateGraph(GraphState)
    

    builder.add_node("researcher", researcher_node)
    builder.add_node("reviewer", reviewer_node)
    builder.add_node("writer", writer_node)
    builder.add_node("publisher", publisher_node)
    
    # Nodo especial para marcar el estado como abortado
    def abort_node(state: GraphState):
        return {"is_aborted": True}
    builder.add_node("abort_node", abort_node)
    
    
    builder.set_entry_point("researcher")
    builder.add_edge("researcher", "reviewer")
    
    # Si se aborta, va al writer para generar reporte de fallo, luego al publicador (o termina).
    # Para el aborto, simplemente terminamos después de redactar la falla.
    builder.add_edge("abort_node", "writer")
    
    # Del writer pasamos al publisher
    builder.add_edge("writer", "publisher")
    
    # Del publisher termina
    builder.add_edge("publisher", END)
    
    
    builder.add_conditional_edges(
        "reviewer",
        check_reliability,
        {
            "writer": "writer",
            "researcher": "researcher",
            "abort": "abort_node"
        }
    )
    
    # --- ORQUESTACIÓN AVANZADA ---
    # TODO 6: Instancia el sistema de memoria para guardar checkpoints (Checkpointer)
    memory = None
    
    # TODO 7: Compila el grafo indicando el checkpointer y dónde interrumpir el flujo (Human-in-command)
    # Por ahora compila sin interrupciones para que no falle:
    graph = builder.compile()
    
    return graph
