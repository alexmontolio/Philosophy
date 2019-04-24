# The Wikipedia Philosophy Game

A strange occurance where articles lead to the Philosophy article on Wikipedia, implemented in a non-brute force fashion.

Current runtime: Python 3.6+

## Installation

To install this solution, clone this repo.

`$ git clone git@github.com:alexmontolio/Philosophy.git`

Then from the `wikipedia-game` folder, run a pip install of the requirements.

`$ pip install -r requirements.txt`


## Running

The Wikipedia game solution can be run as either a module:

`$ python -m wikipedia_game.game`

Or from the command line inside the `wikipedia-game` directory:

```
>>> from wikipedia_game.game import main
>>> result = main()
```