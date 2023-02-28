import re
from enum import Enum


def is_valid_credentials(args: list):
    return len(args) >= 3


def is_valid_name(name: str):
    return re.match("(?i)^([a-z]['-]?)+[a-z]$", name)


def is_valid_email(email: str):
    return re.match("(?i)^[a-z0-9._-]+@[a-z0-9_-]+\\.([a-z0-9]\\.?)+$", email)


initial_greetings = "==Learning-Progress-Tracker=="
goodbye = "Bye!"
add_students_menu = "Enter student credentials or 'back' to return:"
add_points_menu = "Enter an id and points or 'back' to return:"
find_menu = "Enter an id or 'back' to return:"
command_add_students = "add students"
command_add_points = "add points"
command_back = "back"
command_exit = "exit"
command_find = "find"
command_list_students = "list"
command_empty = ""
response_added_students_result_template = "There was a total of {} students added"
response_students_points_template = "{} points: {}={}; {}={}; {}={}; {}={}"
response_student_id_not_found_template = "No student is found for id={}."
response_back = "Do you wish to quit the program? You may enter exit to do so"
response_empty = "oooops....that's no input, try again"
response_invalid_command = "Hmm... that is unknown for me. You can try a new command or type exit to leave"
response_list_students_none_found = "No students found"
response_list_students_header = "Students\n"
response_points_updated = "Points updated."
invalid_credentials = "incorrect credentials"
invalid_email = "That's some incorrect email, don't try to fool me"
invalid_first_name = "Incorrect first name it probably is"
invalid_last_name = "I'm sure this is an incorrect last name"
invalid_points_format = "Incorrect points format."
student_added = "yeah student has been added."
email_is_taken = "This email is already taken."

id_sequence_generator = 0


class Course(Enum):
    Python = "Python"
    DSA = "DSA"
    Databases = "Databases"
    Flask = "Flask"


class Student:
    id: str
    first_name: str
    last_name: str
    email: str

    courses = None

    def __init__(self, first_name, last_name, email):
        self.courses = {
            Course.Python: 0,
            Course.Databases: 0,
            Course.DSA: 0,
            Course.Flask: 0,
        }
        global id_sequence_generator
        self.id = str(id_sequence_generator)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        id_sequence_generator = id_sequence_generator + 1

    def get_student_points(self):
        return response_students_points_template.format(self.id,
                                                        Course.Python.name, self.courses[Course.Python],
                                                        Course.DSA.name, self.courses[Course.DSA],
                                                        Course.Databases.name, self.courses[Course.Databases],
                                                        Course.Flask.name, self.courses[Course.Flask])

    def __eq__(self, other):
        if self == other:
            return True
        if self is None or type(self) != type(other):
            return False
        return self.email == other.email

    #def __hash__(self):
    #    return self.email.__hash__()

    def update_points(self, points: list):
        self.courses[Course.Python] = self.courses[Course.Python] + points[0]
        self.courses[Course.DSA] = self.courses[Course.DSA] + points[1]
        self.courses[Course.Databases] = self.courses[Course.Databases] + points[2]
        self.courses[Course.Flask] = self.courses[Course.Flask] + points[3]

    def __str__(self):
        return self.id


class StudentsRepository:
    students_repository = []

    def contains(self, email: str):
        if len(self.students_repository) == 0:
            return False
        for s in self.students_repository:
            if email == s.email:
                return True
        return False

    def add(self, name: str, last_name: str, email: str):
        if self.contains(email):
            return False
        else:
            self.students_repository.append(Student(name, last_name, email))
            return True

    def list_students_id(self) -> str:
        if len(self.students_repository) == 0:
            return ""
        return "\n".join([str(s) for s in self.students_repository])

    def find_by_id(self, id) -> Student:
        try:
            return next(s for s in self.students_repository if s.id == id)
        except:
            return None


