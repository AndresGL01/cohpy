<h1 style="text-align: center">COHPY</h1>
<div style="text-align: center">
<i>An unofficial API Wrapper for Company Of Heroes API</i>

</div>

[![Lint and Tests](https://github.com/AndresGL01/cohpy/actions/workflows/ci.yml/badge.svg)](https://github.com/AndresGL01/cohpy/actions/workflows/ci.yml)
<a href="https://github.com/AndresGL01/cohpy/stargazers"><img src="https://img.shields.io/github/stars/AndresGL01/cohpy" alt="Stars Badge"/></a>


### Tutorial
- [How to install](#How-to-install)
- [Functionalities](#Functionalities)
- [Examples](#Examples)

## How to install
````shell
pip install cohpy
````
Visit [Pypi](https://pypi.org/project/cohpy/) for more info!

## Current API Coverage
- List all leaderboards ✔️
- Show players from a leaderboard ️✔️
- Show match historial from a player ✔️
- Show personal player stats ✔️

## Functionalities

api_client:
: Interface between wrapper and Company of Heroes API 

````python
import cohpy

api_client = cohpy.get_api_client()
````

api_client.leaderboards():
: Get all leaderboards available from the COH API

- Parameters:
  - remove_server_status (optional): **Default=True** Remove from the response the server status (redundant).
You can show it setting this param to **False**

````python
import cohpy

api_client = cohpy.get_api_client()

api_client.leaderboards()
````

api_client.leaderboards():
: Get all leaderboards available from the COH API

- Parameters:
  - leaderboard_id (mandatory): Leaderboard identifier extracted from leaderboards() function. You can use raw ints like 2130329 or
Code class that wraps more used leaderboards
  - count (optional): **Default=200** How many players will be showed in the response. From 1 to 200.
  - sort_type (optional): **Default=ELO** Set the order of the leaderboard based on wins or elo. You can use ints like 0 (ELO) or 1 (WINS). Also you can use SortType wrapper
  - start (optional): **Default=1** Sets the position of the first player obtained from the request.
  - remove_server_status (optional): **Default=True** Remove from the response the server status (redundant).
You can show it setting this param to **False**
````python
import cohpy

api_client = cohpy.get_api_client()

api_client.leaderboard(leaderboard_id=cohpy.Codes.USF3v3, sort_type=cohpy.SortType.ELO)
````

api_client.match_history():
: Get all leaderboards available from the COH API

- Parameters:
  - profile_params (mandatory): Player id. Can be steam profile id or relic id (Don't forget to set the mode). Can be a list of ints or strings. Steam queries must follow /steam/[0-9]+
  - mode (optional): **Default=relic** Set the query mode. Options are [relic, steam].
  - remove_server_status (optional): **Default=True** Remove from the response the server status (redundant).
You can show it setting this param to **False**
````python
import cohpy

api_client = cohpy.get_api_client()

api_client.match_history(profile_params=[1, 2])
api_client.match_history(profile_params=1)
api_client.match_history(profile_params='/steam/123456789', mode='steam')
api_client.match_history(profile_params=['/steam/123456789', '/steam/123456789'], mode='steam')

````

api_client.personal_stats():
: Get all leaderboards available from the COH API

- Parameters:
  - profile_params (mandatory): Player id. Can be steam profile id, relic id or alias (Don't forget to set the mode). Can be a list of ints or strings. Steam queries must follow /steam/[0-9]+
  - mode (optional): **Default=relic** Set the query mode. Options are [relic, steam, alias].
  - remove_server_status (optional): **Default=True** Remove from the response the server status (redundant).
You can show it setting this param to **False**
````python
import cohpy

api_client = cohpy.get_api_client()

api_client.personal_stats(profile_params=[1, 2])
api_client.personal_stats(profile_params=1)
api_client.personal_stats(profile_params='/steam/123456789', mode='steam')
api_client.personal_stats(profile_params=['/steam/123456789', '/steam/123456789'], mode='steam')
api_client.personal_stats(profile_params='yoursuperalias', mode='alias')
api_client.personal_stats(profile_params=['yoursuperalias', 'awesomealias'], mode='alias')

````

# Examples
First of all, you'll need an APIClient instance to retrieve the api data: 
````python
import cohpy

api_client = cohpy.get_api_client()
````
Then you could use the API interface to retrieve the data you want:

````python
import cohpy

all_leaderboards = api_client.leaderboards() # Returns all leaderboards info
american_3v3_leaderboard = api_client.leaderboard(leaderboard_id=cohpy.Codes.USF3v3) # Returns info from specific leaderboard
````
Note that ````leaderboard_id```` can be a int or a cohpy.Codes instance.
