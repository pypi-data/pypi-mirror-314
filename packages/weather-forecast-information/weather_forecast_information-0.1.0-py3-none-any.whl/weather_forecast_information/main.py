import argparse # to parse command line arguments
import pyfiglet # to generate ASCII art from text
from simple_chalk import chalk # to change the color of the text
import requests # to send HTTP requests
import string # to build the string with valid characters
import os # to create a file path for city.txt

# api key for openweathermap
apikey = "d8a9346172f8c77261b04e2db71f75a7"

# base url for openweathermap api
base_url = "https://api.openweathermap.org/data/2.5/weather"

# Weather codes to icons in a dictionary.  Made it a dictionary so it can look up the weather codes.
weather_icons = {
    # day icons
    "01d": "☀️", # clear sky
    "02d": "⛅", # few clouds
    "03d": "☁️", # scattered clouds
    "04d": "☁️", # broken clouds
    "09d": "🌧️", # shower rain
    "10d": "🌦️", # rain
    "11d": "⚡", # thunderstorm
    "13d": "❄️", # snow
    "50d": "🌫️", # mist 

    # night icons
    "01n": "🌙", # clear sky
    "02n": "☁️", # few clouds
    "03n": "☁️", # scattered clouds
    "04n": "☁️", # broken clouds
    "09n": "🌧️", # shower rain
    "10n": "🌦️", # rain
    "11n": "⚡", # thunderstorm
    "13n": "❄️", # snow
    "50n": "🌫️" # mist
}

valid_characters = string.ascii_lowercase + string.ascii_uppercase # added lowercase and uppercase letters from the English alphabet to a variable called valid_characters.

# contruct api url with query parameters
def parse_arguments():
    """
    This function parses the arguments given on the command line.
    It only accepts one argument.
    The argument is expected to be the name of a city to check the weather for.
    If no city is provided it returns None.
    If a city is provided it will return city=Whatever city you enter.
    """
    parser = argparse.ArgumentParser(description="Check the weather for a certain city") # ArgumentParser initalizes the parser that will handle the command line argument.  Description given if user runs with --help.
    parser.add_argument(
        "city", nargs="?", default=None, help="The city to check the weather for (optional)") # "city" is the name of the argument.  nargs="?" means the argument is optional.  If no city is provided the default argument is none.  The help message tells the user that the argument is the city to check the weather for but this argument is optional.
    return parser.parse_args() # Parsing the command line argument into an object.  Ex. if the argument is Paris then city=Paris.

def read_city_from_file():
        """
        Reads the city name from the city.txt file and returns it.
        The file should not be empty.
        The file should only have one city name.
        The function will raise errors if:
        - The file doesn't exist
        - The file is empty
        - The file has more than one city name
        - The file has invalid characters
        - The file cannot be read due to permission issues
        """
        try:
            file_path = os.path.join(os.path.dirname(__file__), "city.txt") # creates path for city.txt 
            file = open(file_path, "r") # attempts to open city.txt in read mode
            city = file.readlines() # Reads the entire file and stores each line as a string in a list. 
            city = [word.strip() for word in city if word.strip()]  # Removes whitespace and empty lines from the list
            if not city: # if city is empty
                print(chalk.red("Error: No command line argument given and city.txt is empty."))
                exit()
            if len(city) != 1: # if there is more than one city name
                    print(chalk.red("Error: city.txt must contain exactly one city name."))
                    exit()
            if any(char not in valid_characters + ' ' for char in "".join(city)): # Checks if the city name has only characters from the English alphabet.  any will return true if there is an invalid character but allows spaces.  "".join(city) joins the elements in the list into a single string.  By this I mean, if city.txt says New York, the list will be ['New', 'York'], so it combines it into one string.
                print(chalk.red("Error: Only letters from the English alphabet are accepted in your argument."))
                exit()
            file.close() # closes the file after reading it
            return city[0] # returns the first item in the city list
        # prints an error message if the file is not found
        except FileNotFoundError:
            print(chalk.red("Error: The file containing the city name was not found"))
            exit()
        # prints an error message if the program doesn't have read permissions 
        except PermissionError:
            print(chalk.red("Error: No read permission for 'city.txt'"))
            exit()

