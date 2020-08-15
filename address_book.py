#address_book.py

#features: add (done), modify (done), delete (done), search,
#search by tag (done), tag contacts (done)

#contact format: contact can be large dict, with key (name) linking to
#new contact object containing fields for data and methods for
#modifiying data (done)

#must store contact list using pickle (done)

import pickle
from os import system

contacts_list = None
contacts_file = None
new_file = False
user_input = None

def clear_screen(): system("cls")

def retry_sequence(func):
    """A decorator used to repeat a function consisting of a sequence of events.
    
    The function should usually be a string of inputs with some
    processing in it, so if the user enters invalid/bad data,
    they are prompted to repeat the inputs but put valid data in
    this time.
    """
    def wrapper_function(self=None): 
        #ugly default None parameter present because decorator is also used for some class methods
        while True:
            try:
                result = func(self)
            except DataFormatError as dfe:
                print("\nPlease enter {} in the {} field.\n".format(dfe.wanted_type,dfe.field))
            except BaseException:
                print("\nSorry, something appears to have gone wrong. Please try again.\nMake sure to enter the correct type of information for that input, and not to use any special characters.\n")
            else:
                return result
                break
    return wrapper_function 

def request_contact_info(quickfix=None):
    """Uses inputs to take information about the contact from users, then makes a returns a  Contact object with them.
    
    The function is decorated with the retry_sequence function to make sure 
    that any errors in data entry are corrected by the user.
    """
    first_name=input("Please enter your contact's first name. Use alphabets of any case only, with no spaces.")
    last_name=input("Please enter your contact's last name. Use alphabets of any case only, with no spaces.")
    number=input("Please enter your contact's phone number. Use digits only.")
    email_address=input("Enter your contact's email address if you wish to. Otherwise, press Enter.")
    tags = request_tags()
    return Contact(first_name,last_name,number,email_address,*tags)
request_contact_info = retry_sequence(request_contact_info)

def create_new_contact():
    """Creates a new contact using the request_contact_info function.
    
    Basically, takes the output from that and then checks for duplicates
    in the contacts_list. If there aren't any, then it adds it.
    """
    new_contact = request_contact_info()
    if new_contact.full_name in contacts_list:
        print("\nSorry, you already have a contact with that name.\nTo change that contact's data, please 'view' it from the main screen, then select the option to modify it.\nThe original contact has not been modified.")
    else:
        contacts_list[new_contact.full_name] = new_contact
    del new_contact
    save_contacts_list_to_contacts_file()
    
def save_contacts_list_to_contacts_file():
    """Dumps the contacts_list dictionary to the contacts.data file using pickle.
    
    The function isn't called before the file is checked to exist, so
    no probllem with that. Check the code near #opening contacts file
    for a better explanation.
    """
    print("\nOpening contacts file to update contacts list...")
    contacts_file = open("contacts.data","wb")
    pickle.dump(contacts_list,contacts_file)
    print("\nContacts saved to file. Closing contacts file...")
    contacts_file.close()
    
def request_tags(quickfix=None):
    #ugly unused parameter included because otherwise I have to mess around with 'retry_sequence' to get it to work right
    """Used to request a list of tags using a certain selection method.
    
    Basically, the user can create a list of strings by adding strings
    (by just typing them in at the prompt and pressing Enter) or
    removing them (by just typing them in again.) The user can submit
    the list of strings by typing nothing and pressing Enter. The function
    will then pass a tuple containing the strings.
    """
    try:
        #to check if this has already been assigned a value before so that it can take it (can't add it as a parameter, because it'll probably screw something up with 'retry_sequence'
        #if not defined yet, defines it as an empty list
        modified_tags
    except NameError:
        modified_tags = list()
    while True:  
        print("These are the current tags you have selected: {}".format(modified_tags))
        user_input = input("Please enter a single tag that you would like to change. If the entered tag matches a tag that is already present, that tag will be removed from the contact. If the entered tag is not already associated with the contact, it will be added. If you have finished changing the tags, simply press Enter without typing anything.")
        clear_screen()
        if user_input == "":
            return tuple(modified_tags)
            break
        else:
            if user_input in modified_tags:
                del modified_tags[modified_tags.index(user_input)]
            else:
                modified_tags.append(user_input)
request_tags = retry_sequence(request_tags)


class DataFormatError(Exception):
    """An exception raised if the wrong data is entered in a contact's field."""
    def __init__(self,field,wanted_type):
        self.field = field
        self.wanted_type = wanted_type

