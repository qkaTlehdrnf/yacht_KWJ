import numpy as np

class Yacht():
    def __init__(self):
        self.diceroll()


    def Ones(self):
        try: 
            return self.dice[0]*1
        except KeyError:
            return 0

    def Twos(self):
        try:
            return self.dice[1]*2
        except KeyError:
            return 0

    def Threes(self):
        try:
            return self.dice[2]*3
        except KeyError:
            return 0

    def Fours(self):
        try:
            return self.dice[3]*4
        except KeyError:
            return 0

    def Fives(self):
        try:
            return self.dice[4]*5
        except KeyError:
            return 0

    def Sixes(self):
        try:
            return self.dice[5]*6
        except KeyError:
            return 0


    def Choice(self):
        return self.dice_sum()

    def FofaKind(self):
        if np.any(self.dice)>=4:
            return self.dice_sum()
        else: return 0

    def FullHouse(self):
        if (np.count_nonzero(self.dice)==2 and np.any(self.dice==3)) or len(self.dice)==1:
            return self.dice_sum()
        else: return 0

    def SmallStraight(self):
        for i in range(3):
            if self.dice[i:i+4].all():
                return 15
        return 0

    def LargeStraight(self):
        for i in range(2):
            if self.dice[i:i+5].all():
                return 30
        return 0

    def Yacht(self):
        if np.count_nonzero(self.dice)==1:
            return 50
        else: return 0
    
    def dice_sum(self):
        sum = 0
        for i in range(6):
            sum += self.dice[i]*(i+1) 
        return sum

    def roll(self,fix_array):
        assert (self.dice - fix_array).all()>=0
        self.diceroll(5-sum(fix_array))
        self.dice = fix_array + self.dice
        return self.dice
    
    def diceroll(self,n=5):#5 dices only have 6 eyes
        self.dice = np.zeros(6, int)#six class for dice
        for i in range(n): self.dice[np.random.randint(6)] +=1

    def expect(self, n=None):
        score_board=np.array(
            (self.Ones(),
            self.Twos(),
            self.Threes(),
            self.Fours(),
            self.Fives(),
            self.Sixes(),
            self.Choice(),
            self.FofaKind(),
            self.FullHouse(),
            self.SmallStraight(),
            self.LargeStraight(),
            self.Yacht()))
        if n == None: return score_board 
        else: return score_board[n]

    def show(self):
        expect = self.expect()
        print("dices: ", self.dice)
        print("Ones: ", expect[0])
        print("Twos: ", expect[1])
        print("Threes: ", expect[2])
        print("Fours: ", expect[3])
        print("Fives: ", expect[4])
        print("Sixes: ", expect[5])
        print("Choice: ", expect[6])
        print("4 of a Kind: ", expect[7])
        print("Full House: ", expect[8])
        print("Small Straight: ", expect[9])
        print("Large Straight: ", expect[10])
        print("Yacht: ", expect[11])

class Battle():

    def __init__(self):
        self.yacht = Yacht()
        self.score_board = np.zeros(12,int)
        self.score_selected = np.zeros(12,int)
        self.dice = self.yacht.dice
        self.yacht.roll(np.zeros(6,int))
        self.dice_remain=np.array((2))

    def roll(self, fix=np.zeros(6,int)):
        assert self.dice_remain#make sure dice not roll 3 times
        self.dice = self.yacht.roll(fix)
        self.dice_remain-=1
        return self.dice

    def turn(self, select):
        assert not self.score_selected[select]
        self.score_board[select] = self.yacht.expect(select)
        self.score_selected[select] += 1
        self.dice_remain = np.array((2))
        self.yacht.roll(np.zeros(6,int))
        return self.score_selected, self.total_score()
    
    def total_score(self):
        bonus = 35 if sum(self.score_board[:7])>=63 else 0
        score = sum(self.score_board)
        return bonus + score


if __name__ == '__main__':
    x=Yacht()
    print(x.dice)