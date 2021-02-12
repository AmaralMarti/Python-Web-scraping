from webscraping import process_url
from report import generate_report
import json

if __name__ == '__main__':
    #tree = process_url('freeCodeCamp/freeCodeCamp')
    #tree = process_url('vivadecora/desafio-backend-trabalhe-conosco')
    #tree = process_url('ohmyzsh/ohmyzsh')
    tree = process_url('Edlaine-Pontes/Forkids')
    # print(json.dumps(tree, indent = 2))
    generate_report('Edlaine-Pontes/Forkids', tree)