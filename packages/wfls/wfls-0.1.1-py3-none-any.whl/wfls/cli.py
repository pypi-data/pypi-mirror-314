import sys
import os
import time
import wfls.ui as ui
import wfls.movinf as movinf
import wfls.conway as conway

def help_message():
    return """Usage: poetry run <command> [options]

Commands:
    help        :     Display this help message
    -h, --help  :     Display this help message
    movinfo     :     Search for a movie, series, or episode
    wc [path]   :     Count lines, words, and characters in the specified file
    ls [path]   :     List the contents of the specified directory
    gol         :     Start the Game of Life simulation
"""

def main():
    """Handle command-line arguments and call the appropriate functions."""
    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        print(help_message())
        return

    command = sys.argv[1]

    if command == "movinfo":
        movinf.movinfo()
    elif command == "wc":
        if len(sys.argv) != 3:
            print("Usage: wc <file_path>")
        else:
            wc(sys.argv[2])
    elif command == "ls":
        if len(sys.argv) == 2:
            ls()
        elif len(sys.argv) == 3:
            ls(sys.argv[2])
        else:
            print("Usage: ls [directory_path]")
    elif command == "gol":
        game_of_life()
    else:
        print(f"Unknown command: {command}")
        print(help_message())

def greet(names):
    """Returns a string that consists of a greeting to the given names in the correct format."""
    if len(names) == 1:
        name_str = names[0]
    else:
        name_str = f"{', '.join(names[:-1])} and {names[-1]}"

    utc_time = arrow.utcnow()
    eastern_time = utc_time.to('US/Eastern').format('YYYY-MM-DD HH:mm:ss')
    return f"Hello, {name_str} | It is now {eastern_time} EDT"

def wc(file_path):
    """Count the number of lines, words, and characters in a file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            num_lines = content.count('\n')
            words = content.split()
            num_words = len(words)
            num_chars = len(content)

        print(f"{num_lines} lines, {num_words} words, {num_chars} characters")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def ls(directory_path='.'):
    """List the contents of a directory."""
    try:
        with os.scandir(directory_path) as entries:
            for entry in entries:
                print(entry.name)
    except FileNotFoundError:
        print(f"Error: The directory '{directory_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def ls_from_args():
    """Handle ls command and pass the directory path argument."""
    import sys
    if len(sys.argv) == 1:
        ls() 
    elif len(sys.argv) == 2:
        ls(sys.argv[1])
    else:
        print("Usage: ls [directory_path]")

def movinfo():
    """To start the movie/series/episode search."""
    ui.list_results(movinf.prompt())

def game_of_life():
    """Start the Game of Life simulation. No arguments are required since it will be randomized."""
    rows, cols = 20, 40
    grid = conway.initialize_grid(rows, cols)
    while True:
        conway.display_grid(grid)
        grid = conway.update_grid(grid)
        time.sleep(0.5)

if __name__ == "__main__":
    main()



