from collections import Counter, defaultdict
"""."""


class Statistics:
    """Main class to handle board game statistics."""

    def __init__(self, filename):
        """Initialize Statistics object and load data from a file."""
        self.games = {}
        self.players = {}
        self.load_file(filename)

    def load_file(self, filename):
        """Load game data from a text file."""
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                game_name, players_str, result_type, results_str = line.split(";")
                players = [p.strip() for p in players_str.split(",")]

                for p in players:
                    if p not in self.players:
                        self.players[p] = Player(p)

                scores = None
                winner = None
                loser = None

                if result_type == "points":
                    score_list = list(map(int, results_str.split(",")))
                    scores = dict(zip(players, score_list))
                    winner = max(scores, key=scores.get)
                    loser = min(scores, key=scores.get)

                elif result_type == "places":
                    results = [r.strip() for r in results_str.split(",")]
                    if results:
                        winner = results[0]
                        loser = results[-1]

                elif result_type == "winner":
                    winner = results_str.strip()

                if game_name not in self.games:
                    self.games[game_name] = Game(game_name, result_type)

                self.games[game_name].add_match(players, winner, loser, scores)

                for p in players:
                    self.players[p].add_game(game_name, p == winner)

    def get(self, path: str):
        """Return requested statistic based on path."""
        parts = path.strip("/").split("/")
        if not parts:
            return None

        if parts[0] == "players":
            return sorted(self.players.keys())

        if parts[0] == "games":
            return sorted(self.games.keys())

        if parts[0] == "total":
            if len(parts) == 1:
                return sum(g.game_play_count() for g in self.games.values())
            else:
                result_type = parts[1]
                return sum(
                    g.game_play_count() for g in self.games.values()
                    if g.match_type == result_type
                )

        if parts[0] == "player":
            name = parts[1]
            player = self.players.get(name)
            if not player:
                return 0 if parts[2] in ("amount", "won") else None
            if parts[2] == "amount":
                return player.player_game_count()
            if parts[2] == "favourite":
                return player.player_favourite_game()
            if parts[2] == "won":
                return player.player_game_wins()

        if parts[0] == "game":
            game_name = parts[1]
            game = self.games.get(game_name)
            if not game:
                if len(parts) > 2 and parts[2] in ("amount", "player-amount"):
                    return 0
                return ""
            if parts[2] == "amount":
                return game.game_play_count()
            if parts[2] == "player-amount":
                return game.game_player_amount()
            if parts[2] == "most-wins":
                return game.game_most_wins()
            if parts[2] == "most-frequent-winner":
                return game.game_most_frequent_winner()
            if parts[2] == "most-losses":
                return game.game_most_losses()
            if parts[2] == "most-frequent-loser":
                return game.game_most_frequent_loser()
            if parts[2] == "record-holder":
                return game.game_record_holder()

        return None


class Player:
    """Class to track individual player statistics."""

    def __init__(self, name):
        """Initialize a Player object."""
        self.name = name
        self.games_played = []
        self.games_won = []

    def add_game(self, game_name, won=False):
        """Add a game to the player's record."""
        self.games_played.append(game_name)
        if won:
            self.games_won.append(game_name)

    def player_game_count(self):
        """Return the total number of games played."""
        return len(self.games_played)

    def player_game_wins(self):
        """Return the total number of games won."""
        return len(self.games_won)

    def player_favourite_game(self):
        """Return the most frequently played game."""
        if not self.games_played:
            return None
        return Counter(self.games_played).most_common(1)[0][0]


class Game:
    """Class to track statistics for a specific game."""

    def __init__(self, name, match_type):
        """Initialize a Game object."""
        self.name = name
        self.match_type = match_type
        self.matches = []

    def add_match(self, players, winner, loser, scores=None):
        """Add a match to the game record."""
        if not players:
            return
        self.matches.append({
            "players": players,
            "winner": winner,
            "loser": loser,
            "scores": scores
        })

    def game_play_count(self):
        """Return total number of matches played."""
        return len(self.matches)

    def game_player_amount(self):
        """Return the most common number of players per match."""
        counts = [len(m["players"]) for m in self.matches if m["players"]]
        if not counts:
            return 0
        return Counter(counts).most_common(1)[0][0]

    def game_most_wins(self):
        """Return player with the most wins."""
        winners = [m["winner"] for m in self.matches if m["winner"]]
        if not winners:
            return ""
        return Counter(winners).most_common(1)[0][0]

    def game_most_frequent_winner(self):
        """Return player with the highest win rate."""
        played = defaultdict(int)
        wins = defaultdict(int)
        for m in self.matches:
            for p in m["players"]:
                played[p] += 1
            if m["winner"]:
                wins[m["winner"]] += 1
        if not wins:
            return ""
        best_player, best_rate = "", 0
        for p in wins:
            rate = wins[p] / played[p] if played[p] else 0
            if rate > best_rate:
                best_rate = rate
                best_player = p
        return best_player

    def game_most_losses(self):
        """Return player with the most losses."""
        if self.match_type not in ("points", "places"):
            return ""
        losers = [m["loser"] for m in self.matches if m["loser"]]
        if not losers:
            return ""
        return Counter(losers).most_common(1)[0][0]

    def game_most_frequent_loser(self):
        """Return player with the highest loss rate."""
        if self.match_type not in ("points", "places"):
            return ""
        played = defaultdict(int)
        losses = defaultdict(int)
        for m in self.matches:
            for p in m["players"]:
                played[p] += 1
            if m["loser"]:
                losses[m["loser"]] += 1
        if not losses:
            return ""
        best_player, best_rate = "", 0
        for p in losses:
            rate = losses[p] / played[p] if played[p] else 0
            if rate > best_rate:
                best_rate = rate
                best_player = p
        return best_player

    def game_record_holder(self):
        """Return player with highest single-match score (points only)."""
        if self.match_type != "points":
            return ""
        best_score = float("-inf")
        holder = ""
        for m in self.matches:
            if not m["scores"]:
                continue
            for player, score in m["scores"].items():
                if score > best_score:
                    best_score = score
                    holder = player
        return holder
