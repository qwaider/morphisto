# Introduction #

New to Morphisto? Here are some hints to get you started.

# Details #
In our experience, Morphisto newbies may experience some issues getting started. Once you have successfully installed the SFST tools and  downloaded Morphisto, you will need to get ahold of a Morphisto FST automaton. The easiest way to go is to download the Morphisto build provided on the project site. The .a-suffix is meant to automatons in simple format, the .ca-suffix marks SFST automatons in compact format.

Once you have an automaton, you should have a look at one of these three tools that ship with SFST:
  * fst-mor <simple automaton file>
  * fst-infl <simple automaton file>
  * fst-infl2 <compact automaton file>
  * fst-compact <simple automaton file> <output file with .ca-suffix>
fst-mor allows you to "chat" with the automaton: You enter a German word form and receive the result. _Enter_ switches between analysis respectively generation mode.
fst-infl / fst-infl2 allow you to batch-process a text file containing a list of words.
fst-compact can convert from the simple format to the compact one.
There are some PDFs mainly written by Helmut Schmid which come with the SFST package. Whatever the Stuttgart people write about SMOR, will also apply to Morphisto.
We hope that helps you to get started!