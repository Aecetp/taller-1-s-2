from typing import Annotated, TypedDict, List, Dict, Any
import operator

class GraphState(TypedDict):
    """
    Estado centralizado del flujo de trabajo.
    Todos los nodos leen y escriben en esta estructura.

    Recuerda: los campos normales se SOBRESCRIBEN.
              los campos con Annotated se ACUMULAN.
    """
    # ── Campos heredados de S1 (ya conocidos) ──────────────
    topic:             str
    sources:           Annotated[List[str], operator.add]
    research_notes:    str
    reliability_score: int
    revision_retries:  int
    final_draft:       str
    is_aborted:        bool

    # ── NUEVOS: Comunicación A2A ────────────────────────────
    # TODO 1: Define 'publisher_payload' como Dict[str, Any]
    #         (el writer le pasa el contenido al publisher de forma estructurada)
    publisher_payload: ...

    # TODO 2: Define 'published_result' como str
    #         (el resultado que devuelve el publisher)
    published_result: ...

    # ── NUEVOS: Observabilidad y Governance ─────────────────
    # TODO 3: Define 'token_cost' como entero ACUMULABLE
    #         Pista: Annotated[int, operator.add]
    #         ¿Por qué acumulable? Porque cada nodo suma sus propios tokens.
    token_cost: ...

    # TODO 4: Define 'decision_log' como lista de strings ACUMULABLE
    #         Pista: Annotated[List[str], operator.add]
    decision_log: ...
