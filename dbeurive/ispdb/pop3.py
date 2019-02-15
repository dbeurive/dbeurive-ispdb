from typing import List

class Pop3:

    def __init__(self):
        self.hostname: str = None
        self.port: int = None
        self.socket_type: str = None
        self.username: str = None
        self.authentications: List[str] = None