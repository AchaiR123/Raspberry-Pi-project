#simple service desk program for help
found=""
print("Welcome to the service desk\n\n\t")
def loop():
    print("How can we assist you today?")
    userInput = str(input(""))
    userInput = userInput.lower()
    if userInput in["navigate", "help","navigating","stuck"]:
        print("press \033ctrl+shift+f1\033\n\nTo navigate to the help menu")
        return()
    elif userInput in["stop"]:
        break()
    elif userInput in ["overheating", "over heating"]: 
        print("Your PI")
        return()
    elif userInput in ["work","apps","applications","app","application"]:
        print("Here is the PI OS manual https://www.bing.com/ck/a?!&&p=\
              eeac646b829d2ec4Jml\
              tdHM9MTcxNTI5OTIwMCZpZ3VpZD0zNGE1NmMwN\
              C1iY2MwLTZkOTQtMTZjNi03ODc3YmQwYjZjMG\
              ImaW5zaWQ9NTIwNA&ptn=3&ver=2&h\
              sh=3&fclid=34a56c04-bcc0-6d94-16c6-7877bd0b6c\
              0b&psq=pi+os+manua\
              l&u=a1aHR0cHM6Ly93d3cucmFzcGJlcnJ5cGkuY29tL2RvY3V\
              tZW50YXRpb24vcmFzcGJpYW4v&ntb=1")
        return()
    else:
        print("Sorry,\nWe can't help you!\n\n\nMake sure you spelled it correctly!\n\n\tsay \"stop\" to end the program.\n")
        return loop()

loop()

