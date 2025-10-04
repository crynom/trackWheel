#%% setup and class defs
import pickle
import os
from typing import Optional


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
                history: dict[str, list] = {
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
    def updateHistory(self, event: str, instrument: str, strike: Optional[float], quantity: float, price: float, total: float):
        self.history['Event'].append(event)
        self.history['Instrument'].append(instrument)
        self.history['Strike'].append(strike)
        self.history['Quantity'].append(quantity)
        self.history['Price'].append(price)
        self.history['Total'].append(total)
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

    def __init__(self, name: str = 'Default', symbols: dict[str, Symbol] = {}):
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

    def dump(self, path: Optional[str] = None):
        if path is None: path = f'{os.path.realpath(__file__)}\\{self.name}.pickle'
        with open(path, 'wb') as f:
            pickle.dump(self, f)

#%% run in interactive mode and use p as a portfolio
p = Portfolio('Default')