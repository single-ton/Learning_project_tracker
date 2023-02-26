import re


# Write your code here

def is_valid_credentials(args: list):
    return len(args) >= 3


def is_valid_name(name: str):
    return re.match("(?i)^([a-z]['-]?)+[a-z]$", name)


def is_valid_email(email: str):
    return re.match("(?i)^[a-z0-9._-]+@[a-z0-9_-]+\\.([a-z0-9]\\.?)+$", email)


class Ui:
    def interact(self):
        print("---Learning-Progress-Tracker---")
        while True:
            self.main_menu()

    def main_menu(self):
        user_input = input()
        response = self.process_main_input(user_input)
        print(response)
        if str.strip(user_input).lower().casefold() == "exit":
            exit(0)

    def process_main_input(self, user_input):
        command = str.strip(user_input).lower()
        if command == "exit":
            return "Bye"
        elif command == "back":
            return "Enter to exit the program"
        elif command == "add students":
            return self.add_students()
        elif command == "":
            return "No input."
        else:
            return "unknown command"

    def add_students(self):
        print("Enter student credentials or 'back' to return")
        s = self.add_several_students(0)
        return s

    def add_several_students(self, count: int) -> str:
        user_input = input()
        if user_input.casefold() == "back":
            return f"There was a total of {count} students added"

        args = re.split("\\s+", user_input.strip())
        if not is_valid_credentials(args):
            print("Incorrect credentials")
            return self.add_several_students(count)
        elif not is_valid_name(args[0]):
            print("Incorrect first name")
            return self.add_several_students(count)
        elif not is_valid_email(args[len(args) - 1]):
            print("incorrect email")
            return self.add_several_students(count)
        else:
            any_invalid = True
            for i in range(len(args)):
                if i == 0:
                    continue
                if i == len(args)-1:
                    continue
                if not is_valid_name(args[i]):
                    any_invalid = False
                    break
            if not any_invalid:
                print("Incorrect last name.")
                return self.add_several_students(count)
            print("yeah student has been added.")
            return self.add_several_students(count + 1)


ui = Ui()
ui.interact()
