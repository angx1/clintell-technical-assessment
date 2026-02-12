from src.models.mocks import ConversationModel, ParserModel
from src.agents.assistant import AssistantAgent
from src.agents.debt import DebtAgent
from src.servicies.http_client import HttpClient
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_debt_game_loop():
    logging.info("Starting debt game loop (DebtAgent demo)")

    user_responses = [
        "Hola", 
        "Pagaré 150.50 euros el 2026-12-01", 
        "Sí confirmo que pagaré eso"
    ]
    parsed_sequence = [
        {"commitment_date": None, "commitment_amount": None},
        {"commitment_date": "2026-12-01", "commitment_amount": 150.50},
        {"commitment_date": "2026-12-01", "commitment_amount": 150.50}
    ]

    conversation_model_mock = ConversationModel(user_responses)
    parser_model_mock = ParserModel(parsed_sequence)
    http_client_mock = HttpClient()

    agent = DebtAgent(conversation_model_mock, parser_model_mock, http_client_mock)

    for i in range(len(user_responses)):
        logging.info(f"Turno {i+1} (USER input): {user_responses[i]}")
        agent_replay = agent.handle_turn()
        logging.info(f"Turno {i+1} (AGENT inetrnal context): {agent_replay}")


def run_assistant_game_loop():
    logging.info("\n \n Starting assistant game loop (AssistantAgent demo)")
    
    user_responses = ["Tengo un problema con una de mis factoras de enero"]
    parsed_sequence = [{"request": "revisión de factura de enero"}]

    conversation_model_mock = ConversationModel(user_responses)
    parser_model_mock = ParserModel(parsed_sequence)
    http_client_mock = HttpClient()

    agent = AssistantAgent(conversation_model_mock, parser_model_mock, http_client_mock)

    for i in range(len(user_responses)):
        logging.info(f"Turno {i+1} (USER input): {user_responses[i]}")
        agent_replay = agent.handle_turn()
        logging.info(f"Turno {i+1} (AGENT internal context): {agent_replay}")


if __name__ == "__main__":
    try:
        run_debt_game_loop()
        run_assistant_game_loop()
        
    except KeyboardInterrupt:
        logging.info("Demo interrumpida")

    except Exception as e:
        logging.error(f"{e}")