# Epiet

A programming language for the artistically and assembly-language inclined

## VANDYHACKS VI - ART

This was originally a project I took on at Vandyhacks VI for their art theme I'm looking to try to get this controlled for Python version, but with Python 3.8.3 and the pygame version listed in the `requirements.txt` file, this should work. For a demo, I'd recommend using the IDE to open `demoInput.txt` and running that.

## How to use (PLEASE READ)

First and foremost, _programs made in the editor need to be saved before the can be run_. Now that that's out of the way, you can open the editor by running the `main.py` file in this repository. For notes about how to code in the language, check out the sections below.

## Differences between Piet and Epiet

Epiet is a language I created borrowing *heavily* from the esoteric programming language Piet, for which no functional interpreters exist anymore (as far as I could find). Given that I had only 36 hours to code this, it isn't nearly as nice as Piet, but I tried to stay true to what I think makes Piet such a great language. Mainly, this is still a visual coding language where instructions are demarcated by differences in color.

One of the main differences are the instruction sets. Epiet's instructions are constructed around the idea that a user's end result is to print a string, and the way they'll want to get there is starting from an int, performing operations to get to the  ASCII equivalent of a target letter for their string, converting to that char, and appending that char to a register they'll use as a buffer to eventually print to stdout.

## The language

Looking back, I'm the first to admit the interpretation of this language is far from intuitive. Looking at the `execute` function in `painterModules/interpreterModule.py` is probably the best way to get a clear sense of what's going on with the instructions. There are three registers (r1, r2, and r3), along with one accumulator that is the destination for loaded values. There's also a stringRegister, which can be used as a buffer for printing to the screen.

The direction of interpretation is a `snake` starting from the top left. It reads in the first row from left to right, the second from right to left, the third from left to right, and so on. Programs are saved as txt files with lists of pixel values

### Instruction Types

* __Load__ - This loads the value in the specified register into the accumulator, overwriting whatever was there previously
* __Save__ - This saves whatever value is in the accumulator to the specified register
* __Add__, __Subtract__, and other math operations - *The least intuitive of the bunch*, these take whatever value is currently in the accumulator as the first argument to the specified math operation, and automatically make whatever is in r3 the second argument.
*  __CastTo__ - converts whatever value is in the accumulator to the type specified
* __Print__ - prints the accumulator to the screen
* __StrPrint__ - prints the stringRegister to the screen
* __StrAppend__ - appends a stringified version of the accumulator to the value in the stringRegister
* __strClear__ - clears the stringRegister
* __exit__  - ends the program. Anything you draw in the spaces after the exit statement will not be interpreted

## Issues
* Currently, there's a bug where once a program is run, the remains in `select` mode and must be clicked again to de-select.
