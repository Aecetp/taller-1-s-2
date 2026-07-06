from typing import Annotated, TypedDict, List, Dict, Any
import operator

class GraphState(TypedDict):
    """
    Estado centralizado del flujo de trabajo.
    Todos los nodos leen y escriben en esta estructura.

    Campos acumulables (Annotated + operator.add):
      - sources, token_cost, decision_log
      Se suman en cada paso en lugar de sobrescribirse.
    """
    # Tema de investigación
    topic: str

    # Fuentes encontradas (acumulables entre reintentos)
    sources: Annotated[List[str], operator.add]

    # Notas generadas por el investigador
    research_notes: str

    # Puntaje de fiabilidad del revisor (0-100)
    reliability_score: int

    # Número de rondas de investigación/revisión
    revision_retries: int

    # Borrador final redactado
    final_draft: str

    # Flag para indicar si el proceso fue abortado
    is_aborted: bool

    # --- NUEVOS: Comunicación A2A ---
    # Payload estructurado que el writer le pasa al publisher
    publisher_payload: Dict[str, Any]

    # Resultado devuelto por el agente publicador
    published_result: str

    # --- NUEVOS: Observabilidad y Governance ---
    # Tokens consumidos (acumulables por nodo)
    token_cost: Annotated[int, operator.add]

    # Registro de decisiones de cada nodo (acumulable)
    decision_log: Annotated[List[str], operator.add]
