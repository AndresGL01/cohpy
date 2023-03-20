<h1 style="text-align: center">COHPY</h1>
<div style="text-align: center">
<i>An API Wrapper for Company Of Heroes API</i>

<a href="https://github.com/AndresGL01/cohpy/stargazers"><img src="https://img.shields.io/github/stars/AndresGL01/cohpy" alt="Stars Badge"/></a>
</div>

### Tutorial
- [How to install](#How-to-install)
- [Examples](#Examples)

## Current API Coverage
- List all leaderboards ✔️
- Show players from a leaderboard ️✔️
- Show match historial from a player ✔️


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