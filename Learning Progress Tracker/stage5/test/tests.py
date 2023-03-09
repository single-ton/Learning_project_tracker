from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import *
import re
import random
from hstest.testing.tested_program import TestedProgram
import numpy as np

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


def any_missing_keywords(output: str, *keywords:str):
    tokens = re.split("\\W+", output.lower())
    return not all(el.casefold() in tokens for el in keywords)


def incorrect_string(output: str, model: str):
    normalized_output = re.sub("\\W+", "", output).lower()
    normalized_model = re.sub("\\W+", "", model).lower()
    return not normalized_model in normalized_output


def generate_names(n: int):
    names = ["Shoshana Utica", "Marisa Firman", "Gwenette Anagnos", "Charlena Girardo",
             "Alexina Belcher", "Karee Antoinetta", "Dolley Panther", "Elysha Quinlan", "Trixie Winer",
             "Ricki Trovillion", "Amye Uriisa", "Hedwig Wally", "Gwenette Kironde", "Jermaine Naaman",
             "Olga Rosanne", "Annecorinne Ause", "Aurie Dorisa", "Van Fawnia", "Carmella Campman",
             "Francesca Francis", "Elwira Florrie", "Nonna Miko", "Natka Herculie", "Roxi Hett", "Brandise Hardan",
             "Toby Bleier", "Dalia Gleeson", "Emelia Annnora", "Beatrisa Jegar", "Barbara-Anne Chicky",
             "Ann Agnella", "Lebbie Alabaster", "Leola Whelan", "Starlin Griz", "Anjanette Uis", "Tasha Chem"]
    random.shuffle(names)
    return names[0:n]


def generate_emails(n: int):
    emails = []
    for i in range(0, n):
        emails.append("address" + str(i) + "@mail.com")
    return emails


def get_random_credentials(n: int):
    credentials = []
    names = generate_names(n)
    emails = generate_emails(n)
    for i in range(0, n):
        credentials.append(f"{names[i]} {emails[i]}")
    return credentials


def next_point():
    return random.randint(1, 10)


def get_correct_points(n):
    points = []
    for i in range(1, n):
        points.append(f"{next_point()} "
                      f"{next_point()} "
                      f"{next_point()} "
                      f"{next_point()}")
    return points


def parse_ids(output: str):
    lines = output.splitlines()
    return lines[1:]


def check_lines_1(current_lines, ids):
    return (not ((re.match(".+\\s+10\\s+1\\.7\\s?%.*", current_lines[2])) or
            (re.match(".+\\s+10\\s+1\\.8\\s?%.*", current_lines[2])) or
            (re.match(".+\\s+10\\s+1\\.6\\s?%.*", current_lines[2]))) or

            not ((re.match(".+\\s+5\\s+0\\.8\\s?%.*", current_lines[3])) or
            (re.match(".+\\s+5\\s+0\\.9\\s?%.*", current_lines[3])) or
            (re.match(".+\\s+5\\s+0\\.7\\s?%.*", current_lines[3]))) or

            not ((re.match(".+\\s+5\\s+0\\.8\\s?%.*", current_lines[4])) or
            (re.match(".+\\s+5\\s+0\\.9\\s?%.*", current_lines[4])) or
            (re.match(".+\\s+5\\s+0\\.7\\s?%.*", current_lines[4]))) or

            not ((re.match(".+\s+2\s+0\.3\s?%.*", current_lines[5])) or
            (re.match(".+\s+2\s+0\.2\s?%.*", current_lines[5])) or
            (re.match(".+\s+2\s+0\.4\s?%.*", current_lines[5]))) or

            not current_lines[2].startswith(ids[0]) or
            (not current_lines[3].startswith(ids[1]) and not current_lines[3].startswith(ids[2])) or
            (not current_lines[4].startswith(ids[1]) and not current_lines[4].startswith(ids[2])) or
            not current_lines[5].startswith(ids[3]) or
            (current_lines[3].startswith(ids[1]) and ids[1] >= ids[2]) or
            (current_lines[3].startswith(ids[2]) and ids[2] >= ids[1]))


