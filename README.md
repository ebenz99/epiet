# Epiet

A programming language for the artistically and assembly-language inclined

## VANDYHACKS VI - ART

This was originally a project I took on at Vandyhacks VI for their art theme I'm looking to try to get this controlled for Python version, but with Python 3.8.3 and the pygame version listed in the `requirements.txt` file, this (mostly) works. For a demo, I'd recommend using the IDE to open `demoInput.txt` and running that.

## Differences between Piet and Epiet

Epiet is a language I created borrowing *heavily* from the esoteric programming language Piet, for which no functional interpreters exist anymore (as far as I could find). Given that I had only 36 hours to code this, it isn't nearly as nice as Piet, but I tried to stay true to what I think makes Piet such a great language. Mainly, this is still a visual coding language where instructions are demarcated by differences in color.

One of the main differences are the instruction sets. Epiet's instructions are constructed around the idea that a user's end result is to print a string, and the way they'll want to get there is starting from an int, performing operations to get to the  ASCII equivalent of a target letter for their string, converting to that char, and appending that char to a register they'll use as a buffer to eventually print to stdout.
