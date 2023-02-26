import re
from enum import Enum


def sort_func(e):
    return e['value']


def sort_func2(e):
    return e.points


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
statistics_menu = "Type the name of a course to see details or 'back' to quit:"
command_statistics = "statistics"
response_unknown_course = "Unknown course."
command_notify = "notify"

id_sequence_generator = 0


class Course(Enum):
    Java = "Java"
    DSA = "DSA"
    Databases = "Databases"
    Spring = "Spring"


completed_courses = {
    Course.Java: 600,
    Course.Databases: 480,
    Course.DSA: 400,
    Course.Spring: 550,
}


class Student:
    id: str
    first_name: str
    last_name: str
    email: str

    courses = None

    def __init__(self, first_name, last_name, email):
        self.courses = {
            Course.Java: 0,
            Course.Databases: 0,
            Course.DSA: 0,
            Course.Spring: 0,
        }

        global id_sequence_generator
        self.id = str(id_sequence_generator)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        id_sequence_generator = id_sequence_generator + 1

    def get_student_points(self):
        return response_students_points_template.format(self.id,
                                                        Course.Java.name, self.courses[Course.Java],
                                                        Course.DSA.name, self.courses[Course.DSA],
                                                        Course.Databases.name, self.courses[Course.Databases],
                                                        Course.Spring.name, self.courses[Course.Spring])

    def get_course_stat(self, course):
        return CourseStatistic(self.id, self.courses[course], course)

    def __eq__(self, other):
        if self == other:
            return True
        if self is None or type(self) != type(other):
            return False
        return self.email == other.email

    def __hash__(self):
        return self.email.__hash__()

    def update_points(self, points: list):
        self.courses[Course.Java] = self.courses[Course.Java] + points[0]
        self.courses[Course.DSA] = self.courses[Course.DSA] + points[1]
        self.courses[Course.Databases] = self.courses[Course.Databases] + points[2]
        self.courses[Course.Spring] = self.courses[Course.Spring] + points[3]

    def __str__(self):
        return self.id


class CourseStatistic:
    id: str
    points: int
    course: Course

    def __init__(self, id: str, points: int, course: Course):
        self.id = id
        self.points = points
        self.course = course

    def get_completed(self):
        return float(
            '{:.1f}'.format
            (float(100 * float(self.points) / completed_courses[self.course]))
        )


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

    def get_course_stat(self, course: Course) -> list:
        list_stat = []
        for s in self.students_repository:
            stat: CourseStatistic = s.get_course_stat(course)
            if stat.points != 0:
                list_stat.append(stat)
        return list_stat
    def get_users_completed(self):
        students = []
        for s in self.students_repository:
            for c in Course:
                if s.courses[c] >= completed_courses[c]:
                    students.append({"student": s, "course_name": c.name})
        return students




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
        elif user_input == command_statistics:
            return ui.statistics(True)
        elif user_input == command_notify:
            return ui.notify()
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

    def get_course_stats_list(self, course_name: str) -> list:
        course_names = [s.name for s in Course]
        stat_for_course: list
        if course_name not in course_names:
            return []
        else:
            course = Course[course_name]
            stat_for_course = repository.get_course_stat(course)

        return stat_for_course

    def get_course_stats(self, course_name: str):
        list_stat = self.get_course_stats_list(course_name)
        list_stat.sort(key=sort_func2, reverse=True)
        print(course_name)
        print("id    points    completed")
        for stat in list_stat:
            print("{}    {}    {}%".format(stat.id, stat.points, stat.get_completed()))

    def get_statistics_report(self):
        report = """Most popular: {}
Least popular: {}
Highest activity: {}
Lowest activity: {}
Easiest course: {}
Hardest course: {}"""
        if len(self.repository.students_repository) == 0:
            return report.format("n/a", "n/a", "n/a", "n/a", "n/a", "n/a")
        else:
            courses = []
            list_java = self.get_course_stats_list("Java")
            sum_points_java = sum([x.points for x in list_java])
            courses.append({"name": Course["Java"], "value": sum_points_java})
            list_dsa = self.get_course_stats_list("DSA")
            sum_points_dsa = sum([x.points for x in list_dsa])
            courses.append({"name": Course["DSA"], "value": sum_points_dsa})
            list_databases = self.get_course_stats_list("Databases")
            sum_points_databases = sum([x.points for x in list_databases])
            courses.append({"name": Course["Databases"], "value": sum_points_databases})
            list_spring = self.get_course_stats_list("Spring")
            sum_points_spring = sum([x.points for x in list_spring])
            courses.append({"name": Course["Spring"], "value": sum_points_spring})
            courses.sort(key=sort_func, reverse=True)
            return report.format(", ".join(x["name"].name for x in courses),
                                 "n/a",
                                 ", ".join(x["name"].name for x in courses),
                                 "n/a",
                                 courses[0]["name"].name,
                                 courses[len(courses) - 1]["name"].name)

    def get_students_completed_courses(self):
        return self.repository.get_users_completed()


def is_valid_points_format(id_points_input: list):
    if len(id_points_input) != 5:
        return False
    all_points_matches = True
    for p in id_points_input[1:]:
        if not re.match("\\d+", p):
            all_points_matches = False
    return all_points_matches


def is_course(course_name):
    return course_name in [s.name for s in Course]


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

    def statistics(self, print_eader: bool):
        if print_eader:
            print(statistics_menu)
            print(self.controller.get_statistics_report())

        user_input = input()

        if user_input == command_back:
            return ""
        elif not is_course(user_input):
            print(response_unknown_course)
        else:
            print(self.controller.get_course_stats(user_input))

        return self.statistics(False)
    notified_students_courses=[]
    def notify(self):
        completed_students = self.controller.get_students_completed_courses()
        current_notified = []
        for s in completed_students:
            if s not in self.notified_students_courses:
                current_notified. append(s)
            else:
                continue
            output_str = """To: {}
Re: Your Learning Progress
Hello, {}! You have accomplished our {} course!"""
            #{"student": s, "course_name": c.name}
            print(output_str.format(s["student"].email,
                                    s["student"].first_name+" " + s["student"].last_name,
                                    s["course_name"])
                  )
        for s in current_notified:
            self.notified_students_courses.append(s)
        output_str_2 = "Total {} students have been notified."
        students = [s["student"] for s in current_notified]
        students = list(dict.fromkeys(students) )
        print(output_str_2.format(len(students)))
        return ""


if __name__ == '__main__':
    repository = StudentsRepository()
    controller = Controller(repository)
    ui = Ui(controller)
    ui.interact()