def check_lines_2(current_lines, ids):
    return (not ((re.match(".+\\s+10\\s+2\\.5\\s?%.*", current_lines[2])) or
            (re.match(".+\\s+10\\s+1\\.6\\s?%.*", current_lines[2])) or
            (re.match(".+\\s+10\\s+1\\.4\\s?%.*", current_lines[2]))) or

            not ((re.match(".+\\s+5\\s+1\\.3\\s?%.*", current_lines[3])) or
            (re.match(".+\\s+5\\s+1\\.4\\s?%.*", current_lines[3])) or
            (re.match(".+\\s+5\\s+1\\.2\\s?%.*", current_lines[3]))) or

            not ((re.match(".+\\s+5\\s+1\\.3\\s?%.*", current_lines[4])) or
            (re.match(".+\\s+5\\s+1\\.2\\s?%.*", current_lines[4])) or
            (re.match(".+\\s+5\\s+1\\.4\\s?%.*", current_lines[4]))) or

            not ((re.match(".+\\s+2\\s+0\\.5\\s?%.*", current_lines[5])) or
            (re.match(".+\\s+2\\s+0\\.4\\s?%.*", current_lines[5])) or
            (re.match(".+\\s+2\\s+0\\.3\\s?%.*", current_lines[5]))) or

            not current_lines[2].startswith(ids[0]) or
            (not current_lines[3].startswith(ids[1]) and not current_lines[3].startswith(ids[2])) or
            (not current_lines[4].startswith(ids[1]) and not current_lines[4].startswith(ids[2])) or
            not current_lines[5].startswith(ids[3]) or
            (current_lines[3].startswith(ids[1]) and ids[1] >= ids[2]) or
            (current_lines[3].startswith(ids[2]) and ids[2] >= ids[1]))


def check_lines_3(current_lines, ids):
    return (not ((re.match(".+\\s+10\\s+2\\.1\\s?%.*", current_lines[2])) or
            (re.match(".+\\s+10\\s+2\\.2\\s?%.*", current_lines[2])) or
            (re.match(".+\\s+10\\s+2\\.0\\s?%.*", current_lines[2]))) or

            not ((re.match(".+\\s+5\\s+1\\.0\\s?%.*", current_lines[3])) or
            (re.match(".+\\s+5\\s+1\\.1\\s?%.*", current_lines[3]))) or

            not ((re.match(".+\\s+5\\s+1\\.0\\s?%.*", current_lines[4])) or
            (re.match(".+\\s+5\\s+1\\.1\\s?%.*", current_lines[4]))) or

            not ((re.match(".+\\s+2\\s+0\\.4\\s?%.*", current_lines[5])) or
            (re.match(".+\\s+2\\s+0\\.3\\s?%.*", current_lines[5])) or
            (re.match(".+\\s+2\\s+0\\.5\\s?%.*", current_lines[5]))) or

            not current_lines[2].startswith(ids[0]) or
            (not current_lines[3].startswith(ids[1]) and not current_lines[3].startswith(ids[2])) or
            (not current_lines[4].startswith(ids[1]) and not current_lines[4].startswith(ids[2])) or
            not current_lines[5].startswith(ids[3]) or
            (current_lines[3].startswith(ids[1]) and ids[1] >= ids[2]) or
            (current_lines[3].startswith(ids[2]) and ids[2] >= ids[1]))


def check_lines_4(current_lines, ids):
    return (not ((re.match(".+\\s+10\\s+1\\.8\\s?%.*", current_lines[2])) or
            (re.match(".+\\s+10\\s+1\\.9\\s?%.*", current_lines[2])) or
            (re.match(".+\\s+10\\s+1\\.7\\s?%.*", current_lines[2]))) or

            not ((re.match(".+\\s+5\\s+0\\.9\\s?%.*", current_lines[3])) or
            (re.match(".+\\s+5\\s+0\\.8\\s?%.*", current_lines[3]))) or

            not ((re.match(".+\\s+5\\s+0\\.9\\s?%.*", current_lines[4])) or
            (re.match(".+\\s+5\\s+0\\.8\\s?%.*", current_lines[4]))) or

            not ((re.match(".+\\s+2\\s+0\\.4\\s?%.*", current_lines[5])) or
            (re.match(".+\\s+2\\s+0\\.3\\s?%.*", current_lines[5])) or
            (re.match(".+\\s+2\\s+0\\.5\\s?%.*", current_lines[5]))) or

            not current_lines[2].startswith(ids[0]) or
            (not current_lines[3].startswith(ids[1]) and not current_lines[3].startswith(ids[2])) or
            (not current_lines[4].startswith(ids[1]) and not current_lines[4].startswith(ids[2])) or
            not current_lines[5].startswith(ids[3]) or
            (current_lines[3].startswith(ids[1]) and ids[1] >= ids[2]) or
            (current_lines[3].startswith(ids[2]) and ids[2] >= ids[1]))


