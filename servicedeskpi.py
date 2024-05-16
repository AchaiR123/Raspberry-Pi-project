# Simple service desk program for the Raspberry PI
welcome = "How can we assist you today?"   
found = ""
print("Welcome to the service desk\n\n\t")

def loop():
    global welcome  # Declare 'welcome' as global to modify it within the function
    print(welcome)
    userInput = str(input(""))
    userInput = userInput.lower()
    if userInput in ["navigate", "help", "navigating", "stuck"]:
        print("Press \033[ctrl+shift+f1\033[0m\n\nTo navigate to the help menu")
        welcome = "How else can we assist you today?"
        loop()
    elif userInput in ["stop"]:
        print("OK")
    elif userInput in ["overheating", "over heating"]: 
        print("Don't worry, this issue happened to us! You could:\n\n\t• Put the Pi in an air conditioning unit,\n\n\t• Get a new Pi, or\n\n\t• Replace the overheated parts\n")
        welcome = "How else can we assist you today?"
        loop()
    elif userInput in ["work", "apps", "applications", "app", "application"]:
        print("Here is the Pi OS manual: https://www.bing.com/ck/a?!&&p=\
              eeac646b829d2ec4Jml\
              tdHM9MTcxNTI5OTIwMCZpZ3VpZD0zNGE1NmMwN\
              C1iY2MwLTZkOTQtMTZjNi03ODc3YmQwYjZjMG\
              ImaW5zaWQ9NTIwNA&ptn=3&ver=2&h\
              sh=3&fclid=34a56c04-bcc0-6d94-16c6-7877bd0b6c\
              0b&psq=pi+os+manua\
              l&u=a1aHR0cHM6Ly93d3cucmFzcGJlcnJ5cGkuY29tL2RvY3V\
              tZW50YXRpb24vcmFzcGJpYW4v&ntb=1")
        welcome = "How else can we assist you today?"
        loop()
    else:
        print("Sorry,\nWe can't help you!\n\n\nMake sure you spelled it correctly!\n\n\tsay \"stop\" to end the program.\n")
        welcome = "How else can we assist you today?"
        loop()

loop()
