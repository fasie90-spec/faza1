# Phonebook CLI
import json

contacts = {}

def add_contact(name, phone):
    contacts[name] = phone

def delete_contact(name):
    contacts.pop(name)

def search_contact(name):
    print(f"Name: {name} | Phone: {contacts[name]}")

def show_all():
    if not contacts:
        print("Your contacts list is empty!")
        return
    for i, (name, phone) in enumerate(sorted(contacts.items()), start=1):
        print(f"{i}. Name: {name} | Phone: {phone}")

def menu():
    load_from_json()
    while True:
        print("\n1. Add contact")
        print("2. Delete contact")
        print("3. Search contact")
        print("4. Show all")
        raspuns = input("What do you want me to do?")

        if raspuns == "1":
            name_input = input("What's the name of the person to add?")
            if name_input in contacts:
                print("You already have a contact with this name!")
                continue
            phone_input = input("What's the number of the person?")
            if phone_input in set(contacts.values()):
                print("You already have this number saved!")
                continue
            add_contact(name_input, phone_input)
            print(f"You've added {name_input} to your contacts list!")
            save_to_json()
        elif raspuns == "2":
            delete_input = input("What's the name of the contact you want to delete?")
            if delete_input not in contacts:
                print("You dont have this contact registred!")
                continue
            delete_contact(delete_input)
            print(f"You deleted {delete_input} from your contacts list!")
            save_to_json()
        elif raspuns == "3":
            search_input = input("What contact are you looking for?")
            if search_input not in contacts:
                print("You dont have this contact registred!")
                continue
            search_contact(search_input)
        elif raspuns == "4":
            show_all()

def save_to_json():
    with open("contacts.json", "w") as f:
        json.dump(contacts, f)
    print("Contacts saved!")

def load_from_json():
    global contacts
    try:
        with open("contacts.json", "r") as f:
            contacts = json.load(f)
        print("Contacts load!")
    except FileNotFoundError:
        print("No contacts to load!")


if __name__ == "__main__":
    menu()