class LearningProgressTrackerTest(StageTest):
    blanket_input = ["", " ", "\t", " \t"]
    unknown_commands = ["abc", "quit", "  brexit ", "exi  t", "help", "break",
                        "-help", "Ctrl+C", "exit please", ":q"]
    correct_credentials = ["John Smith jsmith@hotmail.com", "Anny Doolittle anny.md@mail.edu",
                           "Jean-Claude O'Connor jcda123@google.net", "Mary Emelianenko 125367at@zzz90.z9",
                           "Al Owen u15da125@a1s2f4f7.a1c2c5s4", "Robert Jemison Van de Graaff robertvdgraaff@mit.edu",
                           "Ed Eden a1@a1.a1", "na'me s-u ii@ii.ii", "n'a me su aa-b'b ab@ab.ab", "nA me 1@1.1"]
    incorrect_credentials = [
        ["", "Incorrect credentials"], [" \t", "Incorrect credentials."],
        ["name surname", "Incorrect credentials."],
        ["n surname email@email.xyz", "Incorrect first name."],
        ["'name surname email@email.xyz", "Incorrect first name."],
        ["-name surname email@email.xyz", "Incorrect first name."],
        ["name- surname email@email.xyz", "Incorrect first name."],
        ["name' surname email@email.xyz", "Incorrect first name."],
        ["nam-'e surname email@email.xyz", "Incorrect first name."],
        ["na'-me surname email@email.xyz", "Incorrect first name."],
        ["na--me surname email@email.xyz", "Incorrect first name."],
        ["na''me surname email@email.xyz", "Incorrect first name."],
        ["námé surname email@email.xyz", "Incorrect first name."],
        ["name s email@email.xyz", "Incorrect last name."],
        ["name -surname email@email.xyz", "Incorrect last name."],
        ["name 'surname email@email.xyz", "Incorrect last name."],
        ["name surnam''e email@email.xyz", "Incorrect last name."],
        ["name surn--ame email@email.xyz", "Incorrect last name."],
        ["name s'-urname email@email.xyz", "Incorrect last name."],
        ["name su-'rname email@email.xyz", "Incorrect last name."],
        ["name surname- email@email.xyz", "Incorrect last name."],
        ["name surname' email@email.xyz", "Incorrect last name."],
        ["name surnámé email@email.xyz", "Incorrect last name."],
        ["name surname emailemail.xyz", "Incorrect email."],
        ["name surname email@emailxyz", "Incorrect email."],
        ["name surname email@e@mail.xyz", "Incorrect email."]
    ]
    incorrect_points = ["", "-1 1 1 1", "1 1 2 A", "1 1 1", "1 1 1 1 1"]

    @dynamic_test(order=1)
    def test_and_exit(self):
        main = TestedProgram()
        output = main.start().lower()
        if len(output.split("\n")) < 2:
            return CheckResult.wrong("When started, your program "
                                     "should print at least one line "
                                     "and wait for input")

        if incorrect_string(output, "Learning Progress Tracker"):
            return CheckResult.wrong("When started, your program " +
                                     "should print \"Learning Progress Tracker\"")

        if main.is_waiting_input() is False:
            return CheckResult.wrong("After the start, your program should " +
                                     "be ready to accept commands from the user")
        output = main.execute("back")
        if main.is_waiting_input() is False:
            return CheckResult.wrong("Your program should keep running after the 'back' " +
                                     "command is entered")

        if any_missing_keywords(output, "enter", "exit", "program"):
            return CheckResult.wrong("When 'back' command is entered your program " +
                                     "should print the hint \"Enter 'exit' to exit the program\"")
        output = main.execute("exit")
        if any_missing_keywords(output, "bye"):
            return CheckResult.wrong("When the 'exit' command is entered, " +
                                     "your program should say bye to the user")
        if not main.is_finished():
            return CheckResult.wrong("After the 'exit' command has been entered, " +
                                     "your program should stop working")

        return CheckResult.correct()

    @dynamic_test(order=2, data=blanket_input)
    def test_blanket_input(self, input: str):
        main = TestedProgram()
        main.start()
        output = main.execute(input)

        if incorrect_string(output, "no input"):
            return CheckResult.wrong("When the user enters an empty or blank " +
                                     "string, your program should print \"No input\"")

        return CheckResult.correct()

    @dynamic_test(order=3, data=unknown_commands)
    def test_unknown_command(self, input: str):
        main = TestedProgram()
        main.start()

        output = main.execute(input)
        if any_missing_keywords(output, "unknown", "command"):
            return CheckResult.wrong("When an unknown command is entered, your " +
                                     "program should display an error message: \"Unknown command!\"")

        return CheckResult.correct()

    @dynamic_test(order=4)
    def test_add_students_1(self):
        main = TestedProgram()
        main.start()

        output = main.execute("add students")
        if any_missing_keywords(output,
                                "enter", "student", "credentials", "back", "return"):
            return CheckResult.wrong("When 'add students' command is entered, your " +
                                     "program should display the prompt \"Enter student credentials or " +
                                     "'back' to return.\"")

        output = main.execute("exit")
        if any_missing_keywords(output, "incorrect", "credentials"):
            return CheckResult.wrong("Expected output: \"Incorrect credentials.\", " +
                                     "but your output was: " + output)

        output = main.execute("back")
        if any_missing_keywords(output, "total", "0", "students", "added"):
            return CheckResult.wrong("Expected: \"Total 0 students were added\", but " +
                                     "your output was: " + output)

        output = main.execute("back")
        if any_missing_keywords(output, "enter", "exit", "program"):
            return CheckResult.wrong("When 'back' command is entered your program " +
                                     "should stop waiting for student credentials")

        output = main.execute("exit")
        if any_missing_keywords(output, "bye"):
            return CheckResult.wrong("When the 'exit' command is entered, " +
                                     "your program should say bye to the user")

        if not main.is_finished():
            return CheckResult.wrong("After the 'exit' command has been entered, " +
                                     "your program should stop working")

        return CheckResult.correct()

    @dynamic_test(order=5)
    def test_add_student_2(self):
        main = TestedProgram()
        main.start()
        main.execute("add students")

        for input in self.correct_credentials:
            output = main.execute(input)
            if any_missing_keywords(output, "student", "added"):
                return CheckResult.wrong("Expected output: \"Student has been added.\", but your " +
                                         "output was: " + output)
        output = main.execute("back")
        if any_missing_keywords(output, "total", "10", "students", "added"):
            return CheckResult.wrong("Expected: \"Total 10 students have been added\", but " +
                                     "your output was: " + output)

        return CheckResult.correct()

    @dynamic_test(order=6)
    def test_add_students3(self):
        main = TestedProgram()
        main.start()
        main.execute("add students")

        for args in self.incorrect_credentials:
            output = main.execute(args[0])
            if incorrect_string(output, args[1]):
                main.stop()
                return CheckResult.wrong("Expected output: \"" + args[1] + "\", but your " +
                                         "output was: " + output)
        output = main.execute("back")
        if any_missing_keywords(output, "total", "0", "students", "added"):
            return CheckResult.wrong("Expected: \"Total 0 students have been added\", but " +
                                     "your output was: " + output)
        return CheckResult.correct()

    @dynamic_test(order=7)
    def test_find_all_1(self):
        main = TestedProgram()
        main.start()
        main.execute("add students")
        main.execute("back")

        output = main.execute("list")
        if any_missing_keywords(output, "no", "found"):
            return CheckResult.wrong("Expected: \"No students found.\", but " +
                                     "your output was: " + output)

        return CheckResult.correct()

    @dynamic_test(order=8)
    def test_add_doubles(self):
        main = TestedProgram()
        main.start()
        main.execute("add students")

        credentials = get_random_credentials(12)
        for arg in credentials:
            output = main.execute(arg)
            if any_missing_keywords(output, "student", "added"):
                return CheckResult.wrong("Expected output: \"The student has been added.\", but your " +
                                         "output was: " + output)
            output = main.execute(arg)
            if any_missing_keywords(output, "this", "email", "already", "taken"):
                return CheckResult.wrong("Expected output: \"This email is already taken.\", but your " +
                                         "output was: " + output)

        output = main.execute("back")
        if any_missing_keywords(output, "total", str(len(credentials)), "students", "added"):
            return CheckResult.wrong(
                "Expected: \"Total " + str(len(credentials)) + "students have been added.\", but " +
                "your output was: " + output)

        return CheckResult.correct()

    @dynamic_test(order=9)
    def test_find_all_2(self):
        main = TestedProgram()
        main.start()
        main.execute("add students")

        credentials = get_random_credentials(12)
        for arg in credentials:
            output = main.execute(arg)
            if any_missing_keywords(output, "student", "added"):
                return CheckResult.wrong("Expected output: \"The student has been added.\", but your " +
                                         "output was: " + output)
        output = main.execute("back")
        if any_missing_keywords(output, "total", str(len(credentials)), "students", "added"):
            return CheckResult.wrong(
                "Expected: \"Total " + str(len(credentials)) + "students have been added.\", but " +
                "your output was: " + output)
        output = main.execute("list")
        if "students" not in output.split("\n")[0].lower():
            return CheckResult.wrong(
                "Expected the header \"Students:\" but your first line was: " + output.split("\n")[0])

        ids = parse_ids(output)
        array = np.array(ids)
        unique_ids = np.unique(array)

        if unique_ids.size != len(ids):
            return CheckResult.wrong("Expected " + str(len(ids)) +
                                     " unique IDs but found only " + unique_ids.size())
        return CheckResult.correct()

    @dynamic_test(order=10)
    def test_back_from_add_point(self):
        main = TestedProgram()
        main.start()

        output = main.execute("add points")
        if any_missing_keywords(output, "enter", "id", "points", "back", "return"):
            return CheckResult.wrong("When 'add points' command is entered, your program should print " +
                                     "\"Enter an id and points or 'back' to return:\" but your output was: " + output)

        main.execute("back")
        output = main.execute("back")
        if any_missing_keywords(output, "enter", "exit", "program"):
            return CheckResult.wrong("When 'back' command is entered your program " +
                                     "should stop waiting for student id and points")

        output = main.execute("exit")
        if any_missing_keywords(output, "bye"):
            return CheckResult.wrong("When the 'exit' command is entered, " +
                                     "your program should say bye to the user")

        if not main.is_finished():
            return CheckResult.wrong("After the 'exit' command has been entered, " +
                                     "your program should stop working")
        return CheckResult.correct()

    @dynamic_test(order=11)
    def test_student_point_1(self):
        main = TestedProgram()
        main.start()
        main.execute("add students")

        credentials = get_random_credentials(6)
        for arg in credentials:
            main.execute(arg)

        main.execute("back")
        output = main.execute("list")
        ids = parse_ids(output)

        main.execute("add points")
        for point in self.incorrect_points:
            output = main.execute(ids[0] + " " + point)
        if any_missing_keywords(output, "incorrect", "points", "format"):
            return CheckResult.wrong("Expected output: \"Incorrect points format.\", " +
                                     "but your output was: " + output)

        output = main.execute("imsurethereisnosuchstudentid 1 1 1 1")
        if any_missing_keywords(output, "no", "student", "found") or "imsurethereisnosuchstudentid" not in output:
            return CheckResult.wrong("Expected output was: \"No student is found " +
                                     "for id=imsurethereisnosuchstudentid\", but your output was: " + output)

        return CheckResult.correct()

    @dynamic_test(order=12)
    def test_student_points_2(self):
        main = TestedProgram()
        main.start()
        main.execute("add students")

        credentials = get_random_credentials(6)
        for arg in credentials:
            main.execute(arg)

        main.execute("back")
        output = main.execute("list")
        ids = parse_ids(output)

        main.execute("add points")
        points = get_correct_points(6)
        for i in range(len(points) - 1):
            output = main.execute(ids[i] + " " + points[i])
            if any_missing_keywords(output, "points", "updated"):
                return CheckResult.wrong("Expected \"Points updated.\" but your output was " + output)

        return CheckResult.correct()

    @dynamic_test(order=13)
    def test_back_from_find(self):
        main = TestedProgram()
        main.start()
        output = main.execute("find")
        if any_missing_keywords(output, "enter", "id", "back", "return"):
            return CheckResult.wrong("When 'find' command is entered, you program should " +
                                     "print \"Enter an id or 'back' to return:\", but your output was: " + output)

        main.execute("back")
        output = main.execute("back")
        if any_missing_keywords(output, "enter", "exit", "program"):
            return CheckResult.wrong("When 'back' command is entered your program " +
                                     "should stop waiting for student id")

        output = main.execute("exit")
        if any_missing_keywords(output, "bye"):
            return CheckResult.wrong("When the 'exit' command is entered, " +
                                     "your program should say bye to the user")

        if not main.is_finished():
            return CheckResult.wrong("After the 'exit' command has been entered, " +
                                     "your program should stop working")
        return CheckResult.correct()

    @dynamic_test(order=14)
    def test_find_by_id(self):
        main = TestedProgram()
        main.start()
        output = main.execute("add students")

        credentials = get_random_credentials(5)
        for arg in credentials:
            main.execute(arg)
        main.execute("back")
        output = main.execute("list")
        ids = parse_ids(output)

        main.execute("add points")
        for i in range(len(ids)):
            main.execute("{} {} {} {} {}".format(ids[i], i, i, i, i))
            main.execute("{} {} {} {} {}".format(ids[i], i, i, i, i))

        main.execute("back")
        output = main.execute("find")
        if any_missing_keywords(output, "enter", "id", "back", "return"):
            return CheckResult.wrong("When 'find' command is entered, you program should " +
                                     "print \"Enter an id or 'back' to return:\", but your output was: " + output)

        for i in range(len(ids)):
            output = main.execute(ids[i])
            expected = "{} points: Python={}; DSA={}; Databases={}; Flask={}".format(ids[i], i * 2, i * 2, i * 2, i * 2)
            if incorrect_string(output, expected):
                return CheckResult.wrong("Expected output: " + expected +
                                         ", but your output was: " + output)

        return CheckResult.correct()

    @dynamic_test(order=15)
    def test_back_from_statistics(self) -> CheckResult:
        main = TestedProgram()
        main.start()
        output = main.execute("statistics")
        main.execute("back")
        output = main.execute("back")
        if any_missing_keywords(output, "enter", "exit", "program"):
            return CheckResult.wrong("When 'back' command is entered your program " +
                                     "should stop waiting for student id")
        output = main.execute("exit")
        if any_missing_keywords(output, "bye"):
            return CheckResult.wrong("When the 'exit' command is entered, " +
                                     "your program should say bye to the user")

        if not main.is_finished():
            return CheckResult.wrong("After the 'exit' command has been entered, " +
                                     "your program should stop working")
        return CheckResult.correct()

    @dynamic_test(order=16)
    def test_statistics_1(self) -> CheckResult:
        main = TestedProgram()
        main.start()

        output = main.execute("statistics")
        lines = output.split("\n")
        lines = [i for i in lines if i]
        feedback = "When the \"statistics\" command is entered, your " \
                   "program must print: \"Type the name of a course to see details or 'back' " \
                   "to quit:\", but your output was: "
        if len(lines) == 0:
            return CheckResult.wrong(feedback)

        if any_missing_keywords(lines[0], "course", "details", "back", "quit"):
            return CheckResult.wrong(feedback + lines[0])

        if len(lines) < 7:
            return CheckResult.wrong("Your program should print a header and 6 " +
                                     "categories, but you printed only " + str(len(lines)) + " lines")

        categories = ["Most popular: n/a", "Least popular: n/a",
                      "Highest activity: n/a", "Lowest activity: n/a", "Easiest course: n/a",
                      "Hardest course: n/a"]

        for i in range(len(categories)):
            if incorrect_string(lines[i + 1], categories[i]):
                return CheckResult.wrong("Expected: " + categories[i] +
                                         ", but your output was " + lines[i + 1])

        return CheckResult.correct()

    @dynamic_test(order=17)
    def test_statistics_2(self) -> CheckResult:
        main = TestedProgram()
        main.start()
        main.execute("statistics")

        courses = ["Python", "DSA", "Databases", "Flask"]
        for course in courses:
            output = main.execute(course)
            lines = output.split("\n")
            if len(lines) < 2:
                return CheckResult.wrong("Expected 2 lines, but your output was only " + str(len(lines)) + " lines.")
            if incorrect_string(lines[0], course.lower()):
                return CheckResult.wrong("Your first line should be " + course + ", but your output was " + lines[0])
            if any_missing_keywords(lines[1], "id", "points", "completed"):
                return CheckResult.wrong("Your second line should be \"id\tpoints\tcompleted\", " +
                                         "but your output was " + lines[1])
        unknown = [c for c in self.unknown_commands if c.casefold() not in courses]
        for course in unknown:
            output = main.execute(course)
            if incorrect_string(output, "unknown course"):
                return CheckResult.wrong("Expected output: \"Unknown course.\", but your output was: " + output)

        return CheckResult.correct()

    @dynamic_test(order=18)
    def test_statistics_3(self) -> CheckResult:
        main = TestedProgram()
        main.start()
        main.execute("statistics")

        main.execute("back")
        if main.is_waiting_input() is False:
            return CheckResult.wrong("Your program should keep running after the 'back' "
                                     "command is entered")

        output = main.execute("back")
        if any_missing_keywords(output, "enter", "exit", "program"):
            return CheckResult.wrong("When 'back' command is entered your program "
                                     "should print the hint \"Enter 'exit' to exit the program.\"")

        output = main.execute("exit")
        if any_missing_keywords(output, "bye"):
            return CheckResult.wrong("When the 'exit' command is entered, "
                                     "your program should say bye to the user")

        if not main.is_finished():
            return CheckResult.wrong("After the 'exit' command has been entered, "
                                     "your program should stop working")
        return CheckResult.correct()

    @dynamic_test(order=19)
    def test_categories_1(self) -> CheckResult:
        main = TestedProgram()
        main.start()
        main.execute("add students")

        credentials = get_random_credentials(4)
        for c in credentials:
            main.execute(c)

        main.execute("back")
        output = main.execute("list")
        ids = parse_ids(output)

        main.execute("add points")
        for id in ids:
            main.execute("{} 5 4 3 1".format(id))

        main.execute("back")
        output = main.execute("statistics")
        lines = output.splitlines()
        output_string = ""
        if len(lines) != 7:
            output_string = ''.join([line + "\n" for line in lines])
            return CheckResult.wrong("Expected header: "
                                     "Type the name of a course to see details or 'back' to quit "
                                     "and six lines with the following information: "
                                     "Most popular, Least popular, Highest activity, Lowest activity, Easiest course, "
                                     "Hardest course, but your output was: " + output_string)
        if any_missing_keywords(lines[1], "python", "dsa", "databases", "flask"):
            return CheckResult.wrong("Expected most popular: Python, DSA, Databases, Flask, "
                                     "but your output was: " + lines[1])
        if "n/a" not in lines[2].lower():
            return CheckResult.wrong("Expected least popular: n/a, "
                                     "but your output was: " + lines[2])

        if any_missing_keywords(lines[3], "python", "dsa", "databases", "flask"):
            return CheckResult.wrong("Expected top activity: Python, DSA, Databases, Flask, " +
                                     "but your output was: " + lines[3])

        if "n/a" not in lines[4].lower():
            return CheckResult.wrong("Expected lowest activity: n/a, "
                                     "but your output was: " + lines[4])

        if any_missing_keywords(lines[5], "python"):
            return CheckResult.wrong("Expected easiest course: Python, " +
                                     "but your output was: " + lines[5])

        if any_missing_keywords(lines[6], "flask"):
            return CheckResult.wrong("Expected hardest course: Flask, "
                                     "but your output was: " + lines[6])

        return CheckResult.correct()

    @dynamic_test(order=20)
    def test_categories_2(self) -> CheckResult:
        main = TestedProgram()
        main.start()
        main.execute("add students")

        credentials = get_random_credentials(4)
        for c in credentials:
            main.execute(c)

        main.execute("back")
        output = main.execute("list")
        ids = parse_ids(output)

        main.execute("add points")
        main.execute("{} 10 10 10 10".format(ids[0]))
        main.execute("{} 5 5 5 5".format(ids[1]))
        main.execute("{} 5 5 5 5".format(ids[2]))
        main.execute("{} 2 2 2 2".format(ids[3]))

        main.execute("back")
        main.execute("statistics")

        lines_python = main.execute("Python").splitlines()
        lines_dsa = main.execute("DSA").splitlines()
        lines_db = main.execute("Databases").splitlines()
        lines_flask = main.execute("Flask").splitlines()

        if check_lines_1(lines_python, ids):
            return CheckResult.wrong("Your Python student list either contains incorrect data or is incorrectly sorted")
        if check_lines_2(lines_dsa, ids):
            return CheckResult.wrong("Your DSA student list either contains incorrect data or is incorrectly sorted")
        if check_lines_3(lines_db, ids):
            return CheckResult.wrong("Your Databases student list either contains incorrect data "
                                     "or is incorrectly sorted")
        if check_lines_4(lines_flask, ids):
            return CheckResult.wrong("Your Flask student list either contains incorrect data "
                                     "or is incorrectly sorted")

        return CheckResult.correct()

    @dynamic_test(order=21)
    def test_categories_3(self) -> CheckResult:
        main = TestedProgram()
        main.start()
        main.execute("add students")

        main.execute("John Doe johnd@email.net")
        main.execute("Jane Spark jspark@yahoo.com")
        main.execute("back")

        output = main.execute("list")
        ids = parse_ids(output)
        lines = output.splitlines()

        main.execute("add points")
        main.execute("{} 8 7 7 5".format(ids[0]))
        main.execute("{} 7 6 9 7".format(ids[0]))
        main.execute("{} 6 5 5 0".format(ids[0]))
        main.execute("{} 8 0 8 6".format(ids[1]))
        main.execute("{} 7 0 0 0".format(ids[1]))
        main.execute("{} 9 0 0 5".format(ids[1]))

        main.execute("back")
        main.execute("statistics")

        lines_python = main.execute("Python").splitlines()
        lines_dsa = main.execute("DSA").splitlines()
        lines_db = main.execute("Databases").splitlines()
        lines_flask = main.execute("Flask").splitlines()

        if (not re.match(".+\\s+24\\s+4\\.0\\s?%.*", lines_python[2]) or
                not re.match(".+\\s+21\\s+3\\.5\\s?%.*", lines_python[3]) or
                not lines_python[2].startswith(ids[1]) or not lines_python[3].startswith(ids[0])):
            return CheckResult.wrong("Your Python student list either contains incorrect data or is incorrectly sorted")

        if not re.match(".+\\s+18\\s+4\\.5\\s?%.*", lines_dsa[2]) or not lines_dsa[2].startswith(ids[0]):
            return CheckResult.wrong("Your DSA student list either contains incorrect data or is incorrectly sorted")

        if (not re.match(".+\\s+21\\s+4\\.4\\s?%.*", lines_db[2]) or
                not re.match(".+\\s+8\\s+1\\.7\\s?%.*", lines_db[3]) or
                not lines_db[2].startswith(ids[0]) or not lines_db[3].startswith(ids[1])):
            return CheckResult.wrong("Your Databases student list either contains incorrect data "
                                     "or is incorrectly sorted")

        if (not re.match(".+\\s+12\\s+2\\.2\\s?%.*", lines_flask[2]) or
                not re.match(".+\\s+11\\s+2\\.0\\s?%.*", lines_flask[3]) or
                not lines_flask[2].startswith(ids[0]) or not lines_flask[3].startswith(ids[1])):
            return CheckResult.wrong("Your Flask student list either contains incorrect data "
                                     "or is incorrectly sorted")

        return CheckResult.correct()

    @dynamic_test(order=22)
    def test_notification_1(self) -> CheckResult:
        main = TestedProgram()
        main.start()

        output = main.execute("notify")
        lines = output.splitlines()
        all_match = True
        for line in lines:
            if not any_missing_keywords(line, "total", "0", "notified"):
                all_match = False
                break
        if all_match:
            CheckResult.wrong("Expected output was \"Total 0 students have been notified.\", "
                              "but your output was: " + output)

        return CheckResult.correct()

    @dynamic_test(order=23)
    def test_notification_2(self) -> CheckResult:
        main = TestedProgram()
        main.start()

        main.execute("add students")
        main.execute("John Doe johnd@email.net")
        main.execute("Jane Spark jspark@yahoo.com")
        main.execute("back")

        output = main.execute("list")
        lines = output.splitlines()
        ids = parse_ids(output)

        main.execute("add points")
        main.execute("{} 600 400 0 0".format(ids[0]))
        main.execute("back")

        output = main.execute("notify")
        lines = output.splitlines()

        if(not lines[0].lower().startswith("to:") or
           "johnd@email.net" not in lines[0].lower() or
           not lines[1].lower().startswith("re:") or
           any_missing_keywords(lines[1],"learning", "progress") or
           any_missing_keywords(lines[2],"john", "doe", "accomplished") or
           "python" not in lines[2].lower() and "python" in lines[5].lower()):
            return CheckResult.wrong("You program should have printed the following:\nTo: johnd@email.net\n" +
                                     "Re: Your Learning Progress\nHello, John Doe! You have accomplished our Python "
                                     "course!\nbut your output was: \n" + output)

        if (not lines[3].lower().startswith("to:") or
                "johnd@email.net" not in lines[3].lower() or
                not lines[4].lower().startswith("re:") or
                any_missing_keywords(lines[4], "learning", "progress") or
                any_missing_keywords(lines[5], "john", "doe", "accomplished") or
                "dsa" not in lines[2].lower() and "dsa" not in lines[5].lower()):
            return CheckResult.wrong("You program should have printed the following:\nTo: johnd@email.net\n" +
                                     "Re: Your Learning Progress\nHello, John Doe! You have accomplished our Python "
                                     "course!\nbut your output was: \n" + output)

        if any_missing_keywords(lines[6].lower(), "total", "1", "notified"):
            return CheckResult.wrong(
                "Expected output was \"Total 1 student has been notified.\", but your output was: \n" +
                output)

        for line in lines:
            if "jane" in line or "spark" in line or "jspark@yahoo.com" in line:
                return CheckResult.wrong("Your notification should not mention Jane Spark")

        output = main.execute("notify")
        lines = output.splitlines()
        all_match = False
        for line in lines:
            if not any_missing_keywords(line, "total", "0", "notified"):
                all_match = True
                break
        if not all_match:
            return CheckResult.wrong("Expected output was \"Total 0 students have been notified\", " +
                                     "but your output was: " + output)

        return CheckResult.correct()


if __name__ == '__main__':
    LearningProgressTrackerTest().run_tests()
