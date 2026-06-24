# Guía del Instructor: Live Coding en 2 Horas (LangGraph Avanzado)

Esta guía detalla la estrategia pedagógica para llevar a cabo el taller interactivo de 2 horas. Define qué archivos dejar preconstruidos, qué bloques de código vaciar con comentarios `TODO` para que los estudiantes los completen en vivo, y proporciona los bloques de "Antes" y "Después".

---

## 🗺️ Estrategia Pedagógica: ¿Qué se pre-construye y qué se codifica?

Para optimizar el tiempo de 2 horas y enfocarse en los fundamentos avanzados de LangGraph (Checkpointing, HITL, Context Engineering, Observabilidad y Gobernanza):

1. **Pre-construido (Estático):**
   - La conexión al LLM (`utils/llm.py`) y el archivo `.env.example`.
   - Los System Prompts de los agentes (Researcher, Reviewer, Writer).
   - Lógica de extracción de métricas.
2. **Live-Coding (A completar por los alumnos):**
   - **`state.py`**: Añadir variables avanzadas de payload A2A, logs de decisiones y estimación de costos en tokens (`operator.add`).
   - **`nodes/publisher.py`**: Invocar la acción destructiva (A2A) recibiendo un contexto reducido.
   - **`graph.py`**: Compilar el grafo con `MemorySaver` y utilizar `interrupt_before` para habilitar el Human-in-the-loop.
   - **`main.py`**: Interceptar el estado del grafo pausado, solicitar aprobación en consola y reanudar el flujo (Streaming & Checkpointing).

---

## 📝 Bloques a Completar en Vivo (Paso a Paso)

### Paso 1: Configurar el Estado Avanzado (`state.py`)

**Concepto a explicar:**
- En sistemas multiagente productivos, no pasamos todo el historial al nodo final (Context Engineering). Solo le enviamos lo que necesita (`publisher_payload`).
- Para auditar y gobernar, acumulamos métricas (Tokens) y decisiones usando Reducers (`operator.add`).

#### ❌ Plantilla del Estudiante
```python
    # --- NUEVOS CAMPOS AVANZADOS ---

    # TODO 1: Context Engineering. Define 'publisher_payload' como Dict[str, Any] 
    # y 'published_result' como str para el nodo publicador.
    

    # TODO 2: Governance y Observabilidad. Define 'token_cost' acumulable (Annotated[int, operator.add])
    # y 'decision_log' acumulable (Annotated[List[str], operator.add])
```

#### ✅ Solución
```python
    # Context Engineering: Solo lo estrictamente necesario para el agente publicador
    publisher_payload: Dict[str, Any]

    # Resultado de la acción destructiva simulada
    published_result: str

    # Governance: Registro básico de costo acumulativo (ej. en tokens o créditos)
    token_cost: Annotated[int, operator.add]

    # Observabilidad: Registro simple de las decisiones clave tomadas por los agentes
    decision_log: Annotated[List[str], operator.add]
```

---

### Paso 2: Interoperabilidad A2A y Extracción estructurada (`nodes/publisher.py`)

**Concepto a explicar:**
- El nodo publisher es un agente externo (Agent-to-Agent). Recibe el contenido, pero en lugar de generar texto libre, debe forzar una salida JSON.
- Evaluaremos cómo extraer los tokens y el log de su decisión.

#### ❌ Plantilla del Estudiante
```python
    try:
        # TODO 3: Invocar al LLM, extraer el JSON (limpiando ```json si es necesario)
        # y retornar el diccionario con 'published_result', 'token_cost' y 'decision_log'.
        
        # Simulamos respuesta de error temporalmente para evitar crash:
        return {
            "published_result": "❌ No implementado",
            "token_cost": 0,
            "decision_log": ["[Publisher] Falta implementación"]
        }
    except Exception as e:
