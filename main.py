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
    parser.add_argument('--single', action='store_true',
                        help='Run in single question mode')
    parser.add_argument('prompt', type=str, nargs='*',
                        help='Prompt to send to Gemini')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(
        logging, args.log.upper(), logging.WARNING))
    logger = logging.getLogger("main")

    # Initialize ConversationManager
    manager = ConversationManager()
    conversation_id = manager.start_conversation()

    # Single question mode
    if args.single:
        if not args.prompt:
            print("Error: Prompt is required in single question mode.")
            sys.exit(1)
        prompt = " ".join(args.prompt)
        response = manager.interact(conversation_id, prompt)
        print(response)
        sys.exit(0)

    # Conversation mode
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
