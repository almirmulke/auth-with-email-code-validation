class User:
    def __init__(
        self, id, email, password, activation_code, activation_code_expires_at, is_activated=False
    ):
        self.id = id
        self.email = email
        self.password = password
        self.activation_code = activation_code
        self.activation_code_expires_at = activation_code_expires_at
        self.is_activated = is_activated

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.email,
            "activation_code": self.email,
            "activation_code_expires_at": self.email,
            "is_activated": self.email,
        }
