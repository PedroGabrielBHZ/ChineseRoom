import sys
import argparse
import logging
from chineseroom.gemini_client import GeminiClient


def main():
    parser = argparse.ArgumentParser(
        description="Query Google's Gemini generative AI model.")
    parser.add_argument(
        '--model', type=str, default="gemini-2.0-flash-lite", help='Gemini model name')
    parser.add_argument('--log', type=str, default="WARNING",
                        help='Logging level (DEBUG, INFO, WARNING, ERROR)')
    parser.add_argument('prompt', type=str, nargs='*',
                        help='Prompt to send to Gemini')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(
        logging, args.log.upper(), logging.WARNING))
    logger = logging.getLogger("main")

    # Initialize GeminiClient
    client = GeminiClient(model_name=args.model)
    if not args.prompt:
        print("Error: Prompt is required in single question mode.")
        sys.exit(1)
    prompt = " ".join(args.prompt)
    response = client.ask(prompt)
    print(response)
    sys.exit(0)


if __name__ == "__main__":
    main()
