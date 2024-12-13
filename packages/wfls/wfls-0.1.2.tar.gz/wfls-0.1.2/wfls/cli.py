import arrow
import sys
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
    greet[names]:     Greet the specified names

Examples:
    wfls movinfo
    wfls wc file.txt
    wfls ls /path/to/directory
    wfls gol
    wfls greet Alice Bob Charlie
"""

def greet(names):
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
        import os
        if not directory_path:
            directory_path = '.'
        for entry in os.listdir(directory_path):
            print(entry)
    except FileNotFoundError:
        print(f"Error: The directory '{directory_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def movinfo():
    """To start the movie/series/episode search."""
    ui.list_results(movinf.prompt())

def game_of_life():
    """Start the Game of Life simulation."""
    rows, cols = 20, 40
    grid = conway.initialize_grid(rows, cols)
    while True:
        conway.display_grid(grid)
        grid = conway.update_grid(grid)
        time.sleep(0.5)

def main():
    """Handle command-line arguments and call the appropriate functions."""

    valid_commands = ["movinfo", "wc", "ls", "gol", "greet"]
    command_map = {
        "movinfo": movinfo,
        "wc": lambda: wc(sys.argv[2] if len(sys.argv) > 2 else None),
        "ls": lambda: ls(sys.argv[2] if len(sys.argv) > 2 else '.'),
        "gol": game_of_life,
        "greet": lambda: print(greet(sys.argv[2:])),
    }

    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command in valid_commands:
        try:
            command_map[command]()
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        if command:
            print(f"Error: Invalid command '{command}'")
        else:
            print("Error: No command provided.")
        print(help_message())

if __name__ == "__main__":
    main()