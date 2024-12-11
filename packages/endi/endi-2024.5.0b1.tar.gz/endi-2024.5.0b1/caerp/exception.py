"""
    enDI specific exception
"""


class BadRequest(Exception):
    """
    Exception raised when the request is invalid (form invalid datas ...)
    """

    message = "La requête est incorrecte"

    def __init__(self, message=None):
        if message:
            self.message = message

    def messages(self):
        """
        Used to fit colander's Invalid exception api
        """
        return [self.message]

    def asdict(self, translate=None):
        return {"erreur": self.message}


class Forbidden(Exception):
    """
    Forbidden exception, used to raise a forbidden action error
    """

    message = "Vous n'êtes pas autorisé à effectuer cette action"


class SignatureError(Forbidden):
    """
    Exception for status modification calls with the wrong signature
    """

    message = "Des informations manquent pour effectuer cette action"
