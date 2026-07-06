# Laboratorio S2: LangGraph Avanzado

**Prerequisito:** Haber completado o revisado el laboratorio S1.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Aecetp/taller-1-sesion-1?devcontainer_path=.devcontainer%2Fdevcontainer.json)

---

## 🎯 ¿Qué añadimos sobre S1?

El mismo grafo de investigación de S1, ahora con **cuatro capacidades de producción**:

```
[researcher] → [reviewer] → condicional → [writer] ⏸️ PAUSA HITL ⏸️ → [publisher] → END
                                                                              ↓
                                                                      Panel de Governance
```

| Capacidad nueva | ¿Para qué sirve? |
|:---|:---|
| **Checkpointing** | Guarda el estado en cada paso — si falla, retoma donde quedó |
| **HITL** | El humano aprueba antes de la publicación |
| **A2A** | El publisher recibe solo un payload estructurado, no todo el estado |
| **Governance** | Token cost y decision log acumulados por nodo |

---

## 📂 Estructura del Proyecto

```text
s2-langgraph-avanzado/
├── main.py       # Dos fases: flujo hasta HITL, luego reanuda si apruebas.
├── graph.py      # Misma estructura de S1 + publisher + checkpointing + HITL.
├── agents.py     # Misma lógica de S1 + call_publisher_agent.
├── state.py      # Estado ampliado con token_cost, decision_log, publisher_payload.
└── utils/
    └── llm.py    # Sin cambios.
```

> **La misma regla de S1:**
> - `agents.py` → personalidad del agente (prompts).
> - `graph.py` → nodos, aristas y orquestación.

---

## ⚙️ Configuración

```bash
cp .env.example .env   # Configura tu GOOGLE_API_KEY
uv run main.py
```

---

## 📝 Retos del Laboratorio

### Reto 1 — Estado ampliado (`state.py`)
Añade los nuevos campos al `GraphState`. Los acumulables usan el mismo patrón de S1.
> Campos nuevos: `publisher_payload`, `published_result`, `token_cost`, `decision_log`

### Reto 2 — Publisher y Observabilidad (`graph.py`)
Completa el `publisher_node` para que lea el `publisher_payload` y llame a `call_publisher_agent`. Además, asegúrate de que los nodos existentes retornen `token_cost` y `decision_log`.

### Reto 3 — Checkpointing e HITL (`graph.py` + `main.py`)
En `create_graph()`, compila el grafo con `MemorySaver` e `interrupt_before=["publisher"]`. En `main.py`, gestiona la pausa: muestra el borrador, pide aprobación y reanuda pasando `None` al `stream`.
