from dotenv import load_dotenv
from graph import create_graph

load_dotenv()

def print_separator(title=""):
    print(f"\n{'='*60}")
    if title:
        print(f" {title} ".center(60, "="))
    print(f"{'='*60}")

def run_lab():
    print_separator("LABORATORIO S2: LANGGRAPH AVANZADO")
    print("Conceptos: Checkpointing · HITL · A2A · Governance")

    graph = create_graph()

    topic = input("\n📝 Ingresa un tema de investigación: ")
    if not topic.strip():
        topic = "Impacto de la IA en la Educación"
        print(f"Usando tema por defecto: {topic}")

    initial_state = {
        "topic": topic,
        "sources": [],
        "research_notes": "",
        "reliability_score": 0,
        "revision_retries": 0,
        "final_draft": "",
        "is_aborted": False,
        "publisher_payload": {},
        "published_result": "",
        "token_cost": 0,
        "decision_log": []
    }

    # El config lleva el thread_id que usa el MemorySaver para recordar la sesión
    config = {"configurable": {"thread_id": "sesion-s2"}}

    print_separator("FASE 1: INVESTIGACIÓN → REDACCIÓN")

    # TODO A: Stream FASE 1 — ejecutar el grafo hasta la pausa (interrupt_before=["publisher"])
    # Pista: igual que S1 pero pasando config como segundo argumento
    #   for step in graph.stream(initial_state, config=config):
    #       for node_name, state_update in step.items():
    #           print(f"✅ Nodo '{node_name}' completado.")
    #           # Muestra reliability_score, token_cost y decision_log si existen
    ...

    # TODO B: Leer el estado actual del grafo (está en pausa antes del publisher)
    #   current_state = graph.get_state(config)
    #   print(f"⏸️  Siguiente nodo: {current_state.next}")
    #   Muestra los primeros 500 caracteres del final_draft como vista previa
    ...

    print_separator("PAUSA: APROBACIÓN HUMANA (HITL)")
    approval = input("\n🧑 ¿Apruebas la publicación? (s/n): ").strip().lower()

    if approval == "s":
        print_separator("FASE 2: PUBLICACIÓN A2A")
        # TODO C: Reanudar el grafo pasando None como estado
        # El checkpointer ya sabe dónde estaba — None le dice "continúa desde aquí"
        #   for step in graph.stream(None, config=config):
        #       ...
        ...
    else:
        print("\n❌ Publicación cancelada por el operador humano.")

    # TODO D: Panel de Governance — leer el estado final con graph.get_state(config).values
    # Mostrar: token_cost, reliability_score, revision_retries, decision_log
    print_separator("PANEL DE GOVERNANCE Y OBSERVABILIDAD")
    ...

    if approval == "s":
        print_separator("RESULTADO DE PUBLICACIÓN (A2A)")
        # TODO E: Imprimir el 'published_result' del estado final
        ...

if __name__ == "__main__":
    run_lab()
