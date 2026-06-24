from typing import Annotated, TypedDict, List, Dict, Any
import operator

class GraphState(TypedDict):
    """
    Estado centralizado del flujo de trabajo.
    Todos los nodos leen y escriben en esta estructura.
    """
    # Tema de investigación ingresado por el usuario
    topic: str
    
   
    # Pista: Usa Annotated y operator.add.
    sources: Annotated[List[str], operator.add] 
    # Resumen o notas de la investigación
    research_notes: str
    
    # Métrica de fiabilidad calculada por el revisor (0 a 100)
    reliability_score: int
    
    # Conteo de intentos de investigación y revisión (para evitar bucles infinitos)
    revision_retries: int
    
    # Borrador final redactado
    final_draft: str
    
    # Flag para indicar si la investigación fue abortada por baja calidad continua
    is_aborted: bool

    # --- NUEVOS CAMPOS AVANZADOS ---

    # TODO 1: Context Engineering. Define 'publisher_payload' como Dict[str, Any] 
    # y 'published_result' como str para el nodo publicador.
    

    # TODO 2: Governance y Observabilidad. Define 'token_cost' acumulable (Annotated[int, operator.add])
    # y 'decision_log' acumulable (Annotated[List[str], operator.add])
    

