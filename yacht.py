import random
def keyEwrapper(func):
    try:
        return func
    except KeyboardInterrupt:
        return 0

class SimpleNums:
    @keyEwrapper
    def Ones(self):
        return self.dice[0]*1
    @keyEwrapper
    def Twos(self):
        return self.dice[1]*2
    @keyEwrapper
    def Threes(self):
        return self.dice[2]*3
    @keyEwrapper
    def Fours(self):
        return self.dice[3]*4
    @keyEwrapper
    def Fives(self):
        return self.dice[4]*5
    @keyEwrapper
    def Sixes(self):
        return self.dice[5]*6

class ComplexNums:    
    def dice_sum(self):
        sum = 0
        for i in range(6):
            sum += self.dice[i]*(i+1) 
        return sum
    
    def diceroll(self,n=5):#5 dices only have 6 eyes
        self.dice = [0]*6#six values for dice
        for _ in range(n): self.dice[random.randint(0,5)] += 1

    def Choice(self):
        return self.dice_sum()

    def FofaKind(self):
        if 4 in self.dice or 5 in self.dice:
            return self.dice_sum()
        else: return 0

    def FullHouse(self):
        if (3 in self.dice and 2 in self.dice) or 5 in self.dice:
            return self.dice_sum()
        else: return 0

    def SmallStraight(self):
        for i in range(3):
            if 0 not in self.dice[i:i+4]:
                return 15
        return 0

    def LargeStraight(self):
        for i in range(2):
            if 0 not in self.dice[i:i+5]:
                return 30
        return 0

    def Yacht(self):
        if 0 not in self.dice:
            return 50
        else: return 0

class Yacht(SimpleNums, ComplexNums):
    def __init__(self):
        self.diceroll()

    def roll(self,fix_array = None):
        assert not sum(map(lambda x, y: x-y<0, self.dice, fix_array)), f"{sum(map(lambda x, y: x-y<0, self.dice, fix_array))}, {self.dice}, {fix_array}"#0아래의 숫자가 있으면 모두 셈, 그 결과값이 한개라도 있으면 에러
        self.diceroll(5-sum(fix_array))
        self.dice = list(map(lambda x,y:x + y, self.dice, fix_array)) 
        return self.dice

    def expect(self, n=None):
        score_board=[
            self.Ones(),
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
            self.Yacht()]
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

class Battle:
    def __init__(self):
        self.yacht = Yacht()
        self.score_board = [0]*12
        self.score_selected = [0]*12
        self.dice = self.yacht.dice
        self.yacht.roll([0]*6)
        self.dice_remain= 2

    def roll(self, fix=[0]*6):
        assert self.dice_remain#make sure dice not roll 3 times
        self.dice = self.yacht.roll(fix_array = fix)
        self.dice_remain-=1
        return self.dice

    def turn(self, select):
        assert not self.score_selected[select]
        self.score_board[select] = self.yacht.expect(select)
        self.score_selected[select] += 1
        self.dice_remain = 2
        self.yacht.roll([0]*6)
        return self.score_selected, self.total_score()
    
    def total_score(self):
        bonus = 35 if sum(self.score_board[:7])>=63 else 0
        score = sum(self.score_board)
        return bonus + score


if __name__ == '__main__':
    x=Yacht()
    x.show()