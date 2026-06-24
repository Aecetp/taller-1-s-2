# Laboratorio: LangGraph Avanzado y Multiagentes en Producción

¡Bienvenido al laboratorio de **LangGraph Avanzado**! 

En esta sesión, evolucionaremos un sistema multiagente básico hacia una arquitectura robusta orientada a producción, incorporando patrones avanzados de orquestación.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Aecetp/taller-1-s-2?devcontainer_path=.devcontainer%2Fdevcontainer.json)

---

## 🎯 Objetivo del Laboratorio

Implementar un pipeline multiagente end-to-end con **checkpointing**, interoperabilidad **A2A (Agent-to-Agent)** con un agente externo, un panel de **observabilidad/gobernanza** y un nodo de **aprobación humana (HITL)** antes de ejecutar una acción destructiva.

### Conceptos Clave
1. **Orquestación Avanzada:** Checkpointing y recuperación de estado usando `MemorySaver`.
2. **Interoperabilidad A2A:** Comunicación entre agentes heterogéneos mediante payloads estructurados (Context Engineering).
3. **Observabilidad y Gobernanza:** Registro de decisiones (Decision logs) y estimación de costos en tokens.
4. **Human-in-Command (HITL):** Interrupción de grafos (`interrupt_before`) para validación de acciones críticas.

---

## 💻 Configuración del Entorno

### Opción A: En la Nube (GitHub Codespaces)
1. Haz clic en el botón **Open in GitHub Codespaces** de arriba.
2. Espera a que el entorno se configure solo. El sistema instalará automáticamente `uv` y todas las dependencias del proyecto.
3. Copia el archivo `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```
4. Abre el archivo `.env` e ingresa tu `GOOGLE_API_KEY`.
5. Ejecuta el archivo principal:
   ```bash
   uv run main.py
   ```

> [!TIP]
> **Seguridad:** También puedes configurar tu `GOOGLE_API_KEY` directamente en los secretos de tu cuenta de GitHub (Settings -> Secrets and variables -> Codespaces). Si haces esto, la variable de entorno se cargará automáticamente cada vez que crees un Codespace.

### Opción B: Entorno Local (Requiere `uv`)
Este proyecto utiliza `uv` como gestor de paquetes moderno.

1. Asegúrate de tener `uv` instalado ([instrucciones de instalación](https://github.com/astral-sh/uv)):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Clona este repositorio y navega a la carpeta:
   ```bash
   git clone https://github.com/Aecetp/taller-1-s-2.git
   cd taller-1-s-2
   ```
3. Copia el archivo `.env.example` a `.env` y configura tus API Keys (se recomienda LangSmith para observabilidad):
   ```bash
   cp .env.example .env
   ```
4. Ejecuta el archivo principal:
   ```bash
   uv run main.py
   ```

---

## 📂 Arquitectura del Proyecto

El proyecto está diseñado con una arquitectura modular para simular desarrollos en producción:

```text
/taller-1-s-2
├── main.py               # 🚀 Orquestador principal. Controla el flujo, interacciones HITL y logs de gobernanza.
├── graph.py              # 🧠 Define la topología del grafo (StateGraph, persistencia con MemorySaver e interrupciones).
├── state.py              # 📦 Estado centralizado (memoria compartida, logs de auditoría y costo de tokens).
├── nodes/                # 🤖 Agentes especializados (nodos del grafo)
│   ├── researcher.py     # Agente Investigador (generación inicial).
│   ├── reviewer.py       # Agente Revisor (auditoría contra alucinaciones).
│   ├── writer.py         # Agente Redactor (formateo y refinamiento final).
│   └── publisher.py      # Agente Publicador (A2A - simulación de publicación estructurada externa).
├── utils/                
│   └── llm.py            # 🔌 Proveedor del modelo LLM (Gemini por defecto).
└── .env.example          # Plantilla de variables de entorno (API Keys de Gemini y LangSmith).
```

---

## 📝 Retos del Laboratorio (A completar en vivo)

*(El instructor guiará el desarrollo de estas secciones paso a paso).*

### Paso 1: Configurar el Estado Avanzado (`state.py`)
Abre `state.py` y define las variables de estado avanzadas necesarias para:
- **Context Engineering**: Payload estructurado `publisher_payload` que filtra el contexto enviado al publicador.
- **Gobernanza e Inspección**: Reducers (`operator.add`) para acumular de forma transparente `token_cost` y `decision_log` a lo largo del ciclo de vida del flujo.

### Paso 2: Interoperabilidad A2A (`nodes/publisher.py`)
Abre `nodes/publisher.py` y completa la lógica del agente publicador:
- Generación de respuestas estrictamente formateadas en JSON para interactuar de forma segura con APIs externas.
- Extracción de métricas de uso de tokens (`usage_metadata`) y registro de la decisión en el log de auditoría.

### Paso 3: Persistencia y HITL (`graph.py`)
Abre `graph.py` y configura la orquestación avanzada del grafo:
- Instanciación de un checkpointer (`MemorySaver`) para dotar de memoria persistente a la ejecución.
- Configuración de `interrupt_before=["publisher"]` para pausar la ejecución automáticamente antes de una acción de alto impacto.

### Paso 4: Flujo Streaming y Aprobación Humana (`main.py`)
Abre `main.py` y completa la lógica de interacción con el grafo en pausa:
- Consulta de estado (`graph.get_state(config)`) para previsualizar los cambios propuestos al usuario.
- Aceptación/rechazo interactivo en consola y reanudación del grafo pasando `None` para continuar desde el punto de interrupción.
