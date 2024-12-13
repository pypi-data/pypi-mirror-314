import requests

def list_results(results):
    """The codes below are used to display the list of search results.
       The user is prompted to enter the number of the movie they want to see more information about."""
    if 'Search' in results:
        for index, item in enumerate(results['Search'], start=1):
            print(f"{index}. Title: {item['Title']}")

        try:
            user_input = int(input("Enter the number of the movie you want to see more information about: "))
            selected_item = results['Search'][user_input - 1]
            display_details(selected_item)
        except (ValueError, IndexError):
            print("Invalid input, please enter a valid number.")
    else:
        print("No results found.")

def display_details(item):
    """Fetch and display detailed information for the selected item"""
    response = requests.get("http://www.omdbapi.com", params={"apikey":"36b4f1ae", "i": item['imdbID']})
    details = response.json()

    if details.get('Response') == 'True':
        print("\n")
        title = details.get('Title')
        runtime = details.get('Runtime')
        genre = details.get('Genre')
        actors = details.get('Actors')
        year = details.get('Year')
        plot = details.get('Plot')

        info_parts = []
        if title and title != 'N/A':
            info_parts.append(title)
        if runtime and runtime != 'N/A':
            info_parts.append(f"is a {runtime}")
        else:
            info_parts.append("is a")
        if genre and genre != 'N/A':
            info_parts.append(genre)
        if actors and actors != 'N/A':
            info_parts.append(f"movie starring {actors}")
        if year and year != 'N/A':
            if '–' in year and year.split('–')[1]:
                info_parts.append(f"It was released in {year}")
            else:
                info_parts.append(f"It was released in {year.split('–')[0]}")
        if plot and plot != 'N/A':
            info_parts.append(plot)

        output = ". ".join(info_parts).replace("is a. ", "is a ").replace(". .", ".").replace(". is a", " is a").replace(". movie starring", " movie starring")
        print(output + ".")

        if details.get('Awards') and details['Awards'] != 'N/A':
            print("Awards: ")
            for award in details['Awards'].split("."):
                print(award.strip())

        if details.get('Ratings'):
            print("Ratings: ")
            for rating in details['Ratings']:
                print(f"{rating['Source']}: {rating['Value']}")
    else:
        print("No details available.")