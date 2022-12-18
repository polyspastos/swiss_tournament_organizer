import random
import os

# Create a class to represent a player in the tournament
class Player:
    def __init__(self, name, score=0):
        self.name = name
        self.score = score
        self.games_with_white = 0
        self.games_with_black = 0
        self.had_bye = False

# Create a class to represent the tournament
class Tournament:
    def __init__(self):
        self.players = []
        self.pairings = []
        self.previous_pairings = []
        self.rounds_played = 1
        self.number_of_rounds = 0        
        self.bye_player = Player("BYE")

    def add_player(self, player):
        self.players.append(player)

    def enter_results(self):
        # Display the pairings for the current round
        print("Pairings for round {}:".format(self.rounds_played))

        for p1, p2 in self.pairings:
            print("{} vs. {}".format(p1.name, p2.name))
        # Get the results for each match
        for p1, p2 in self.pairings:
            if p1.name == "BYE":  # Check if player has played BYE already
                # The BYE player automatically loses
                p2.score += 1
                p2.games_with_white += 1
                p1.games_with_black += 1
                p2.had_bye = True  # Set player's had_bye attribute to True
            elif p2.name == "BYE":
                # The BYE player automatically loses
                p1.score += 1
                p1.games_with_white += 1
                p2.games_with_black += 1
                p1.had_bye = True  # Set player's had_bye attribute to True            
            else:
                while True:  # Loop until a valid result is entered
                    result = input("Enter result for match between {} and {} (1 for win, 2 for loss, 0 for draw): ".format(p1.name, p2.name))
                    try:
                        result = int(result)
                    except ValueError:
                        print("Invalid result entered, please enter a number.")
                        continue  # Go back to the start of the loop
                    if result == 1:
                        # White (p1) wins
                        p1.score += 1
                        p1.games_with_white += 1
                        p2.games_with_black += 1
                        break  # Break out of loop
                    elif result == 2:
                        # Black (p2) wins
                        p2.score += 1
                        p1.games_with_black += 1
                        p2.games_with_white += 1
                        break  # Break out of loop
                    elif result == 0:
                        # Draw
                        p1.score += 0.5
                        p2.score += 0.5
                        p1.games_with_white += 1
                        p2.games_with_black += 1
                        break  # Break out of loop
                    else:
                        print("Invalid result entered, please try again.")

        # Generate a unique filename in the format "tourXXX"
        file_index = 1
        while True:
            filename = "tour{:03d}.txt".format(file_index)
            if not os.path.exists(filename):
                break
            file_index += 1

        self.previous_pairings += self.pairings
        self.save_state(filename)

    def display_standings(self):
      # Sort the players by score, then by number of games with white
      self.players = [player for player in self.players if player.name != "BYE"]
      self.players.sort(key=lambda x: (-x.score, x.games_with_white))
      print("Standings:")
      for i, player in enumerate(self.players):
        if player.had_bye:
          print("{}. {} ({} points) - received a bye".format(i+1, player.name, player.score))
        else:
          print("{}. {} ({} points)".format(i+1, player.name, player.score))

    def load_state(self, filename):
        with open(filename, "r") as f:
            # Load the number of rounds
            self.number_of_rounds = int(f.readline().strip())
            # Load the current round
            self.rounds_played = int(f.readline().strip())
            # Load the players
            for line in f:
                name, score, games_with_white, games_with_black = line.strip().split(",")
                player = Player(name, float(score), int(games_with_white), int(games_with_black))
                self.add_player(player)
            # Load the pairings
            self.pairings = []
            for line in f:
                p1_name, p2_name = line.strip().split(",")
                p1 = next(p for p in self.players if p.name == p1_name)
                p2 = next(p for p in self.players if p.name == p2_name)
                self.pairings.append((p1, p2))

    def save_state(self, filename):
        # Save the current tournament state to the given file
        with open(filename, "w") as file:
            file.write(str(self.number_of_rounds) + "\n")
            file.write(str(self.rounds_played) + "\n")
            for player in self.players:
                file.write("{},{},{},{}\n".format(player.name, player.score, player.games_with_white, player.games_with_black))

    def pair_players(self):
      # Check if there is an odd number of players
      if len(self.players) % 2 == 1:
        # Add the BYE player to the list of players
        self.players.append(Player("BYE"))

      # Create a dictionary to store the player scores
      scores = {}
      for player in self.players:
        scores[player] = player.score

      # Sort the players by score in descending order
      sorted_players = sorted(self.players, key=lambda x: x.score, reverse=True)

      # Initialize the pairings list
      self.pairings = []

      # Pair the players based on their scores
      while len(sorted_players) > 0:
        # Find the player with the highest score
        top_player = sorted_players.pop(0)

        # If the top player is the BYE player, assign the BYE to the player with the lowest score
        if top_player.name == "BYE":
          if len(sorted_players) > 0:
            bottom_player = sorted_players.pop()
            self.pairings.append((bottom_player, top_player))
        else:
          # Find the player with the closest score to the top player
          closest_score = float("inf")
          closest_player = None
          for player in sorted_players:
            score_difference = abs(scores[top_player] - scores[player])
            if score_difference < closest_score:
              closest_score = score_difference
              closest_player = player

          # Pair the top player with the player with the closest score, if one was found
          if closest_player is not None:
            self.pairings.append((top_player, closest_player))
            sorted_players.remove(closest_player)

      # Save the pairings in the self.previous_pairings attribute
      self.previous_pairings.extend(self.pairings)

    # Main function to run the tournament
    def run_tournament(self):
        # Ask the user if they want to load the tournament state from a file
        # load_state = input("Do you want to load the tournament state from a file (Y/N)? ")
        # if load_state.upper() == "Y":
        if 1 == 2:
            pass
        #     filename = input("Enter the name of the file to load: ")
        #     self.load_state(filename)
        else:
            # Get the names of the players from the user
            print("Enter the names of the players, one per line. When finished, type 'done'.")
            name = input("Enter player name: ")
            while name.lower() != "done":
                player = Player(name)
                self.add_player(player)
                name = input("Enter player name: ")

            # Get the number of rounds from the user
            self.number_of_rounds = int(input("Enter the number of rounds: "))
            # Randomly pair the players for the first round
            random.shuffle(self.players)
            if len(self.players) % 2 == 1:
                # If there is an odd number of players, add a bye player
                self.players.append(self.bye_player)

            self.pair_players()
            self.enter_results()
            self.display_standings()


            # self.pairings = [(p1, p2) for p1, p2 in zip(self.players[::2], self.players[1::2])]
            self.rounds_played += 1

            # Generate a unique filename in the format "tourXXX"
            file_index = 1
            while True:
                filename = "tour{:03d}.txt".format(file_index)
                if not os.path.exists(filename):
                    break
                file_index += 1

            self.save_state(filename)

        # Run the rounds of the tournament
        for round_num in range(1, self.number_of_rounds):
            self.pair_players()
            self.enter_results()
            self.display_standings()
            self.rounds_played += 1
            
            file_index += 1
            filename = "tour{:03d}.txt".format(file_index)
            self.save_state(filename)

# Run the tournament
my_tour = Tournament()
my_tour.run_tournament()
