#%% setup and class defs
import pickle
import os

def loadPortfolio(path: str):
        with open(path, 'rb') as f:
            portfolio = pickle.load(f)
        return portfolio

class Symbol:

    def __init__(self, 
                symbol: str,
                shares: float = 0.,
                basis: float = 0.,
                premiums: float = 0.,
                history: dict[str:list] = {
                    'Event': [],
                    'Instrument': [],
                    'Strike': [],
                    'Quantity': [],
                    'Price': [],
                    'Total': []
                }
            ):
        self.symbol = symbol.upper()
        self.shares = shares
        self.basis = basis
        self.premiums = premiums
        self.net()
        self.history = history

    def __repr__(self):
        return f'{self.shares:.2f} shares of {self.symbol} at ${self.perShare} per share. TVL: {self.premiums + self.basis}'
    
    def net(self):
        self.netBasis = self.basis - self.premiums
        self.perShare = round((self.netBasis / self.shares) + .00001, 2) if self.shares > 0 else 0

    def updateHistory(self, event: str, instrument: str, strike: float, quantity: float, price: float, total: float):
        self.history['Event'].append(event)
        self.history['Instrument'].append(instrument)
        self.history['Strike'].append(strike)
        self.history['Quantity'].append(quantity)
        self.history['Price'].append(price)
        self.history['Total'].append(total)
    
    def equity(self, shares: float, price: float, buy: bool = True):
        if buy:
            self.shares += shares
            self.basis += price * shares
            self.updateHistory('BUY', 'SHARES', None, shares, price, -shares * price)
        else:
            self.shares -= shares
            self.basis -= price * shares
            self.updateHistory('SELL', 'SHARES', None, shares, price, shares * price)
        self.net()

    def options(self, contracts: int, strike: float, price: float, sell: bool = True, call: bool = True):
        if sell:
            self.premiums += contracts * price * 100
            self.updateHistory('SELL', 'CALL' if call else 'PUT', strike, contracts, price, contracts * price * 100)
        else:
            self.premiums -= contracts * price * 100
            self.updateHistory('BUY', 'CALL' if call else 'PUT', strike, contracts, price, -contracts * price * 100)
        self.net()


class Portfolio:

    def __init__(self, name: str = 'Default', symbols: dict[str:Symbol] = {}):
        self.name = name
        self.symbols = symbols

    def __repr__(self):
        return f'Portfolio {self.name}:\n' + '\n'.join([symbol for symbol in self.symbols.keys()])
    
    def addSymbol(self, symbol: Symbol):
        self.symbols[symbol.symbol] = symbol

    def removeSymbol(self, symbol: Symbol):
        if symbol in self.symbols:
            self.symbols.pop(symbol.symbol)

    def pprint(self):
        print(f'{self.name} contains:\n')
        for symbol in self.symbols:
            print(f'\t{self.symbols[symbol]}')

    def dump(self, path: str = None):
        if path is None: path = f'{os.path.realpath(__file__)}\\{self.name}.pickle'
        with open(path, 'wb') as f:
            pickle.dump(self, f)

#%% preloading my stuff
if False:
    # poet
    poet = Symbol('POET')
    poet.equity(100, 5.72, buy=True)
    poet.options(1, 6, .40, sell=True, call=True)
    poet.options(1, 7, .72, sell=True, call=False)
    poet.equity(100, 7, buy=True)
    poet.equity(1, 4.84, buy=True)
    poet.options(1, 8, .08, sell=True, call=True)
    poet.equity(1.658, 8, buy=True)
    poet.options(1, 6, .16, sell=True, call=True)

    # rbrk
    rbrk = Symbol('rbrk')
    rbrk.options(1, 82.5, 7.70, sell=True, call=False)
    rbrk.equity(8, 90.81, buy=True)

    # fubo
    fubo = Symbol('fubo')
    fubo.options(3, 3.5, .11, call=False)
    fubo.equity(9, 3.62)
    fubo.equity(300, 3.5)
    fubo.options(2, 5, .06)
    fubo.options(1, 5, .01)
    fubo.options(2, 5, .15, sell=False)
    fubo.options(2, 5.5, .09)
    fubo.options(1, 6, .07)
    fubo.equity(2.381, 3.55)
    fubo.options(3, 5, .04)
    fubo.equity(1.455, 3.44)
    fubo.options(3, 5, .03)

    
    # vale
    vale = Symbol('vale')
    vale.options(3, 10, .41, call=False)
    vale.equity(12, 10)
    vale.equity(300, 10)
    vale.options(3, 10, .10)
    vale.equity(2.572, 9.71)

    # rgti
    rgti = Symbol('rgti')
    rgti.equity(10, 12.35)
    rgti.options(1, 13, .85, call=False)
    rgti.options(1, 14, .7, call=False)
    rgti.equity(4, 15.52)
    rgti.options(1, 14.5, .63, call=False)
    rgti.equity(2.84, 15.14)
    rgti.options(1, 14.5, .44, call=False)

    # gen
    gen = Symbol('gen')
    gen.options(2, 29, .75, call=False)
    gen.equity(5, 29.89)
    gen.options(2, 28, .09, call=False)
    gen.equity(.54, 31.45)

    # tenb
    tenb = Symbol('tenb')
    tenb.options(1, 34, 2.5, call=False)
    tenb.equity(8, 32.82)
    tenb.equity(100, 34)
    tenb.options(1, 34, .1)
    tenb.equity(.326, 29.18)

    # mrvl
    mrvl = Symbol('mrvl')
    mrvl.options(1, 62.5, 2.82, call=False)
    mrvl.equity(3, 72.43)

    # intc

    # hut
    hut = Symbol('hut')
    hut.options(1, 20, .71, call=False)
    hut.equity(3, 20.66)

    p = Portfolio('myStuff')
    for s in [poet, rbrk, fubo, vale, rgti, gen, tenb, mrvl, hut]:
        p.addSymbol(s)
    print(p)
    p.dump('P:\\misc\\myStuff.pickle')
