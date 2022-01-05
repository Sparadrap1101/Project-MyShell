import os
import sys
import subprocess
import shlex


#### Section des Built-in commandes ####

    ## Exécuter ici en python pour les commandes LS, PWD et EXIT ##
def builtInCommand(commandList, display):
    if commandList[0] == 'cd':
        if len(commandList) == 1:
            path = os.getenv("HOME")
            os.chdir(path)

        elif len(commandList) == 2 and os.path.exists(commandList[1]):
            os.chdir(commandList[1])
        
        else:
            if display[0] == True:
                printError()

            else: # Write output in a file
                if commandList[display[1]].find(".") >= 0: # On vérifie si le fichier n'a pas déjà un suffixe
                    path = os.getcwd() + "/" + commandList[display[1]]

                else: # S'il n'a pas de suffixe on rajoute .txt par défaut
                    path = os.getcwd() + "/" + commandList[display[1]] + ".txt"

                file = open(path, 'w')
                msg = "An error has occurred"
                file.write(msg)
                file.close()

    elif commandList[0] == 'pwd':
        if display[0] == True:
            try:
                print(os.getcwd())

            except Exception as e:
                printError()
        
        else: # Write output in a file
            if commandList[display[1]].find(".") >= 0: # On vérifie si le fichier n'a pas déjà un suffixe
                path = os.getcwd() + "/" + commandList[display[1]]

            else: # S'il n'a pas de suffixe on rajoute .txt par défaut
                path = os.getcwd() + "/" + commandList[display[1]] + ".txt"

            file = open(path, 'w')
            try:
                msg = os.getcwd()

            except Exception as e:
                msg = "An error has occurred"
                
            file.write(msg)
            file.close()

    elif commandList[0] == 'exit':
        exit()

    else:
        if display[0] == True:
            printError()

        else: # Write output in a file
            if commandList[display[1]].find(".") >= 0: # On vérifie si le fichier n'a pas déjà un suffixe
                path = os.getcwd() + "/" + commandList[display[1]]

            else: # S'il n'a pas de suffixe on rajoute .txt par défaut
                path = os.getcwd() + "/" + commandList[display[1]] + ".txt"

            file = open(path, 'w')
            msg = "An error has occurred"
            file.write(msg)
            file.close()


#### Section Lien aux Programmes ####
def otherCommands(commandList, display):
    ## Faire le lien avec les programmes ici si ce n'est pas une Built-in commande ##
    realPath = ""
    pathList = os.environ["PATH"].split(os.pathsep)

    for path in pathList:
        path = os.path.join(path, commandList[0]) # Add our command at the end of the path 

        if os.path.isfile(path): # Check if this file exist
            realPath = path
        if os.path.isfile(path) and os.access(path, os.X_OK):
            realPath = path

    # Vérifier que le chemin à bien été trouvé avant de faire la suite
        # Si y'a des erreurs rediriger vers la section Erreurs #
    if realPath == "":
        if display[0] == True:
            printError()

        else: # Write output in a file
            if commandList[display[1]].find(".") >= 0: # On vérifie si le fichier n'a pas déjà un suffixe
                path = os.getcwd() + "/" + commandList[display[1]]

            else: # S'il n'a pas de suffixe on rajoute .txt par défaut
                path = os.getcwd() + "/" + commandList[display[1]] + ".txt"
                
            file = open(path, 'w')
            msg = "An error has occurred"
            file.write(msg)
            file.close()

    else: # Si le chemin de la commande à bien été trouvé on continue
        commandList[0] = realPath

        nomFichier = commandList[display[1]] # On récupère le nom du fichier dans lequel enregistrer le résultat si besoin
        if display[0] == False:
            index = display[1] - 1
            del commandList[index:] # On enlève [">", "nomFichier"] de la liste des commandes si on veut enregistrer dans un fichier (pour éviter un bug)

    ## Exécuter la commande grâce au chemin de la commande ##
        process = subprocess.Popen(commandList, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out, err = process.communicate() # On récupère les sorties
    
    ## Afficher le résultat ##
        # Laisser la possibilité d'afficher le résultat dans un fichier si souhaité #
        if display[0] == True:
            if process.returncode == 0: # Si tout à bien fonctionné on affiche l'output
                print("{}".format(out))
            else:                       # Sinon on affiche l'erreur
                print("{}".format(err))
            
        else: # Write output in a file
            if nomFichier.find(".") >= 0: # On vérifie si le fichier n'a pas déjà un suffixe
                path = os.getcwd() + "/" + nomFichier

            else: # S'il n'a pas de suffixe on rajoute .txt par défaut
                path = os.getcwd() + "/" + nomFichier + ".txt"

            file = open(path, 'w')
            msg = ""

            if process.returncode == 0: # Si tout à bien fonctionné on affiche l'output
                msg = "{}".format(out)
            else:                       # Sinon on affiche l'erreur
                msg = "{}".format(err)

            file.write(msg)
            file.close()

#### Section Erreurs ####

    ## Mettre le message global d'erreur ici qu'on appelera si nécessaire ##
def printError():
    err = "An error has occurred"
    print(err, file=sys.stderr)


#### Section principale (Loop) ####

if __name__ == '__main__':
    loop = True
    while loop == True:
    ## Prompt la commande du gars ##
        try:
            display = [True, 0]
            command = input("\nmysh$ ")
    ## Parse et lire la commande ##
            commandList = shlex.split(command)
        # Vérifier s'il y a une redirection à faire ou si on affiche le résultat directement #
            count = 0
            for cmd in commandList:
                count = count + 1
                if cmd == "cat": # On enlève "cat" car c'est un cas spécial pour l'utilisation de ">"
                     count = count   
                else:
                    if cmd == ">":
                        display[0] = False
                        display[1] = count # On met l'index du commandList pour retrouver le nom du fichier dans lequel save

        # Vérifier si c'est une built-in commande et si oui aller dans la section des built-in commandes #
            if commandList[0] == 'cd' or commandList[0] == 'pwd' or commandList[0] == 'exit':
                builtInCommand(commandList, display)

        # Sinon aller dans la section Lien aux Programmes #
            else: 
                otherCommands(commandList, display)
        
        except Exception as e:
            loop = True