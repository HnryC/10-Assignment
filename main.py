import json


def get_input():
    typing = input(" Enter an opperation: ").lower()
    # This match statement is equivelent to chaining if elif else, I just think
    # it looks nicer. This function recives user input, and checks if it fits a
    # registed command. If it dosen't, it preforms the help action.
    #
    # Note: The help command is not registed because it should produce the same
    # outcome as an invalid command.
    match typing:
        case "order" | "o":
            return "order"
        case "add" | "a":
            return "add"
        case "quit" | "q":
            return "quit"
        case "save" | "s":
            return "save"
        case "print" | "p":
            return "print"
        case _:
            return "help"


def add_money(cash, user):
    while True:
        dolars = input(" Enter how many dolars you would like to add: ")
        try:
            dolars = int(dolars)
            break
        except ValueError:
            if dolars == "q":
                return cash
            print(" Please only use numbers, thank you!")

    while True:
        cents = input(" Enter how many cents you would like to add: ")
        try:
            cents = int(cents)
            break
        except ValueError:
            if cash == "q":
                return cash
            print(" Please only use numbers, thank you!")
    # The except ValueError is designed to catch someone inputing a non intiger
    # character when prompted. But to allow someone to quit out of the menu, it
    # checks if the character is q, and if it is, it will quit the shell.

    cash[user] += (dolars * 100) + cents
    # This is nesacary as the money is being stored as cents, to avoid
    # floating point error.
    # https://stackoverflow.com/questions/588004/is-floating-point-math-broken
    return cash


