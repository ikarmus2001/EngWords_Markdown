import json


def test_oxford_json():
    file = "D:\\Nie-gry\\Programowanie\\PycharmProjects\\EngWords_Markdown\\json_dump_surely_original.json"
    with open(file, 'r') as r:
        j = json.load(r)
    result = {}
    for sense in j['results'][0]['lexicalEntries'][0]['entries'][0]['senses']:
        result['shortDefinitions'] = sense['shortDefinitions']
    print(result)


def test_merriam_collegiate():
    pass  # TODO test + json via https://dictionaryapi.com/products/api-collegiate-dictionary


def test_freedict():  # TODO
    pass
# results = json_dict['results']
# lexicalEntries = results['lexicalEntries']
# print(lexicalEntries)
