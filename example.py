from src.fortnite import get_squad_stats, build_string_for_squad_stats

username = 'Reatsila' # Here your username.
platform = 'pc' # Here your platform: psn, xbox, pc.

squad_data = get_squad_stats(username, platform)
if len(squad_data) == 0:
  print("stop")
squad_data = squad_data[0]
print(build_string_for_squad_stats(squad_data))
