
# The Boltzmann wealth model, with no space (using the mean-field assumption).

from mesa import Agent, Model
import seaborn as sns
import matplotlib.pyplot as plt

class Human(Agent):
    def __init__(self, model, init_money=0):
        super().__init__(model)
        self.money = init_money
    def sayhi(self):
        print(f"Hi! I'm human {self.unique_id} with ${self.money}.")
    def giveaway(self):
        otherdude = self.model.random.choice(self.model.agents)
        if self.money > 0:
            self.money = self.money - 1
            otherdude.money = otherdude.money + 1
    def step(self):
        #self.sayhi()
        self.giveaway()

class GiveawayDollarBillGameModel(Model):
    def __init__(self, N):
        super().__init__()
        for i in range(N):
            self.agents.add(Human(self, 4))
    def step(self):
        self.display_hist()
        self.agents.shuffle_do("step")
        for a in self.agents:
            a.sayhi()
    def display_hist(self):
        plt.clf()
        sns.histplot([a.money for a in self.agents], discrete=True)
        plt.xlim(0,20)
        plt.ylim(0,120)
        plt.pause(.2)

model = GiveawayDollarBillGameModel(500)
model.run_for(40)
