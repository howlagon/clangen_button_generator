# clangen_button_generator
### A prototype pygame button generation system for [Thlumyn/clangen](https://github.com/Thlumyn/clangen)

#### i am in the process of rewriting this! it will not function as intended, and has unfinished code!!

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
## Usage
```py
from buttons import Button
surface = Button.new(size=(120, 30), 
                     text=":3",
                     hover=False,
                     unavailable=False)
```

## TODO
### High Priority
> - [ ] document, document, document. 
> - [ ] create "hanging board" style buttons
> - [ ] delete unused variables when possible
> - [ ] general optimizations
### Med Priority
> - [ ] comment this awful code, for fucks sake please for the love of god
> - [ ] proper color support, AND reimpliment hover/disabled
> - [ ] custom dangerous buttons?
### And finally,
> - [ ] pep8 standardizing. gross
> - [ ] actually impliment this into the code. 
  - this will be a separate branch