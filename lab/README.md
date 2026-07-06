# Laboratorio S2 — Versión para Completar

**Prerequisito:** Haber completado S1 o revisar la carpeta padre.  
La solución completa está en `s2-langgraph-avanzado/` (un nivel arriba).

---

## 📂 Qué hay aquí

```text
lab/
├── state.py      # 4 TODOs: campos nuevos para A2A y Governance
├── graph.py      # TODOs: nodos extendidos + publisher_node + HITL/Checkpointing
├── main.py       # TODOs: stream en dos fases + panel de governance
├── agents.py     # ✅ Pre-construido — los 4 agentes ya están listos
└── utils/
    └── llm.py    # ✅ Pre-construido — sin cambios
```

---

## ▶️ Cómo ejecutar

```bash
cd lab
python main.py    # o: uv run main.py
```

---

## 🗺️ Orden de trabajo

1. **`state.py`** — Añadir 4 campos nuevos (10 min)
   - `publisher_payload`, `published_result`, `token_cost`, `decision_log`

2. **`graph.py`** — Sección por sección (45 min)
   - Nodos existentes + `token_cost` / `decision_log` (TODOs 1-9)
   - `publisher_node` — el nodo A2A (TODOs 10-13)
   - Arista condicional (TODO 14)
   - `create_graph` con Checkpointing e HITL (TODOs 15-18)

3. **`main.py`** — Flujo en dos fases (15 min)
   - FASE 1: stream hasta la pausa HITL (TODO A + B)
   - FASE 2: reanudar si el humano aprueba (TODO C)
   - Panel de Governance (TODO D + E)

---

## 🆘 ¿Atascado?

Consulta `SOLUCIONES.py` en esta misma carpeta.
