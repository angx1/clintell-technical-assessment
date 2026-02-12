       ▜ ▗    ▐     ▜▜  ▐        ▌     ▗       ▜                 ▐            ▐
    ▞▀▖▐ ▄ ▛▀▖▜▀ ▞▀▖▐▐  ▜▀ ▞▀▖▞▀▖▛▀▖▛▀▖▄ ▞▀▖▝▀▖▐  ▝▀▖▞▀▘▞▀▘▞▀▖▞▀▘▜▀ ▛▚▀▖▞▀▖▛▀▖▜▀
    ▌ ▖▐ ▐ ▌ ▌▐ ▖▛▀ ▐▐  ▐ ▖▛▀ ▌ ▖▌ ▌▌ ▌▐ ▌ ▖▞▀▌▐  ▞▀▌▝▀▖▝▀▖▛▀ ▝▀▖▐ ▖▌▐ ▌▛▀ ▌ ▌▐ ▖
    ▝▀  ▘▀▘▘ ▘ ▀ ▝▀▘ ▘▘  ▀ ▝▀▘▝▀ ▘ ▘▘ ▘▀▘▝▀ ▝▀▘ ▘ ▝▀▘▀▀ ▀▀ ▝▀▘▀▀  ▀ ▘▝ ▘▝▀▘▘ ▘ ▀

> **SDE - 1** clintell's technical assestment

#### 1. Descripción general de la prueba

#### 2. Diseño del sistema (+ADR's)

#### 3. Ciclo de vida del agente

#### 4. Estructura del proyecto

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

#### 5. Ejecutar demo local

#### 6. Tests ?? no se si incluir esto
