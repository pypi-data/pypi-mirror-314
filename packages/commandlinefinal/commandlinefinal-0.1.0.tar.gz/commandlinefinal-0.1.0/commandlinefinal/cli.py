import math
import sys
import string


def help_message():
    return """Usage: circumference <radius> [options]
    <radius> is a positive number that can include decimals

    Options:
        -h, --help: Displays this help message

    Examples:

    $ circumference 15.7
    A circle with radius 15.7 has a circumference of 98.646
    """

def parse_args(args):
    """Parse the command line arguments. 
    If there is an error, print an error message and exit.
    Args must be a positive decimal number
    Returns the circumference of a circle with the given radius
    """

    if len(args) == 0 or ("-h" in args) or ("--help" in args):

        print(help_message())

        sys.exit(1)


    invalid_chars = string.ascii_letters + "!#$%&'()*+,-/:;<=>?@[]^`{|}~" + '"' # when ran in bash certian charcters will be seen as bash commands and will cause the console to for example 12345! will; search for bash history

    if any(char in invalid_chars for char in args[0]): # checks if argument contains any character that is not a number or a decimal

        print("Invalid argument. Radius must be a number")

        sys.exit(1)

    try: 

        radius = float(args[0])

        if radius < 0:

            print("Invalid input. Please enter a positive number")

            sys.exit(1)

    except ValueError:

        print("Invalid argument. Radius must be a number ")

        sys.exit(1)

    return radius

def solveCircumference(radius):
    """
    solves the circumfrence from the radius and will give a preset output with both the circumfrence and radius to the main
    function to be printed
    """
    circumference = round(2 * math.pi * radius, 3) 

    write_to_file(circumference)

    return f"A circle with radius {radius} has a circumference of {circumference}"
    
def main():
    """
    this function args = sys.argv[1:]  
    radius = parse_args(args)
    print(solveCircumference(radius))
    """
    args = sys.argv[1:]  

    radius = parse_args(args)

    print(solveCircumference(radius))
   
if __name__ == "__main__":

    main()

def write_to_file(circumference):
    """Writes the circumference to the file 'circumference.txt'. Creates the file if one does not already exist.
    """

    open_file = open("circumference.txt","a")

    open_file.write(str(circumference))

    open_file.close()

    

