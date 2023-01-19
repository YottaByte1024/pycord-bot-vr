# Pycord Bot - VR

This bot was developed for personal non-commercial use.

It has a few simple features that will enhance the experience of interacting with Discord servers.

The following project was taken as the basis and structure of the bot:
[Toolkit](https://github.com/Dorukyum/Toolkit)

## Running the bot

### Installing and activating the virtual environment

For Linux:

```sh
python -m venv venv
```

```sh
source venv/bin/activate
```

### Installing requirements

```sh 
pip install -r requirements.txt
```

### Configuring the bot

config.py example:
```python
config = {
    'debug_guilds': [980510954733, 5423978095493],
    'owner_id': 1092357754334
}
```

### Starting the bot

For Linux:

```sh
python main.py
```

### Stopping the bot

For Linux:

> To stop the bot, press Ctrl+C twice
