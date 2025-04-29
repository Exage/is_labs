import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

class Player:
    def __init__(self, name):
        self.name = name

    def choose(self):
        raise NotImplementedError("This method should be overridden by subclasses.")

class RandomPlayer(Player):
    def choose(self):
        return random.choice(["turn", "straight"])

class NeuralNetworkPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.model = self.build_model()
        self.history = []
        self.loss_count = 0
        self.wins = 0
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)

    def build_model(self):
        model = nn.Sequential(
            nn.Linear(2, 10),
            nn.ReLU(),
            nn.Linear(10, 2)
        )
        return model

    def choose(self, opponent_choice=None):
        if opponent_choice is None:
            return random.choice(["turn", "straight"])

        input_data = torch.zeros(1, 2)
        
        if len(self.history) > 0:
            input_data[0][0] = 1 if opponent_choice == "turn" else 0
            input_data[0][1] = 1 if self.history[-1] == "turn" else 0

        with torch.no_grad():
            prediction = self.model(input_data)
        choice = "turn" if torch.argmax(prediction) == 0 else "straight"
        self.history.append(choice)
        return choice

    def update_strategy(self):
        if self.loss_count > 0:
            print(f"{self.name} is changing strategy!")
            last_choice = self.history[-1] if self.history else random.choice(["turn", "straight"])
            return "straight" if last_choice == "turn" else "turn"
        return None

    def train(self, X, y):
        self.model.train()
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.LongTensor([y])
        
        self.optimizer.zero_grad()
        output = self.model(X_tensor)

        loss = nn.CrossEntropyLoss()(output, y_tensor)
        loss.backward()
        self.optimizer.step()
        
        if torch.argmax(output) != y_tensor:
            self.loss_count += 1
        else:
            self.loss_count = 0 
            self.wins += 1  

class Game:
    def __init__(self, player1, player2, rounds):
        self.player1 = player1
        self.player2 = player2
        self.rounds = rounds
        self.score1 = 0
        self.score2 = 0
        self.scores1 = []
        self.scores2 = []

    def determine_outcome(self, choice1, choice2):
        if choice1 == "turn" and choice2 == "turn":
            return "Both players turnd, it's a tie."
        elif choice1 == "turn" and choice2 == "straight":
            return f"{self.player2.name} wins!"
        elif choice1 == "straight" and choice2 == "turn":
            return f"{self.player1.name} wins!"
        else:
            return "Both players went straight, it's a disaster!"

    def play(self):
        for round_number in range(1, self.rounds + 1):
            print(f"\nRound {round_number}:")
            choice1 = self.player1.choose()
            choice2 = self.player2.choose(choice1)

            new_choice = self.player2.update_strategy()
            if new_choice:
                choice2 = new_choice

            outcome = self.determine_outcome(choice1, choice2)
            print(f"{self.player1.name} chose {choice1}, {self.player2.name} chose {choice2}.")
            print(outcome)

            if "wins" in outcome:
                if self.player1.name in outcome:
                    self.score1 += 1
                else:
                    self.score2 += 1

            X = np.array([[1 if choice1 == "turn" else 0, 1 if choice2 == "turn" else 0]])
            y = 1 if choice2 == "turn" else 0
            self.player2.train(X, y)

            self.scores1.append(self.score1)
            self.scores2.append(self.score2)

        self.display_final_scores()
        self.plot_scores()

    def display_final_scores(self):
        print("\nFinal Scores:")
        print(f"{self.player1.name}: {self.score1}")
        print(f"{self.player2.name}: {self.score2}")
        if self.score1 > self.score2:
            print(f"{self.player1.name} is the overall winner!")
        elif self.score2 > self.score1:
            print(f"{self.player2.name} is the overall winner!")
        else:
            print("It's an overall tie!")

    def plot_scores(self):
        rounds = range(1, self.rounds + 1)
        plt.plot(rounds, self.scores1, label=self.player1.name, marker='o')
        plt.plot(rounds, self.scores2, label=self.player2.name, marker='o')
        plt.xlabel("Round")
        plt.ylabel("Score")
        plt.title("Scores of Players Over Rounds")
        plt.legend()
        plt.grid()
        plt.show()

player1 = RandomPlayer("Random Player")
player2 = NeuralNetworkPlayer("Neural Player")
rounds = 50

game = Game(player1, player2, rounds)
game.play()

# pip install -r requirements.txt