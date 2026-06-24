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
   cd s1-langgraph-introduccion
   ```
3. Copia el archivo `.env.example` a `.env` y configura tu API Key:
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
/s1-langgraph-introduccion
├── main.py               # 🚀 Ejecuta el grafo y maneja la entrada/salida (Streaming).
├── graph.py              # 🧠 Define la orquestación (StateGraph, nodos y aristas).
├── state.py              # 📦 Estado centralizado (memoria del flujo).
├── nodes/                # 🤖 Carpeta con los "Agentes" (Nodos).
│   ├── researcher.py     # Agente Investigador.
│   ├── reviewer.py       # Agente Revisor (Auditor de alucinaciones).
│   └── writer.py         # Agente Redactor (Formateador final).
├── utils/                
│   └── llm.py            # 🔌 Conexión al modelo (Gemini por defecto, listo para Claude).
└── .env.example          # Plantilla de variables de entorno.
```

---

## 📝 Retos del Laboratorio (A completar en vivo)

*(El instructor guiará el desarrollo de estas secciones paso a paso).*

### Reto 1: Comprendiendo el Estado (`state.py`)
Abre `state.py` y observa el primer `TODO`. Debes definir el campo `sources` asegurándote de que las fuentes de investigación se **acumulen** a lo largo de las iteraciones en lugar de sobrescribirse.
*Pista:* Investiga el uso de `Annotated` combinado con `operator.add`.

### Reto 2: Construir el Flujo de Nodos y Edges (`graph.py`)
Abre `graph.py`. Deberás:
1. Instanciar el `StateGraph`.
2. Registrar los nodos correspondientes.
3. Definir la lógica de la arista condicional `check_reliability` para validar la fiabilidad de la auditoría.
4. Conectar los nodos con aristas estáticas y dinámicas.
5. Compilar el grafo.

### Reto 3: Ejecución y Trazabilidad (`main.py`)
Abre `main.py` y completa el bucle de ejecución de eventos usando `graph.stream(...)`. Esto permitirá imprimir en consola paso a paso el progreso del estado, lo cual te servirá para auditar el comportamiento del sistema y verificar la tasa de éxito de las investigaciones.
