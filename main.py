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

    # 1. Crear el grafo (con MemorySaver y interrupt_before=["publisher"])
    graph = create_graph()

    # 2. Definir el tema
    topic = input("\n📝 Ingresa un tema de investigación: ")
    if not topic.strip():
        topic = "Impacto de la IA en la Educación"
        print(f"Usando tema por defecto: {topic}")

    # Estado inicial
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

    # thread_id: identificador de sesión para el checkpointer
    # Si corremos el script de nuevo con el mismo ID, retomará desde donde quedó.
    config = {"configurable": {"thread_id": "sesion-s2"}}

    print_separator("FASE 1: FLUJO INVESTIGACIÓN → REDACCIÓN")

    # 3. Ejecutar hasta la interrupción (justo antes del nodo 'publisher')
    for step in graph.stream(initial_state, config=config):
        for node_name, state_update in step.items():
            print(f"\n✅ Nodo '{node_name}' completado.")
            if "reliability_score" in state_update:
                print(f"   📊 Fiabilidad: {state_update['reliability_score']}/100 "
                      f"(Intento {state_update.get('revision_retries', '?')})")
            if "token_cost" in state_update:
                print(f"   🔢 Tokens en este paso: {state_update['token_cost']}")
            if "decision_log" in state_update:
                for log in state_update["decision_log"]:
                    print(f"   📝 {log}")

    # 4. El grafo está en pausa antes de 'publisher' → HITL
    print_separator("PAUSA: APROBACIÓN HUMANA REQUERIDA (HITL)")
    current_state = graph.get_state(config)
    print(f"\n⏸️  El grafo está detenido. Siguiente nodo: {current_state.next}")
    print("\n--- Vista previa del borrador ---")
    draft_preview = current_state.values.get("final_draft", "")
    print(draft_preview[:500] + ("..." if len(draft_preview) > 500 else ""))

    approval = input("\n🧑 ¿Apruebas la publicación? (s/n): ").strip().lower()

    if approval == "s":
        print("\n▶️  Reanudando el flujo hacia el Publisher (A2A)...")
        print_separator("FASE 2: PUBLICACIÓN A2A")
        # Reanudar pasando None como input (el estado ya está guardado en el checkpointer)
        for step in graph.stream(None, config=config):
            for node_name, state_update in step.items():
                print(f"\n✅ Nodo '{node_name}' completado.")
                if "token_cost" in state_update:
                    print(f"   🔢 Tokens: {state_update['token_cost']}")
                if "decision_log" in state_update:
                    for log in state_update["decision_log"]:
                        print(f"   📝 {log}")
    else:
        print("\n❌ Publicación cancelada por el operador humano.")

    # 5. Panel de observabilidad final
    print_separator("PANEL DE GOVERNANCE Y OBSERVABILIDAD")
    final = graph.get_state(config).values

    print(f"💰 Tokens totales consumidos : {final.get('token_cost', 0)}")
    print(f"📊 Fiabilidad final          : {final.get('reliability_score', 0)}/100")
    print(f"🔄 Intentos de investigación : {final.get('revision_retries', 0)}")
    print(f"\n📜 Traza de decisiones:")
    for log in final.get("decision_log", []):
        print(f"   · {log}")

    if approval == "s":
        print_separator("RESULTADO DE PUBLICACIÓN (A2A)")
        print(final.get("published_result", "Sin resultado de publicación."))

if __name__ == "__main__":
    run_lab()
