       ▜ ▗    ▐     ▜▜  ▐        ▌     ▗       ▜                 ▐            ▐
    ▞▀▖▐ ▄ ▛▀▖▜▀ ▞▀▖▐▐  ▜▀ ▞▀▖▞▀▖▛▀▖▛▀▖▄ ▞▀▖▝▀▖▐  ▝▀▖▞▀▘▞▀▘▞▀▖▞▀▘▜▀ ▛▚▀▖▞▀▖▛▀▖▜▀
    ▌ ▖▐ ▐ ▌ ▌▐ ▖▛▀ ▐▐  ▐ ▖▛▀ ▌ ▖▌ ▌▌ ▌▐ ▌ ▖▞▀▌▐  ▞▀▌▝▀▖▝▀▖▛▀ ▝▀▖▐ ▖▌▐ ▌▛▀ ▌ ▌▐ ▖
    ▝▀  ▘▀▘▘ ▘ ▀ ▝▀▘ ▘▘  ▀ ▝▀▘▝▀ ▘ ▘▘ ▘▀▘▝▀ ▝▀▘ ▘ ▝▀▘▀▀ ▀▀ ▝▀▘▀▀  ▀ ▘▝ ▘▝▀▘▘ ▘ ▀

> **SDE - 1** clintell's technical assestment

---

### 1. Descripción general de la prueba

El presente repositorio pretende ser una propuesta de solución para el problema expuesto por Clintell.
El objetivo de la prueba era implementar un sistema de agentes conversacionales que
a partir de las entradas del usuario extraigan información de interés y la redirijan a endpoints simulados.

---

### 2. Diseño del sistema y decisiones técnicas

![Diagrama de clases del sistema](./imgs/system-classes-design.png)

El sistema implementa una arquitectura organizada en 4 capas: Modelos, Agentes, Validación y Servicios. El diseño propuesto prioriza la extensibilidad mediante abstracción y el bajo acoplamiento.

#### Decisiones técnicas relevantes:

1. **Patrón Template Method**: la clase abstracta `BaseAgent` define el flujo de gestión de turnos (`handle_turn()`) y las instancias `DebtAgent` y `AssistantAgent` implementan la especialización específica para la validación, normalización (`_validate_normalize()`) y el procesamiento (`_process_action()`) de la información que les llega. Esto garantiza la consistecia en su ciclo de vida y la posibilidad de añadir nuevos agentes sin duplicidad de código (Principio Apertura/Cierre).

2. **Prevención de Información Duplicada**: Cada Agente tiene un atributo `_action_history: set()` que guarda un registro de entradas validadas con `frozenset()` para prevenir el procesamiento de información duplicada.

3. **Externalización de la Validación**: para desacoplar la validación de la información que les llega a los agentes se han implementado Schemas de validación con pydantic (Principio de Responsabilidad Única).

4. **Inyección de Dependencias**: los agentes reciben `ConversationModel`, `ParserModel` y `HttpClient` por constructor, lo que facilita el testing mediante mocks y reduce el acoplamiento entre capas.

---

### 3. Estructura del proyecto

```
clintell-technical-assessment/
├── src/
│   ├── base.py                    # Clase abstracta BaseAgent
│   ├── agents/
│   │   ├── debt.py                # Clase DebtAgent
│   │   └── assistant.py           # Clase AssistantAgent
│   ├── models/
│   │   ├── schemas.py             # Schemas Pydantic
│   │   └── mocks.py               # Mocks ConversationModel/ParserModel
│   └── services/
│       └── http_client.py         # Mock Cliente HTTP
├── tests/
│   ├── unit/                      # Tests unitarios
│   │   ├── test_schemas.py
│   │   ├── test_http_client.py
│   │   └── test_mocks.py
│   ├── integration/               # Tests de integración
│   │   ├── test_debt_flow.py
│   │   └── test_assistant_flow.py
│   └── conftest.py
├── main.py                        # Demo ejecutable (gameloop simulado)
├── conftest.py                    # Configuración ruta base para los Tests
├── requirements.txt               # Dependencias proyecto
├── .env.example
├── .gitignore
└── README.md
```

---

