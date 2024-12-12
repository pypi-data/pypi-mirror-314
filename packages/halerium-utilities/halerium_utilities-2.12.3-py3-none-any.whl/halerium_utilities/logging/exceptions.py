

class DuplicateIdError(RuntimeError):
    pass


class IdNotFoundError(RuntimeError):
    pass


class BoardConnectionError(RuntimeError):
    pass


class BoardUpdateError(RuntimeError):
    pass


class PromptChainError(RuntimeError):
    pass


class CardTypeError(RuntimeError):
    pass
