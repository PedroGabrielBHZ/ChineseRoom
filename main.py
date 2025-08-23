import sys
import argparse
import logging
from chineseroom.conversation_manager import ConversationManager


def main():
    parser = argparse.ArgumentParser(
        description="Query Google's Gemini generative AI model.")
    parser.add_argument(
        '--model', type=str, default="gemini-2.0-flash-lite", help='Gemini model name')
    parser.add_argument('--log', type=str, default="WARNING",
                        help='Logging level (DEBUG, INFO, WARNING, ERROR)')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(
        logging, args.log.upper(), logging.WARNING))
    logger = logging.getLogger("main")

    # Initialize ConversationManager
    manager = ConversationManager()
    conversation_id = manager.start_conversation()

    print("Type 'exit' to end the conversation.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            response = manager.interact(conversation_id, user_input)
            print(f"Gemini: {response}")
        except Exception as e:
            logger.error(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
