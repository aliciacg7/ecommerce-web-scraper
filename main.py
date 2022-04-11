import os
import sys

# Comprobar numero de argumentos
if __name__ == "__main__":
    if(len(sys.argv) == 3):
        
        searchfile = sys.argv[1]
        searchpages = int(sys.argv[2])

        if (searchpages <= 0):
            print("Numero de paginas a buscar incorrecto")
        
        else:
            with open(searchfile, encoding="utf-8") as f:
                for line in f.readlines():
                    print('python src/sailor.py "{}" {}'.format(line.strip(), searchpages))
                    os.system('python src/sailor.py "{}" {}'.format(line.strip(), searchpages))

    else:
        print("Numero de argumentos incorrecto. Uso del script:")
        print(f'\t> python main.py \"FICHERO_CON_BUSQUEDAS\" \"NUM_PAGINAS\"')
        
