from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import *
import re
from hstest.testing.tested_program import TestedProgram

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


def any_missing_keywords(output: str, *keywords):
    tokens = re.split("\\W+", output.lower())
    return not all(el in tokens for el in keywords)


def incorrect_string(output: str, model: str):
    normalized_output = re.sub("\\W+", "", output).lower()
    normalized_model = re.sub("\\W+", "", model).lower()
    return not normalized_output in normalized_model


class LearningProgressTrackerTest(StageTest):
    blanket_input = ["", " ", "\t", " \t"]
    unknown_commands = ["abc", "quit", "  brexit ", "exi  t", "help", "break",
                        "-help", "Ctrl+C", "exit please", ":q"]

    @dynamic_test
    def test_and_exit(self):
        main = TestedProgram()
        output = main.start().lower()
        if len(output.split("\n")) < 2:
            return CheckResult.wrong("When started, your program "
                                     "should print at least one line "
                                     "and wait for input")

        if incorrect_string(output, "learning progress tracker"):
            return CheckResult.wrong("When started, your program " +
                                     "should print \"Learning Progress Tracker\"")

        if main.is_waiting_input() is False:
            return CheckResult.wrong("After the start, your program should " +
                                     "be ready to accept commands from the user")
        output = main.execute("exit")
        if any_missing_keywords(output, "bye"):
            return CheckResult.wrong("When the 'exit' command is entered, " +
                                     "your program should say bye to the user")
        if not main.is_finished():
            return CheckResult.wrong("After the 'exit' command has been entered, " +
                                     "your program should stop working")

        return CheckResult.correct()

    @dynamic_test(data=blanket_input)
    def test_blanket_input(self, input: str):
        main = TestedProgram()
        main.start()
        output = main.execute(input)

        if incorrect_string(output, "no input"):
            return CheckResult.wrong("When the user enters an empty or blank " +
                                     "string, your program should print \"No input\"")

        return CheckResult.correct()

    @dynamic_test(data=unknown_commands)
    def test_unknown_command(self, input: str):
        main = TestedProgram()
        main.start()
        output = main.execute(input)
        if any_missing_keywords(output, "unknown", "command"):
            return CheckResult.wrong("When an unknown command is entered, your " +
                                     "program should display an error message: \"Unknown command!\"")

        return CheckResult.correct()


if __name__ == '__main__':
    LearningProgressTrackerTest().run_tests()
