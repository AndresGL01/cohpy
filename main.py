import cohpy

api_client = cohpy.get_api_client()

api_client.leaderboard_id = cohpy.Codes.USF3v3

print(api_client.leaderboard_data)

