

class Instabot():
    def setCredentials(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def __init__(self, username:str=None, password:str=None):
        self.setCredentials(username, password)
        self.bot = None

    def login(self, cacheFilePath:str=None) -> None:

        # Login in with saved cache (preferable)
        if cacheFilePath != None:
            print("Logining in using cache")
            return

        if None in [self.username, self.password]:
            raise ValueError("Cache, Username, and or Password is not given")

        print(f"Logining with credientials: {self.username} - {self.password}")

        # Create new cache
        
        self.bot = "Something"

if __name__ == "__main__":
    bot = Instabot("Skilful", "Jester98")

    bot.login()