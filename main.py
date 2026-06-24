from dotenv import load_dotenv
from graph import create_graph

# Cargar variables de entorno antes de importar cualquier cosa que use LLMs
load_dotenv()

def print_separator(title=""):
    print(f"\n{'='*60}")
    if title:
        print(f" {title} ".center(60, "="))
    print(f"{'='*60}")

def run_lab():
    print_separator("LABORATORIO MULTIAGENTE AVANZADO LANGGRAPH")
    print("🌟 Temas cubiertos: Orquestación, Checkpointing, A2A, Observabilidad, HITL, Governance.")
    
    # 1. Instanciamos el grafo
    graph = create_graph()
    
    if not graph:
        print("⚠️ El grafo aún no está construido. Completa graph.py primero.")
        return
        
    # 2. Definimos el tema de entrada
    topic = input("\n📝 Ingresa un tema de investigación (ej. 'Agujeros negros'): ")
    if not topic.strip():
        topic = "Impacto de la IA en Educación"
        print(f"Usando tema por defecto: {topic}")
    
    # Estado inicial (incluyendo los nuevos campos avanzados)
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
    
    # Configuración del Checkpointer (Memoria)
    config = {"configurable": {"thread_id": "sesion_1"}}
    
    print_separator("INICIANDO FLUJO DEL GRAFO")
    
    # 3. Ejecutar el grafo hasta que termine o se interrumpa (HITL)
    for output in graph.stream(initial_state, config=config):
        for node_name, state_update in output.items():
            print(f"\n[Nodo Completado]: {node_name}")
            if "reliability_score" in state_update:
                print(f"  └─ Fiabilidad evaluada: {state_update['reliability_score']}%")
            if "token_cost" in state_update:
                print(f"  └─ Tokens consumidos en paso: {state_update['token_cost']}")

    # 4. Verificamos si el grafo se detuvo por nuestra interrupción manual
    # TODO 9: Obtén el estado del grafo y verifica si el siguiente nodo es 'publisher'.
    # Si es así, pide al usuario aprobación usando `input()`. 
    # Si aprueba, reanuda el grafo.
    # Por ahora, simplemente lo simulamos:
    state = graph.get_state(config)
    pass
    
    print_separator("PANEL DE OBSERVABILIDAD Y GOBERNANZA")
    
    final_state = graph.get_state(config).values
    
    print(f"💰 Costo total estimado (Tokens): {final_state.get('token_cost', 0)}")
    print(f"📊 Fiabilidad final de los datos: {final_state.get('reliability_score', 0)}%")
    print(f"🔄 Intentos de investigación: {final_state.get('revision_retries', 0)}")
    
    print("\n📜 Traza de Decisiones (Decision Log):")
    for log in final_state.get('decision_log', []):
        print(f"  - {log}")
        
    print_separator("RESULTADO DE ACCIÓN (A2A)")
    print(final_state.get("published_result", "Ninguna acción ejecutada."))
    
    print_separator("LANGSMITH")
    print("Recuerda revisar tu dashboard en LangSmith para ver las trazas completas de las LLM Calls.")

if __name__ == "__main__":
    run_lab()
