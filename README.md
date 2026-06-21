## How to use this 
To use this program you will need to download python _keyboard_ library, which requires _sudo_ to run.

## About the game
This in-terminal snake game has support for custom map sizes (from 5×5 to however your screen is big), custom number of apples, custom snake speed, and optional computer opponents (0-4).
To control the snake use arrow keys.
In order to win, be the last standing snake, or become so big, that there is no space left for a new apple to spawn.

## How to use settings
You can save your time writing all the settings all the time by loading them from a file.
In directory _settings_ you may create your own sets of settings or overwrite existing _settings1.json_.
In order for the game to read the settings, they must be located in ./settings/ and their name must be of format _settings?.json_ where _?_ is any single character. The _?_ character is the ID of the settings, which you will need to input when asked at the start of the game.
If your settings do not contain all the settings for the game, you will need to input them via python.
If you do not have any settings saved or chose a set which does not exist, you will need to answer all the questions before the game.