### 4. Ejecutar demo local

**Requisitos**: Python 3.10+ (versión utilizada para el desarrollo: python 3.12)

**Instalación y ejecución**:

```
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Ejecutar demo
python main.py
```

**Qué hace la demo**:

La demo ejecuta dos escenarios simulados:

- El primero es una simulación de la ejecución del agente `DebtAgent`, en el que se "reproduce" una conversación entre usuario-agente y se van logeando
  los mensajes del usuario y el contexto interno (información parseada) del agente.

- El segundo es la misma dinamica de simulación que se acaba de comentar pero para el agente `AssistantAgent`.

**Output esperado:**

```
INFO - Starting assistant game loop (AssistantAgent demo)
INFO - Turno 1 (USER input): Tengo un problema con una de mis factoras de enero
INFO - POST request to: https://api.ringr.assistance/v1/request
{'Authorization': 'Bearer ringr_test_token_9f3a2c1d', 'Content-Type': 'application/json', 'request': 'revisión de factura de enero'}
INFO - Turno 1 (AGENT internal context): {'request': 'revisión de factura de enero'}
```

---

### 5. Tests

El proyecto incluye 27 tests distribuidos en tests unitarios y tests de integración:

**Ejecutar tests:**

```
pytest -v
```

**Cobertura de los tests:**

#### Tests Unitarios (17 casos de prueba)

| ID   | Tipo de Test       | Nombre del Test                                                  |
| ---- | ------------------ | ---------------------------------------------------------------- |
| U-01 | Happy Path Testing | test_debt_agent_schema_valid_commitment                          |
| U-02 | Boundary Testing   | test_debt_agent_schema_invalid_commitment                        |
| U-03 | Exception Testing  | test_debt_agent_schema_past_date_raises_error                    |
| U-04 | Boundary Testing   | test_debt_agent_schema_today_date_raises_error                   |
| U-05 | Exception Testing  | test_debt_agent_schema_negative_amount_raises_error              |
| U-06 | Boundary Testing   | test_debt_agent_schema_0_amount_raises_error                     |
| U-07 | Exception Testing  | test_debt_agent_schema_invalid_date_format_raises_error          |
| U-08 | Happy Path Testing | test_assistant_agent_schema_valid_request                        |
| U-09 | Boundary Testing   | test_assistant_agent_schema_invalid_request                      |
| U-10 | Boundary Testing   | test_assistant_agent_schema_1000_characters_request_is_valid     |
| U-11 | Exception Testing  | test_assistant_agent_schema_1001_characters_request_raises_error |
| U-12 | Happy Path Testing | test_conversation_model_valid_responses                          |
| U-13 | Edge Case Testing  | test_conversation_model_end_of_conversation                      |
| U-14 | Happy Path Testing | test_parser_model_valid_data_sequence                            |
| U-15 | Edge Case Testing  | test_parser_model_empty_data_sequence                            |
| U-16 | Happy Path Testing | test_http_client_with_valid_token                                |
| U-17 | Exception Testing  | test_http_client_with_no_token_raises_error                      |

#### Tests de Integración (10 casos de prueba)

| ID   | Tipo de Test       | Nombre del Test                                        |
| ---- | ------------------ | ------------------------------------------------------ |
| I-01 | Happy Path Testing | test_debt_agent_registers_debt_with_valid_data         |
| I-02 | Behavioral Testing | test_debt_agent_skips_debt_with_no_data                |
| I-03 | Exception Testing  | test_debt_agent_skips_action_with_invalid_date         |
| I-04 | Exception Testing  | test_debt_agent_skips_action_with_invalid_amount       |
| I-05 | Behavioral Testing | test_debt_agent_prevents_duplicate_commitments         |
| I-06 | Behavioral Testing | test_debt_agent_multiple_different_commitments         |
| I-07 | Happy Path Testing | test_assistant_agent_registers_request_with_valid_data |
| I-08 | Behavioral Testing | test_assistant_agent_skips_action_with_no_request      |
| I-09 | Behavioral Testing | test_assistant_agent_prevents_duplicate_requests       |
| I-10 | Behavioral Testing | test_assistant_agent_multiple_different_requests       |
