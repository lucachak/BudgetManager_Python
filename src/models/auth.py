class AuthModel:
    def __init__(self):
        # Default credentials - in production, use proper authentication
        self.valid_credentials = {
            'admin': 'admin'
        }
    
    def authenticate(self, username: str, password: str) -> bool:
        return self.valid_credentials.get(username) == password