def get_weather_data(city):
    """
    Gets data on weather from a specified city by making a request to open weather map.
    The function creates a url with the city name and sends a get request.
    If the get request is successful it will return data on the weather in the given city.
    If the get request is unsuccessful it will raise an error.
    If the staus code is 401 it will print a message to the user that the api key is invalid or missing.
    If the status code is not 200, it will print a more broad message to the user saying that it is unable to get weather information for the given city.

    Parameter:
    
    The function has only one parameter which is the city name.

    Returns:

    The function returns a dictionary containing weather data.
    """
    url = f"{base_url}?q={city.replace(' ', '%20')}&appid={apikey}&units=metric" # creates the url for the api request.  city.replace, replaces the spaces in the string with %20.
    # makes api request and parses response using requests module
    try:
        response = requests.get(url) # Gets data for the given city from open weather map.  It then stores the response in a variable called response.
    except requests.exceptions.RequestException as e: # catches any errors during the request such as, network issues, invalid url or a timeout.
        print(chalk.red(f"Error: Unable to make API request: {e}")) # error message
        exit()
    if response.status_code == 401: # the 401 status code means the API key is wrong or missing
        print(chalk.red("Error: Invalid or missing API key")) # error message
        exit()
    if response.status_code != 200: # The 200 status code means the request was successful. 
        print(chalk.red(f"Error: Unable to retrieve weather information for {city}")) # error message
        exit()
    return response.json() # if the status code is 200 it will return the parsed JSON response

def format_weather_data(data):
    """
    This function formats and returns a readable weather report.
    It has only one parameter which is data which is from open weather map.
    """
    # get information from the response
    temperature = data["main"]["temp"] # gives temperature in celcius
    feels_like = data["main"]["feels_like"] # gives what the temperature feels like in celcius
    description = data["weather"][0]["description"] # Gives the description of the weather.  "weather" is a list.
    icon = data["weather"][0]["icon"] # Gives the icon for the weather.  "weather" is a list.
    city = data["name"] # gives the city name
    country = data["sys"]["country"] # gives the country code

    weather_icon = weather_icons.get(icon, "") # retrieves the icon code from the dictionary
    output = f"{pyfiglet.figlet_format(city)}, {country}\n\n" # Turns the city name into ascii art followed by the country code.  After that, it skips two lines.
    output += f"{weather_icon} {description}\n" # displays the weather icon with the description then skips a line.
    output += f"Temperature: {temperature}°C\n" # displays the temperature in celcius
    output += f"Feels like: {feels_like}°C\n" # displays what the temperature feels like in celcius
    
    return chalk.magenta(output) # returns the output using simple_chalk to make it magenta

def write_weather_to_file(output):
    """
    This function writes the output to a file called weather_output.txt.
    It only has one parameter which is output.
    Output is what was returned in def format_weather_data.
    It will raise an error if the program doesn't have write permission for weather_output.txt
    """
    try:
        file_path = os.path.join(os.path.dirname(__file__), "weather_output.txt") # Creates the file path for weather_output.txt.  os.path.dirname(__file__) returns the directory containing the file.  os.path.join, combines the path to the file with the name of the file.
        file = open(file_path, "w") # Opens weather_output.txt.  It uses "w" which means write so it overwrites what is in weather_output.txt.  This is different than "a" which is append and adds to the file.
        file.write(output) # writes the output
        file.close() # closes the file
    except PermissionError: # if the program doesn't have write permission it will raise an error
        print(chalk.red("Error: No write permission for 'weather_output.txt'")) # error message
        exit()

def main():
    """
    This is the main function for the program.
    It calls all previous functions.
    If the argument is provided on the command line it removes whitespace and checks if the characters are valid.
    It also prints the output.
    """
    args = parse_arguments() # calls parse_arguments and takes the return value and assigns it to args
    if args.city: # checks if the city argument was passed in the command line
        city = args.city.strip() # if the city argument was passed then it strips whitespaces at the start or end of the city name
    else:
        city = read_city_from_file() # If no city name is provided it calls read_city_from_file.  If the file is blank it returns an error message stating that there is no argument on the command line or in the file.
    if any(char not in valid_characters for char in city):
        print(chalk.red("Error: Only letters from the English alphabet are accepted in your argument."))
        exit()
    data = get_weather_data(city) # Calls get_weather_data to get data.  This data is assigned to the data variable.
    output = format_weather_data(data) # Passes the data dictionary to format_weather_data.  The return value is assigned to a variable called output.
    print(output) # prints output
    write_weather_to_file(output) # calls write_weather_to_file to write the output to weather_output.txt.
    print("Weather information saved to weather_output.txt") # prints a message to the user telling them that the weather information was saved to weather_output.txt
    exit()

if __name__ == "__main__":
    main()




t