def place_order(orders, menu, cash, user):
    def check_order(order, user, cash, orders):
        # Private function to make code easier to read
        if cash[user] < order[1]:
            print(" You don't have enough money to order that. :(")
            return (cash, orders)
        orders[user].append(order[0])
        cash[user] -= order[1]
        return (cash, orders)

    place = ''  # Place sets the catogory of item being ordered.
    #             '' means that the user is selecting the catogory
    while True:
        if place == '':
            imput = input(" Enter cagory of order (l to list): ")
            if imput in menu:
                place = imput  # Assigns the catogory
            elif (imput.isdigit() and 0 < int(imput) <= len(menu)):
                place = list(menu)[int(imput) - 1]
                # Hashmaps cannot be indexed by number, but this code indexes
                # the array of the keys by 1 less than the number provided as
                # in python arrays are are indexed from 0
            elif imput.lower() in ('q', 'quit'):  # The .lower() makes the
                return (orders, cash)  # .          input case insensitive
            else:
                print(" ┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ")
                print(" ┃ Shortcut ┃ Item                          ┃ ")
                print(" ┣━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫ ")
                for (i, key) in enumerate(menu.keys()):
                    print(" ┃ " + str(i + 1).ljust(8) +
                          " ┃ " + key.ljust(29) +
                          " ┃ ")
                print(" ┣━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫ ")
                print(" ┃ Q        ┃ Return to menu                ┃ ")
                print(" ┗━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ")
                # Help menu. The code is better explained further down.

        else:
            imput = input(" Enter order (l to list): ")
            if imput in menu[place]:
                price = menu[place][imput]
                cash, orders = check_order((imput, price), user, cash, orders)
                finished = input(" Have you finished ordering? (Y/n) ")
                if not(finished.lower() in ('n', 'no')):
                    return (orders, cash)
                # This orders the food
            elif (imput.isdigit() and 0 < int(imput) <= len(menu[place])):
                indexes = list(menu[place])[int(imput) - 1]
                price = menu[place][indexes]
                cash, orders = check_order((indexes, price),
                                           user, cash, orders)
                finished = input(" Have you finished ordering? (Y/n) ")
                if not(finished.lower() in ('n', 'no')):
                    return (orders, cash)
                # This orders the food, but with number input
            elif imput.lower() in ('b', 'back'):
                place = ''  # Reseting place to '' allows for selecting
                #             a diferent catogory
            elif imput.lower() in ('q', 'quit'):
                return (orders, cash)
            else:
                print(" ┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓ ")
                print(" ┃ Shortcut ┃ Item              ┃ Price     ┃ ")
                print(" ┣━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━┫ ")
                for (i, key) in enumerate(menu[place].keys()):
                    print(" ┃ " + str(i + 1).ljust(8) +
                          " ┃ " + key.ljust(17) +
                          " ┃ " + ('$' + str(menu[place][key] // 100) +
                                   '.' + str(menu[place][key])[-2:].
                                   rjust(2, '0')).rjust(9) +
                          " ┃ ")
                print(" ┣━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━┫ ")
                print(" ┃ B        ┃ Reselect catogory             ┃ ")
                print(" ┃ Q        ┃ Return to menu                ┃ ")
                print(" ┗━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ")
                # The enumerate(ittorator) means that each itterable value is
                # pared by a number, starting at 0. This number has 1 added to
                # it to get the 'menu index', which is shown to the user. The
                # .ljust(x) suffix means that when the string is shorter than x
                # it adds spaces till it matches the width to the end of the
                # string. .rjust works the same way, but it creates right
                # alignment instead of left alignment. I is the number given by
                # enumerate(), and key is the key of the hashmap. The price is
                # given by using deviding the cost by 100, and flooring (or
                # removing all values after the decimal place) and adding the
                # last two items in the cost.


def dump(x):
    # This function takes in a list of tuple's, each tuple should consist of a
    # python dict and a path. It then writes the dict as JSON in the location
    # of the path
    for data in x:
        with open(data[1], "w") as f:
            json.dump(data[0], f)


def print_info(user, money, orders):
    print(" ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ")
    print(" ┃ Current User ┃ " + user.ljust(25) + " ┃ ")
    print(" ┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━┫ ")
    print(" ┃ Balance      ┃  "
          + ('$' + str(money[user] // 100) +
             '.' + str(money[user])[-2:].rjust(2, '0')).rjust(24) +
          " ┃ ")
    if len(orders[user]) == 0:
        print(" ┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ")
        return
    print(" ┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━┫ ")
    print(" ┃ Order        ┃ " + orders[user][0].ljust(25) + " ┃ ")
    if len(orders[user]) == 1:
        print(" ┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ")
        return
    for i in orders[user][1:]:
        print(" ┃              ┃ " + i.ljust(25) + " ┃ ")
    print(" ┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ")
    # This is similar to the menu lister found above. The [1:] pattern means
    # that all items itterated over except the first.


def get_user(order, cash):
    def list_users():
        print(" ┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ")
        print(" ┃ Shortcut ┃ User                          ┃ ")
        print(" ┣━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫ ")
        for (i, key) in enumerate(order.keys()):
            print(" ┃ " + str(i + 1).ljust(8) +
                  " ┃ " + key.ljust(29) +
                  " ┃ ")
        print(" ┣━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫ ")
        print(" ┃ N        ┃ New User                      ┃ ")
        print(" ┃ Q        ┃ Quit                          ┃ ")
        print(" ┗━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ")
        # Another menu system. Wow. It works very similar.

    while True:
        list_users()
        user = input(" Select user: ")
        if user.isdigit() and 0 < int(user) <= len(order):
            user = list(order)[int(user) - 1]
            return(user, order, cash)
        elif user in order:
            return(user, order, cash)
        elif user.lower() == 'q':
            exit(0)
        elif user.lower() == 'n':
            while True:
                new_user = input(" Enter a new username: ")
                match new_user:
                    case 'q' | 'Q':
                        exit(0)
                    case 'n' | 'N':
                        print(" Invalid Username")
                    case _:
                        if new_user in cash:
                            print(" Username allready taken")
                        else:
                            cash[new_user] = 0
                            order[new_user] = []
                            return(new_user, order, cash)


def main():
    def print_help():
        print(" ┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ")
        print(" ┃ Command ┃ Function                       ┃ ")
        print(" ┣━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫ ")
        print(" ┃ Add     ┃ Opens money shell              ┃ ")
        print(" ┃ Order   ┃ Opens order shell              ┃ ")
        print(" ┃ Print   ┃ Prints user data               ┃ ")
        print(" ┃ Help    ┃ Prints help menu               ┃ ")
        print(" ┃ Save    ┃ Saves orders & balance changes ┃ ")
        print(" ┃ Quit    ┃ Save and quit                  ┃ ")
        print(" ┗━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ")
        # The reson that this is a private function of main() is so it allows
        # main() to have more conscice logic statements. These print statements
        # could of been put in the match statement, but I belive that that
        # would make the function harder to read.

    with (
            open("data/menu.json") as f,
            open("data/order.json") as g,
            open("data/cash.json") as h,
            ):
        menu = json.load(f)
        order = json.load(g)
        cash = json.load(h)
    # The with statement opens the .json files that store the menu, order
    # history and money information, and it parses them into a hashmap
    # using the json.load() function from the json crate.

    (user, order, cash) = get_user(order, cash)
    # Assigning a returned tuple to multiple values is called tuple unpacking

    while True:
        match get_input():
            case "help":
                print_help()

            case "add":
                cash = add_money(cash, user)

            case "order":
                (order, cash) = place_order(order, menu, cash, user)

            case "print":
                print_info(user, cash, order)

            case "save":
                dump([
                    (menu, "data/menu.json"),
                    (cash, "data/cash.json"),
                    (order, "data/order.json")
                    ])

            case "quit":
                dump([
                    (menu, "data/menu.json"),
                    (cash, "data/cash.json"),
                    (order, "data/order.json")
                    ])
                exit(0)
        # This matches the output of the get_input function and preforms
        # actions based on it's return value.


# The if __name__ == "__main__" statement allows for this file to only run
# it's code if it is run directly, and not called as a library to
# another program. This is because all code not inside a function or
# other form of indentation will allways run when the file is loaded, but
# the program's __name__ variable will not be "__main__".
if __name__ == "__main__":
    main()
