class SMTPClient:

    @staticmethod
    def send(subject, text, email):

        if not isinstance(subject, str):
            return False

        if not isinstance(text, str):
            return False

        if not isinstance(email, str):
            return False

        if "@" not in email:
            return False

        return True
