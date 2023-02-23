import requests

API_KEY = "c957f71fa44bb198ad10dd61af2133ff"


def get_data(place, forecaste_days=None):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    filtered_data = data["list"]
    num_values = 8 * forecaste_days
    filtered_data = filtered_data[:num_values]

    return filtered_data


if __name__ == "__main__":
    print(get_data(place="Beijing", forecaste_days= 3))
