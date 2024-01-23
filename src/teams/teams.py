from typing import List

class Teams():

    def __init__(self, teams: List[str]):
        self._teams = teams

    def add(self, team: str) -> None:
        # checks if team is already in array
        if team in self._teams:
            return

        self._teams.append(team)

    def remove(self, team: str) -> None:
        # checks if team is not in array
        if team not in self._teams:
            return

        self._teams.remove(team)

    def getTeams(self):
        return self._teams.copy()

if __name__ == "__main__":
    teams = Teams(["MIN", "MIL"])