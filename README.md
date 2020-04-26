# EpiNews

![Discord](https://img.shields.io/badge/Discord-project-brightgreen)
![python](https://img.shields.io/badge/Language-Python-blueviolet)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![EpiNews Banner](src/assets/banner.png)

## About

EpiNews is a discord bot to cast NTTP news on discord.

EpiNews is a project by [gastbob40](https://github.com/gastbob40) and [Baptman21](https://github.com/bat021).

## Requirements

You will need all these elements for the proper working of the project.

- [Python 3.7+](https://www.python.org/downloads/)
- [A Discord Bot Token](https://discordapp.com/developers/applications/)
- [A EpiModo WebSite Token](mailto:quentin.briolant@epita.fr?subject=[GitHub]%20Demande%20de%20Token)

## Getting started

1. **First, you will have to clone the project.**

```shell
git clone https://github.com/gastbob40/epinews
```

2. **Create a `virtual environment`, in order to install dependencies locally.** For more information about virtual environments, [click here](https://docs.python.org/3/library/venv.html).

```shell
python -m venv .venv
```

3. **Activate the virtual environment**

Linux/macOS:

```shell
# Using bash/zsh
source .venv/bin/activate
# Using fish
. .venv/bin/activate.fish
# Using csh/tcsh
source .venv/bin/activate.csh
``` 

Windows:

```
# cmd.exe
.venv\Scripts\activate.bat
# PowerShell
.venv\Scripts\Activate.ps1
```


4. **Finally, install the dependencies**

````shell
pip install -r requirements.txt
````

5. **Configure EpiNews**. This is necessary to use the bot. Check the next section for instructions.

6. **Run `python index.py` to launch EpiNews.** Also make sure that the venv is activated when you launch EpiNews (you should see `venv` to the left of your command prompt).

## Configuration

The `run/config` folder contains all the data of the program configuration.

### tokens.default.yml

This file contain all data about tokens. This file looks like this:

```yaml
epimodo_website_token: ~  # An EpiModo token
discord_token: ~          # A discord bot token
```

You must fill in the file and rename it to `tokens.yml`.


### config_newsgroups.default.default.yml

This file contain all data about the newsgroups. This file looks like this:

```yaml
address: ~          # The address of the newsgroup server
encoding: ~         # The encoding format
delta_time: ~       # Time between update (in second)
stop_on_error: ~    # True if the bot should crash in case of error
date_format: ~      # The date format
```

You must fill in the file and rename it to `tokens.yml`.

For example:
```yaml
address: news.epita.fr
encoding: utf-8
delta_time: 600
stop_on_error: False
date_format: "%Y-%m-%dT%H:%M:%S%z"
```