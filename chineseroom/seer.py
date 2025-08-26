from chineseroom import gemini_client


class Seer():
    def __init__(self):
        self.clients = {}
        self._instantiate_gemini()

    def _instantiate_gemini(self):
        self.clients["gemini"] = gemini_client.GeminiClient()

    def _choose_client(self):
        # TODO: implement esoteric client choosing logic
        return self.clients["gemini"]

    def ask(self, question):
        client = self._choose_client()
        answer = client.ask(question)
        return answer
