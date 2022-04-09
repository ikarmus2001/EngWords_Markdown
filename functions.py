import requests
import json
from mysecrets import oxford_secrets, merriam_collegiate, merriam_intermediate
from datetime import datetime
import csv

json_dir = '/json_files'


def csv_read_sort(file_dir) -> list:
    # importing words from csv file
    with open(file_dir, 'r') as r:
        for w in csv.reader(r):
            words.append(w)

    result = []
    for word in words:
        if word.lower() not in result:
            result.append(word)
    return result


def freedictionary(word: str, save_jsons=True) -> dict:
    """
    Creates, sends and handles API calls to https://dictionaryapi.dev/
    :param word: english word provided to API, assuming it is right
    :param save_jsons: default True, otherwise doese not save requests
    :return: dict{"word": word: str, "shortDefinition{X}": shortdef: str}
         where X = each def.
    """
    dict_name = 'freedict'
    base = "https://api.dictionaryapi.dev/api/v2/entries/en"
    url = f"{base}/{word}"
    # oxford_header = {"app_id": {app_id}, "app_key": {app_key}}
    r = requests.get(url)  # , headers=oxford_header)

    if save_jsons:
        with open(f"{json_dir}/freedict_{word}_{str(datetime.now())}", 'a') as a:
            json.dump(r, a)
            a.write("\n")

    j = json.load(r.json())
    result = {'word': word}  # init result with searched word
    # TODO what if word is not defined in dict?
    if not j.get('title') == "No Definitions Found":
        for index, (_, sense) in enumerate(j['meanings'][0]):
            # part_of_speech = sense['partOfSpeech']
            tmp = sense['definitions'][0]['definition']
            result[f'{dict_name}_shortDefinitions{index}'] = tmp
            # result[f'{dict_name}_partOfSpeech{index}'] = part_of_speech
    return result


def oxford(word: str, save_jsons=True) -> dict:
    """
    Creates, sends and handles API calls to Oxford Dictionaries
    More info: https://developer.oxforddictionaries.com/documentation
    :param word: english word provided to API, assuming it is right
    :param save_jsons: default True, otherwise doese not save requests
    :return: dict{"word": word: str, "shortDefinition{X}": shortdef: str}
         where X = each def.
    """
    dict_name = 'oxford'
    base = "https://od-api.oxforddictionaries.com/api/v2/entries/"
    language = "en-gb"
    app_id, app_key = oxford_secrets()
    url = f"{base}/{language}/{word}"
    oxford_header = {"app_id": {app_id}, "app_key": {app_key}}
    r = requests.get(url, headers=oxford_header)

    if save_jsons:
        with open(f"{json_dir}/oxford_{word}_{str(datetime.now())}", 'a') as a:
            json.dump(r, a)
            a.write("\n")

    j = json.load(r.json())
    result = {'word': word}  # init result with searched word
    # TODO what if word is not defined in dict?
    for index, (_, sense) in enumerate(j['results'][0]['lexicalEntries'][0]['entries'][0]['senses']):
        tmp = sense['shortDefinitions']
        result[f'{dict_name}_shortDefinitions{index}'] = tmp
    return result


def merriam_webster_collegiate(word: str, save_jsons=True) -> dict:
    """
        Creates, sends and handles API calls to Merriam-Webster Dictionaries
        More info: https://dictionaryapi.com/products/json
        :param word: english word provided to API, assuming it is right
        :param save_jsons: default True, otherwise doese not save requests
        :return: dict{"word": word: str, "shortDefinition{X}": shortdef: str}
         where X = each def.
        """
    dict_name = 'merriam collegiate'
    base = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
    api_key = merriam_collegiate
    url = f"{base}/{word}?key={api_key}"
    r = requests.get(url)

    if save_jsons:
        with open(f"{json_dir}/mw_c_{word}_{str(datetime.now())}.json", 'a') as a:
            json.dump(r, a)
            a.write("\n")

    j = json.load(r.json())
    result = {'word': word}  # init result with searched word
    # TODO what if word is not defined in dict?
    for meaning in j.len():
        for index, (_, sense) in enumerate(j[0]['shortdef']):
            tmp = sense['sense']
            result[f'{dict_name}_shortDefinitions{index}'] = tmp
    return result


def merriam_webster_intermediate(word: str, save_jsons=True) -> dict:
    """
        Creates, sends and handles API calls to Merriam-Webster Dictionaries
        More info: https://dictionaryapi.com/products/json
        :param word: english word provided to API, assuming it is right
        :param save_jsons: default True, otherwise doese not save requests
        :return: dict{"word": word: str, "shortDefinition{X}": shortdef: str}
         where X = each def.
        """
    dict_name = 'merriam intermediate'
    base = "https://www.dictionaryapi.com/api/v3/references/sd3/json/"
    api_key = merriam_intermediate
    url = f"{base}/{word}?key={api_key}"
    r = requests.get(url)

    if save_jsons:
        with open(f"{json_dir}/mw_i_{word}_{str(datetime.now())}", 'a') as a:
            json.dump(r, a)
            a.write("\n")

    j = json.load(r.json())
    result = {'word': word}  # init result with searched word
    # TODO what if word is not defined in dict?
    for meaning in j.len():
        for index, (_, sense) in enumerate(j[0]['shortdef']):
            tmp = sense['sense']
            result[f'{dict_name}_shortDefinitions{index}'] = tmp
    return result

# TODO pasowałoby osobną funkcję do requestów zrobić

# TODO jak kiedys bede przy tym siedzial, to trzeba uprosicic zwracane typy,
#       nie ma potrzeby wszędzie jsona trzymać

def ask_which_meaning(meanings: dict) -> tuple:
    # can't' afford API, you need to click the link :(
    word = meanings['word']

    print(f'Choose definition for {word}:')
    definitions = []
    id = 0
    for key, value in meanings:
        if key == 'word':
            continue
        definitions.append(value)
        print(f'{id} from {key.split("_")[0]}:  {value}')
    choice = input("Choose coresponding id  OR  -1 to write own definition")
    if choice == -1 or "":
        result = input("Input your definition: ")
    else:
        result = definitions[choice]

    pl_eng_link = f'https://www.deepl.com/translator#en/pl/{word}'
    print(f'{word} --PL--> {pl_eng_link}')
    translation = input("Input translation: ")

    return (result, translation)

def markdowning(words_def: list, start_id=1) -> str:
    output = ''
    for line in words_def:
        output += f'{start_id} | {line[0]} | {line[1]} | {line[2]} |\n'
    return output
