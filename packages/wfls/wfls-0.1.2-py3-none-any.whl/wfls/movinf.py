import requests
import wfls.ui as ui

def movie():
    """Search format for a movie"""
    s = input("Enter the movie name: ")
    response = requests.get("http://www.omdbapi.com", params={"apikey":"36b4f1ae", "s": s, "type":"movie"})
    return response.json()

def series():
    """Search format for a series"""
    i = input("Enter the series name: ")
    response = requests.get("http://www.omdbapi.com", params={"apikey":"36b4f1ae", "s": i, "type":"series"})
    return response.json()

def episode():
    """Search format for an episode"""
    e = input("Enter the episode name: ")
    response = requests.get("http://www.omdbapi.com", params={"apikey":"36b4f1ae", "s": e, "type":"episode"})
    return response.json()

def prompt():
    """Prompt the user to select the search type.
    The user can select between a movie, series, or episode by typing 1, 2, or 3.
    User input is validated to ensure it is a number between 1 and 3."""
    print("1. Movie")
    print("2. Series")
    print("3. Episode")

    while True:
        try:
            user_input = int(input("What do you want to search for? "))
            if user_input == 1:
                return movie()
            elif user_input == 2:
                return series()
            elif user_input == 3:
                return episode()
            else:
                print("You must enter a number 1 to 3")
        except ValueError:
            print("Invalid input, please enter a valid number.")

