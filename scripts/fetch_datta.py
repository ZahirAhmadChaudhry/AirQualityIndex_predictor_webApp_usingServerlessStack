import requests
city = "saint-etienne"  # Replace your_city with the city you're interested in
token = "ab073ea1b371840c774c54de310fc0aabf5f3aa8"  # Replace with your actual WAQI token

url = f"https://api.waqi.info/feed/{city}/?token={token}"

response = requests.get(url)
data = response.json()

print(data)