class Contact():
    """Stores a contact and its information.
    
    Has methods for deleting and modifying itself.
    """
    def __init__(self,first_name,last_name,number,email_address="",*tags):
        if type(first_name) != str or not first_name.isalpha():
            raise DataFormatError("First name","alphabets only, no spaces")
        if type(last_name) != str or not last_name.isalpha():
            raise DataFormatError("Last name","alphabets only, no spaces")
        if not str(number).isdecimal():
            raise DataFormatError("Number","numbers only, no spaces or other symbols")
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = first_name + " " + last_name
        self.number = str(number)
        self.email_address = str(email_address)
        self.tags = tags
    
    def delete_self(self):
        """Removes itself from contacts list, then deletes itself, then saves contacts."""
        del contacts_list[self.full_name]
        del self
        save_contacts_list_to_contacts_file()
    
    def modify_self_except_tags(self):
        """Used to change data about the contact except for the tags (different fucntion)
        
        Is also decorated with retry_sequence. 
        Cannot use request_contact_info because prompts are different here
        (otherwise I could just take the info straight from the created contact info)
        """
        first_name=input("Please enter your contact's first name. Use alphabets of any case only, with no spaces. If you do not wish to change this, simply press Enter.")
        last_name=input("Please enter your contact's last name. Use alphabets of any case only, with no spaces. If you do not wish to change this, simply press Enter.")
        number=input("Please enter your contact's phone number. Use digits only. If you do not wish to change this, simply press Enter.")
        email_address=input("Enter your contact's email address if you wish to change it. Otherwise, press Enter.")
        new_full_name = first_name + " " + last_name
        if new_full_name in contacts_list:
            print("Sorry, a contact with that name already exists.")
        else:
            old_full_name = self.full_name
            if first_name != "":
                if type(first_name) != str or not first_name.isalpha():
                    raise DataFormatError("First name","alphabets only, no spaces")
                else: self.first_name = first_name
            if last_name != "":
                if type(last_name) != str or not last_name.isalpha():
                    raise DataFormatError("Last name","alphabets only, no spaces")
                else: self.last_name = last_name
            if number != "":
                if not str(number).isdecimal():
                    raise DataFormatError("Number","numbers only, no spaces or other symbols")
                else: self.number = number
            if email_address != "":
                self.email_address = email_address
            if new_full_name != " " and new_full_name != self.full_name:
                self.full_name = new_full_name
                contacts_list[self.full_name] = self
                del contacts_list[old_full_name]
            save_contacts_list_to_contacts_file()
    modify_self_except_tags = retry_sequence(modify_self_except_tags)
    
    def modify_tags(self,*tags_to_change):
        """Changes the tags of the contact by using the request_tags function."""
        modified_tags = list(self.tags)
        self.tags = tuple(request_tags())
        save_contacts_list_to_contacts_file()
    
    def display_self(self):
        #might change this to __str__
        """Prints data about the contact in an orderly way."""
        print(self.full_name)
        print("-"*len(self.full_name))
        print("Number:", self.number)
        print("Email Address:", self.email_address)
        print("Tags: {}".format(self.tags))
        print("\n")

#opening contacts file
try:
    contacts_file = open("contacts.data","rb")
except FileNotFoundError: #if no file detected, create a new file
    print("\nNo contacts file detected, creating new contacts file...")
    contacts_list = dict()
    contacts_file = open("contacts.data","wb")
    pickle.dump(contacts_list,contacts_file)
    print("\nEmpty contacts file created. Closing file...")
    new_file = True #brand-new blank file, so make sure that it doesn't stay empty
    contacts_file.close()
else: #if file present, load info from it
    contacts_list = pickle.load(contacts_file) 
    print("\nContacts read from contacts file. Closing file...")
    contacts_file.close()
    
if new_file: #in case file is brand-new (and so blank)
    print("\nPlease enter a new contact to start the contacts list.")
    create_new_contact()

#main loop
while True:
    user_input = input("\nPlease enter a command word from the following list:\n'view', to view the details of a certain contact;\n'view all', to view all contacts;\n'search', to locate contacts;\n'new', to create a new contact;\nor 'exit', to exit the program.\n")
    clear_screen()
    if user_input == "exit":
        break
    elif user_input == "new":
        create_new_contact()
    elif user_input == "view all":
        for i in contacts_list:
            contacts_list[i].display_self()
    elif user_input == "view":
        user_input = input("Please enter the full name of the contact whose details you would like to view: ")
        if user_input in contacts_list:
            accessed_contact = contacts_list[user_input]
            print("Your contact has been found. Here are their details:")
            accessed_contact.display_self()
            user_input = input("\nEnter 'modify', to modify this contact';\n'delete', to delete this contact;\nor anything else to return to the main screen.\n")
            if user_input == "modify":
                accessed_contact.modify_self_except_tags()
                accessed_contact.modify_tags()
            if user_input == "delete":
                user_input = input("\nAre you sure you would like to delete this contact? Enter 'yes' if so, or anything else if not.\n")
                if user_input == "yes":
                    print("{}'s contact has been deleted.".format(accessed_contact.full_name))
                    accessed_contact.delete_self()
                    
        else:
            print("\nSorry, that contact couldn't be found.")
    elif user_input == "search":
        user_input = input("Please select the mode for your search:\nby 'name', where you can enter the first name, last name or full name of the contact you wish to find;\nor by 'tag', where you can enter one or more tags associated with the contact.\nEnter anything other than the other two options to return to the main screen.\n")
        clear_screen()
        if user_input == "name":
            user_input = input("Please enter the first name, last name OR full name of the contact you wish to locate. The input is case-sensitive.\n")
            print("\nSearching...")
            clear_screen()
            any_found = False
            for i in contacts_list:
                if user_input in (contacts_list[i].first_name,contacts_list[i].last_name,contacts_list[i].full_name):
                    contacts_list[i].display_self()
                    any_found = True
            if not any_found:
                print("Sorry, no contacts with that name could be found.")
        elif user_input == "tag":
            user_input = request_tags()
            clear_screen()
            any_found = False
            for i in contacts_list:
                if set(user_input).issubset(contacts_list[i].tags):
                    contacts_list[i].display_self()
                    any_found = True
            if not any_found:
                print("Sorry, no contacts with those tags could be found.")
        user_input = input("Press Enter to return to the main screen.")
    else:
        print("Sorry, that input is not recognised. Please try again.")
