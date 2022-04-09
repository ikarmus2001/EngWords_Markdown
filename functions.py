import requests
import json
from os import listdir
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


def freedictionary(word: str, save_jsons=True, api_call=False) -> dict:
    """
    Creates, sends and handles API calls to https://dictionaryapi.dev/
    :param word: english word provided to API, assuming it is right
    :param save_jsons: default True, otherwise doese not save requests
    :return: dict{"word": word: str, "shortDefinition{X}": shortdef: str}
         where X = each def.
    """

    if api_call:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        r = api_request(url)
        j = json.load(r.json())
    else:
        j = open_local_json(f"{json_dir}/freedict_{word}_")

    if save_jsons:
        now = datetime.datetime.now()
        date = f'{str(now.date())}_{str(now.hour)}:{str(now.minute)}'
        with open(f"{json_dir}/freedict_{word}_{date}", 'a') as a:
            json.dump(r, a)
            a.write("\n")


    result = {'word': word}  # init result with searched word

    # TODO what if word is not defined in dict?
    dict_name = 'freedict'
    if not j.get('title') == "No Definitions Found":
        for index, (_, sense) in enumerate(j['meanings'][0]):
            # part_of_speech = sense['partOfSpeech']
            tmp = sense['definitions'][0]['definition']
            result[f'{dict_name}_shortDefinitions{index}'] = tmp
            # result[f'{dict_name}_partOfSpeech{index}'] = part_of_speech
    return result


def oxford(word: str, save_jsons=True, api_call=False) -> dict:
    """
    Creates, sends and handles API calls to Oxford Dictionaries
    More info: https://developer.oxforddictionaries.com/documentation
    :param word: english word provided to API, assuming it is right
    :param save_jsons: default True, otherwise doese not save requests
    :return: dict{"word": word: str, "shortDefinition{X}": shortdef: str}
         where X = each def.
    """
    dict_name = 'oxford'
    if api_call:
        base = "https://od-api.oxforddictionaries.com/api/v2/entries/"
        language = "en-gb"
        app_id, app_key = oxford_secrets()
        url = f"{base}/{language}/{word}"
        oxford_header = {"app_id": {app_id}, "app_key": {app_key}}
        r = api_request(url, header=oxford_header)
    else:
        pass  # TODO

    if save_jsons:
        now = datetime.datetime.now()
        date = f'{str(now.date())}_{str(now.hour)}:{str(now.minute)}'
        with open(f"{json_dir}/oxford_{word}_{date}", 'a') as a:
            json.dump(r, a)
            a.write("\n")

    j = json.load(r.json())
    result = {'word': word}  # init result with searched word
    # TODO what if word is not defined in dict?
    for index, (_, sense) in enumerate(j['results'][0]['lexicalEntries'][0]['entries'][0]['senses']):
        tmp = sense['shortDefinitions']
        result[f'{dict_name}_shortDefinitions{index}'] = tmp
    return result


def merriam_webster_collegiate(word: str, save_jsons=True, api_call=False) -> dict:
    """
        Creates, sends and handles API calls to Merriam-Webster Dictionaries
        More info: https://dictionaryapi.com/products/json
        :param word: english word provided to API, assuming it is right
        :param save_jsons: default True, otherwise doese not save requests
        :return: dict{"word": word: str, "shortDefinition{X}": shortdef: str}
         where X = each def.
        """
    if api_call:
        base = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
        url = f"{base}/{word}?key={merriam_collegiate}"
        r = api_request(url)
    else:
        open_local_json()

    if save_jsons:
        now = datetime.datetime.now()
        date = f'{str(now.date())}_{str(now.hour)}:{str(now.minute)}'
        with open(f"{json_dir}/mw_c_{word}_{date}.json", 'a') as a:
            json.dump(r, a)
            a.write("\n")

    j = json.load(r.json())
    dict_name = 'merriam collegiate'
    result = {'word': word}  # init result with searched word
    # TODO what if word is not defined in dict?
    for meaning in j.len():
        for index, (_, sense) in enumerate(j[0]['shortdef']):
            tmp = sense['sense']
            result[f'{dict_name}_shortDefinitions{index}'] = tmp
    return result


def merriam_webster_intermediate(word: str, save_jsons=True, api_call=False) -> dict:
    """
        Creates, sends and handles API calls to Merriam-Webster Dictionaries
        More info: https://dictionaryapi.com/products/json
        :param word: english word provided to API, assuming it is right
        :param save_jsons: default True, otherwise doese not save requests
        :return: dict{"word": word: str, "shortDefinition{X}": shortdef: str}
         where X = each def.
        """
    if api_call:
        dict_name = 'merriam intermediate'
        base = "https://www.dictionaryapi.com/api/v3/references/sd3/json/"
        url = f"{base}/{word}?key={merriam_intermediate}"
        r = api_request(url)
    else:
        open_local_json()

    if save_jsons:
        now = datetime.datetime.now()
        date = f'{str(now.date())}_{str(now.hour)}:{str(now.minute)}'
        with open(f"{json_dir}/mw_i_{word}_{date}", 'a') as a:
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


def api_request(url: str, header=False) -> requests.Response:
    if not header:
        return requests.get(url)
    return requests.get(url, header)

def open_local_json(start_of_filename: str) -> json_object XDDDD:  # TODO asap
    matching_files = [f for f in os.listdir() if f.startswith(start_of_filename)]
    if matching_files.len() > 1
        for id, file in enumerate(matching_files):
            tmp_f = file[-16:-1]
            tmp_f[10] = " "
            formatted_date = datetime.strptime(tmp_f)
        with open()
    return matching_files[0]

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
