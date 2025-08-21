import os

def sort_and_print_names():
    """
    Reads names from names1.txt and names2.txt, combines them, sorts them,
    and prints the first 10 names.
    """
    names = []
    try:
        with open("names1.txt", "r") as f:
            names.extend(f.read().splitlines())
    except FileNotFoundError:
        print("names1.txt not found.")
        return

    try:
        with open("names2.txt", "r") as f:
            names.extend(f.read().splitlines())
    except FileNotFoundError:
        print("names2.txt not found.")
        return

    names.sort()

    print("First 10 alphabetically sorted names:")
    for i in range(min(10, len(names))):
        print(names[i])

if __name__ == "__main__":
    sort_and_print_names()
