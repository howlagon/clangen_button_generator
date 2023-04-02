# clangen_button_generator
### A prototype PIL-based button generation system for [Thlumyn/clangen](https://github.com/Thlumyn/clangen)
 
#### watch me suffer in real-time with [trello](https://trello.com/b/g0XJs6PY/clangen)  
please don't look at this code, its genuinely one of the worst things ive written so far. theres nested ternary statements, conditional lists, SO much repetition, and its just ugly to look at.  
thanks, howl <3

right now, documentation will be in [the wiki](https://github.com/howlagon/clangen_button_generator/wiki/) (outdated)

## Requirements
- [Python 3.11.0](https://www.python.org/downloads/release/python-3110/) or [greater](https://www.python.org/downloads/), 3.11.0 was tested  
- [Pip3](https://pip.pypa.io/en/stable/installation/)

## Install / Setup (Windows)
```bat
git clone https://github.com/howlagon/clangen_button_generator/ clangen_button_generator
cd clangen_button_generator
virtualenv -p python3.11 cg_buttons
.\cg_buttons\Scripts\activate
python -m pip install -r requirements.txt
```
### Without VENV (for all of you nerds who hate dependencies)
```bat
git clone https://github.com/howlagon/clangen_button_generator/ clangen_button_generator
cd clangen_button_generator
python -m pip install -r requirements.txt
```

## Example Usage:
```py
from rewrite import NewButtonImage
image = NewButtonImage.new(
                           width = 52, height = 15,
                           unavailable = False,
                           hover = False,
                           rounded_corners = [True, True, True, True],
                           shadows = [True, True, False, False])
image = image.resize((image.width*2, image.height*2), Image.Resampling.NEAREST) # optional, but may(?) save time
image.show()
```

## TODO
### High Priority
> - [ ] document, document, document. 
> - [ ] create "hanging board" style buttons, including custom dangerous buttons (!!)
> - [ ] delete unused variables when possible
> - [ ] general optimizations
### Med Priority
> - [ ] comment this awful code, for fucks sake please for the love of god
> - [ ] proper color support, AND reimpliment hover/disabled
### Low Priority
> - [ ] test height > width
### And finally,
> - [ ] pep8 standardizing. gross
> - [ ] actually impliment this into the code. 
  - this will be a separate branch

special thanks to [luna (ImLvna)](https://github.com/ImLvna) for realizing you could just add a label onto a button, saving me from the hell of generating text