```

#### ✅ Solución
```python
    try:
        response = llm.invoke(messages)
        usage = getattr(response, 'usage_metadata', {})
        tokens = usage.get('total_tokens', len(response.content) // 4) if usage else len(response.content) // 4
        
        content_str = response.content
        if isinstance(content_str, list):
            if len(content_str) > 0 and isinstance(content_str[0], dict) and "text" in content_str[0]:
                content_str = content_str[0]["text"]
            else:
                content_str = str(content_str[0]) if content_str else ""
        if not isinstance(content_str, str):
            content_str = str(content_str)
            
        content_str = content_str.strip()
        if content_str.startswith("```json"):
            content_str = content_str[7:-3].strip()
        elif content_str.startswith("```"):
            content_str = content_str[3:-3].strip()
            
        published_data = json.loads(content_str)
        result_msg = f"✅ Artículo publicado en: {published_data.get('url', 'Unknown URL')}"
        
        return {
            "published_result": result_msg,
            "token_cost": tokens,
            "decision_log": [f"[Publisher] Contenido publicado exitosamente. ({tokens} tokens)"]
        }
    except Exception as e:
```

---

### Paso 3: Orquestar el Grafo con Memoria e Interrupciones (`graph.py`)

**Concepto a explicar:**
- Para poder pausar el grafo y esperar aprobación humana, necesitamos *Checkpointers* (persistencia). LangGraph nos da `MemorySaver` en memoria (o SQLiteSaver en DB).
- Usaremos el flag `interrupt_before` para detener la ejecución justo antes de entrar al `publisher`.

#### ❌ Plantilla del Estudiante
```python
    # --- ORQUESTACIÓN AVANZADA ---
    # TODO 6: Instancia el sistema de memoria para guardar checkpoints (Checkpointer)
    memory = None
    
    # TODO 7: Compila el grafo indicando el checkpointer y dónde interrumpir el flujo (Human-in-command)
    # Por ahora compila sin interrupciones para que no falle:
    graph = builder.compile()
    
    return graph
```

#### ✅ Solución
```python
    # --- ORQUESTACIÓN AVANZADA ---
    # Instanciamos el sistema de memoria para guardar checkpoints (Checkpointer)
    memory = MemorySaver()
    
    # TODO 7: Compilar el grafo indicando el checkpointer y dónde interrumpir el flujo (Human-in-command)
    graph = builder.compile(
        checkpointer=memory,
        interrupt_before=["publisher"]
    )
    
    return graph
```

---

### Paso 4: Ejecución en Streaming y HITL (`main.py`)

**Concepto a explicar:**
- Como el grafo tiene memoria, debemos pasar un `thread_id` en el `config`.
- Tras finalizar el primer ciclo de `stream()`, usaremos `graph.get_state(config)` para ver si el grafo está pausado y cuál es el nodo `.next`.
- Una vez pedida la aprobación, pasamos `None` al `stream` para reanudar desde el último checkpoint.

#### ❌ Plantilla del Estudiante
```python
    # 4. Verificamos si el grafo se detuvo por nuestra interrupción manual
    # TODO 9: Obtén el estado del grafo y verifica si el siguiente nodo es 'publisher'.
    # Si es así, pide al usuario aprobación usando `input()`. 
    # Si aprueba, reanuda el grafo.
    # Por ahora, simplemente lo simulamos:
    state = graph.get_state(config)
    pass
```

#### ✅ Solución
```python
    # 4. Verificamos si el grafo se detuvo por nuestra interrupción manual
    state = graph.get_state(config)
    
    if state.next and state.next[0] == "publisher":
        print_separator("HUMAN IN COMMAND (HITL)")
        print("⚠️ ALERTA: El sistema está a punto de ejecutar una acción destructiva (Publicar).")
        print("\nPrevisualización del contexto a publicar:")
        payload = state.values.get("publisher_payload", {})
        print(f"Título: {payload.get('title')}")
        print(f"Longitud del contenido: {len(payload.get('content', ''))} caracteres")
        
        user_input = input("\n¿Apruebas la publicación? (s/n): ")
        if user_input.lower() == 's':
            print("\n✅ Aprobado. Reanudando grafo...")
            # Reanudamos el flujo enviando None (continuar con el estado actual)
            for output in graph.stream(None, config=config):
                for node_name, state_update in output.items():
                    print(f"\n[Nodo Completado]: {node_name}")
        else:
            print("\n❌ Rechazado. Abortando publicación.")
```

---

## ⏱️ Distribución de Tiempo sugerida para el Taller (2 Horas)

| Bloque | Duración | Actividad del Instructor | Actividad del Estudiante |
| :--- | :--- | :--- | :--- |
| **Intro Teórica** | 20 min | Explicar Gobernanza, HITL, Context Engineering y Persistencia en LangGraph. | Atender, hacer preguntas iniciales. |
| **Setup & Explicación** | 10 min | Revisar el pipeline pre-construido y mostrar la arquitectura base. | Configurar claves API locales/Codespaces. |
| **Paso 1: Estado Avanzado** | 15 min | Explicar Reducers para tracking de costos y logs de decisión. | Codificar los nuevos campos en `state.py`. |
| **Paso 2: A2A (Publisher)** | 25 min | Explicar cómo el prompt forza JSON y cómo se extraen las métricas y logs en el código. | Codificar extracción de JSON en `publisher.py`. |
| **Paso 3: Checkpointing** | 20 min | Explicar el objeto MemorySaver y el parámetro `interrupt_before`. | Instanciar MemorySaver en `graph.py` y compilar. |
| **Paso 4: HITL & Panel**| 30 min | Mostrar cómo consultar `state.next` y cómo reanudar un thread pausado con `None`. | Escribir la lógica de interrupción en `main.py` y probar. |
