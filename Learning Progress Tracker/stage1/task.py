# Write your code here
print("Learning progress tracker")
input1 = input()
if input1 in ["\n", "", " ", "\t", " \t"]:
    print("No input.")
elif input1 == "exit":
    print("Bye!")
    exit(0)
else:
    print("Error: unknown command!")