class Controller:
    repository: StudentsRepository

    def __init__(self, repository: StudentsRepository):
        self.repository = repository

    def process_main_input(self, user_input: str, ui):
        user_input = user_input.strip().lower()
        if user_input == command_add_points:
            return ui.add_points(True)
        elif user_input == command_add_students:
            return ui.add_students()
        elif user_input == command_back:
            return response_back
        elif user_input == command_empty:
            return response_empty
        elif user_input == command_find:
            return ui.find(True)
        elif user_input == command_exit:
            return goodbye
        elif user_input == command_list_students:
            list_students_id = self.repository.list_students_id()
            if list_students_id == "":
                return response_list_students_none_found
            else:
                return response_list_students_header + list_students_id
        else:
            return response_invalid_command

    def email_is_unique(self, email):
        return not self.repository.contains(email)

    def add_student(self, name: str, last_name: str, email: str):
        was_successful = self.repository.add(name, last_name, email)

        if not was_successful:
            raise ValueError(email_is_taken)

    def find_students_by_id(self, id):
        return self.repository.find_by_id(id)

    def add_points(self, input_id_points_array: list, student: Student):
        points = []
        for p in input_id_points_array[1:]:
            points.append(int(p))
        student.update_points(points)


def is_valid_points_format(id_points_input: list):
    if len(id_points_input) != 5:
        return False
    all_points_matches = True
    for p in id_points_input[1:]:
        if not re.match("\\d+", p):
            all_points_matches = False
    return all_points_matches


class Ui:
    controller: Controller

    def __init__(self, controller: Controller):
        self.controller = controller

    def interact(self):
        print(initial_greetings)

        while (True):
            user_input = input()
            output = self.controller.process_main_input(user_input, self)
            print(output)
            if output == goodbye:
                break

    def add_students(self):
        print(add_students_menu)
        return self.add_several_students(0)

    def add_several_students(self, count):
        user_input = input()

        if user_input.casefold() == command_back:
            return response_added_students_result_template.format(count)

        args = re.split("\\s+", user_input.strip())

        if not is_valid_credentials(args):
            print(invalid_credentials)
            return self.add_several_students(count)
        elif not is_valid_name(args[0]):
            print(invalid_first_name)
            return self.add_several_students(count)
        elif not is_valid_email(args[len(args) - 1]):
            print(invalid_email)
            return self.add_several_students(count)
        elif not self.controller.email_is_unique(args[len(args) - 1]):
            print(email_is_taken)
            return self.add_several_students(count)
        else:
            any_invalid = False
            last_name = ""
            for i in range(len(args)):
                if i == 0:
                    continue
                if i == len(args) - 1:
                    continue
                if not is_valid_name(args[i]):
                    any_invalid = True
                    break
                last_name = last_name + " " + args[i]
            if any_invalid:
                print(invalid_last_name)
                return self.add_several_students(count)
            try:
                self.controller.add_student(args[0], last_name, args[len(args) - 1])
            except Exception as e:
                print(str(e))
                return self.add_several_students(count)
            print(student_added)
            return self.add_several_students(count + 1)

    def add_points(self, print_header: bool):
        if print_header:
            print(add_points_menu)
        id_and_points = input()
        if id_and_points == command_back:
            return ""
        id_and_points_array = re.split("\\s+", id_and_points)
        if not is_valid_points_format(id_and_points_array):
            print(invalid_points_format)
            return self.add_points(False)
        student_by_id = self.controller.find_students_by_id(id_and_points_array[0])
        if student_by_id is None:
            print((response_student_id_not_found_template + "\n").format(id_and_points_array[0]))
        else:
            self.controller.add_points(id_and_points_array, student_by_id)
            print(response_points_updated)
        return self.add_points(False)

    def find(self, print_header: bool):
        if print_header:
            print(find_menu)
        id_input = input()
        if id_input == command_back:
            return ""
        student_by_id = self.controller.find_students_by_id(id_input)
        if student_by_id is None:
            print((response_student_id_not_found_template + "\n").format(id_input))
        else:
            print(student_by_id.get_student_points())

        return self.find(False)


if __name__ == '__main__':
    repository = StudentsRepository()
    controller = Controller(repository)
    ui = Ui(controller)
    ui.interact()
