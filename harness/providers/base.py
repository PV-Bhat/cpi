
class ProviderBase:
    def complete(self, prompt: str) -> str:
        raise NotImplementedError
