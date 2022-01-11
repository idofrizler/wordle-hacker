# wordle-hacker

## Preface
This repo contains a [Wordle](https://www.powerlanguage.co.uk/wordle/) simulator and a bot that plays the game.
Latest bot used entropy to calculate most optimal guess each turn. You can benchmark it, or use it to interactively play the game.

## Usage

### Benchmark
To benchmark the bot on all 2315 words in the Wordle dictionary, simply run the following command: \
`python WordleSimulator.py --benchmark`

Result should look something like:
>Total games: 2315 \
Successful games: 2315 \
Average turns when successful: 3.544708423326134

### Interactive
For using the bot to play Wordle, run the following command: \
`python WordleSimulator.py --interactive`

Then, simply take its printed guess each turn, and write back the pattern that was received from the online game.
The pattern should be five characters (all caps), comprised of 'V','?' or 'X'.
> V - Green square \
? - Yellow square \
X - Grey square


## Further reading
[Blog post](https://ido-frizler.medium.com/the-science-behind-wordle-67c8112ed0d1) about "The Science behind Wordle"
