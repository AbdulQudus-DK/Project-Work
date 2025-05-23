
import json

#How Inputs were added

def add_person():
    name = input("Name: ")
    age = input("Age: ")
    email = input("Email: ")

    person = {"name": name, "age": age, "email": email}
    return person

def display_people(people):
    for i, person in enumerate(people):
        print(i + 1, "-", person["name"], "|", person["age"], "|", person["email"])

def delete_contact(people):
    display_people(people)

    while True:
        number = input("Enter a number to delete: ")
        try:
            number = int(number)
            if number == 0 or number > len(people):
                print("Invalid number or out of range.")
            else:
                break
        except:
            print("Invalid number.")

    people.pop(number -1)

def search(people):
    search_name = input("Search name: ").lower()
    results = []

    for person in people:
        name = person["name"]
        if search_name in name.lower():
            results.append(person)

    display_people(results)


print("Hello, Welcome to Information Management Sysytem.")
print()

with open("Contacts.json", "r") as f:
    people = json.load(f)["Contacts"]


while True:
    print()
    print("Contact list size:", len(people))
    command = input("You can 'ADD', 'DELETE' or 'SEARCH', 'Q' for quit: ").lower()

    if command == "add":
        person = add_person()
        people.append(person)
        print("Person Added")
    elif command == "delete":
        delete_contact(people)
    elif command == "search":
        search(people)
    elif command == "q":
        break
    else:
        print("Invalid Command")


with open("Contacts.json", "w") as f:
    json.dump({"Contacts": people}, f)

    print(people)






