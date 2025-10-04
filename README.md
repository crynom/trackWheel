# Wheel Tracking

## What is the wheel?

### At a high level
The wheel is a popular and simple options strategy for entering and exiting positions on an underlying. Depending on how you position your strikes, this strategy can facilitate entering at dips and exiting at peaks, while earning some additional income. This short description will not fully charaterize the risks of executing this strategy, nor the costs (tax or transactional), only the basic premise. This strategy can be slightly more formally described as _going long theta_.

### Cash Secured Puts
The first step of the wheel involves selling a cash secured put (CSP) on the underlying. This obligates you to purchase the shares at your selected strike price on (or before in the case of American options), at the behest of the buyer. You will be payed a premium for transfering the risk of holding a security from the option buyer to the option seller (you). The objective is to sell these CSPs indefinitely, unless you have a strong bullish view or want to capture a dividend. When they expire, or just before expiration, you can roll forward into the next contract.

Eventually, you will be assigned and the shares will be put to you. This is when the next cycle of the wheel begins.

### Covered Calls
Now that you own 100 shares (or more if you used the premiums to build a long position), you can sell a covered call (CC). A covered call is just a normal call option secured by shares. Selling this contract obligates you to sell your shares at whatever strike price you have sold to the option buyer at the behest of the buyer, just like with the CSP. Now, the objective is to sell these contracts and collect premiums until you are assigned. 

When you are assigned, you go back to selling CSPs.

## Where does the tracker come in?
This tracker allows you to create a portfolio of securities and enter the premiums received or payed for selling or buying options. You can then compute an adjusted cost basis to have a better grasp of what strikes you should sell options at. This is **NOT** connected to any live pricing data, but maybe that is a good feature to consider. A portfolio can be pickled to prevent the need to load the same portfolio repeatedly.
