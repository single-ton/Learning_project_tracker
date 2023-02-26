from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import *
import re
import random
from hstest.testing.tested_program import TestedProgram
import numpy as np

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


def any_missing_keywords(output: str, *keywords):
    tokens = re.split("\\W+", output.lower())
    return not all(el in tokens for el in keywords)


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
    return names[1:n]


def generate_emails(n: int):
    emails = []
    for i in range(1, n):
        emails.append("address" + str(i) + "@mail.com")
    return emails


def get_random_credentials(n: int):
    credentials = []
    names = generate_names(n)
    emails = generate_emails(n)
    for i in range(1, n-1):
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
        #["námé surname email@email.xyz", "Incorrect first name."],
        ["name s email@email.xyz", "Incorrect last name."],
        ["name -surname email@email.xyz", "Incorrect last name."],
        ["name 'surname email@email.xyz", "Incorrect last name."],
        ["name surnam''e email@email.xyz", "Incorrect last name."],
        ["name surn--ame email@email.xyz", "Incorrect last name."],
        ["name s'-urname email@email.xyz", "Incorrect last name."],
        ["name su-'rname email@email.xyz", "Incorrect last name."],
        ["name surname- email@email.xyz", "Incorrect last name."],
        ["name surname' email@email.xyz", "Incorrect last name."],
        #["name surnámé email@email.xyz", "Incorrect last name."],
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
            return CheckResult.wrong("Expected the header \"Students:\" but your first line was: " + output.split("\n")[0])

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
        for i in range(len(points)-1):
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
            expected = "{} points: Java={}; DSA={}; Databases={}; Spring={}".format(ids[i], i * 2, i * 2, i * 2, i * 2)
            if incorrect_string(output, expected):
                return CheckResult.wrong("Expected output: " + expected +
                                         ", but your output was: " + output)

        return CheckResult.correct()

if __name__ == '__main__':
    LearningProgressTrackerTest().run_tests()
