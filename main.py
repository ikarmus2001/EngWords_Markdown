import functions


def main_local():  # TODO
    pass

def main_api(input_csv: str):
    translate_providers = [
        functions.oxford,
        functions.merriam_intermediate,
        functions.merriam_collegiate,
        functions.freedictionary]
    words = functions.csv_read_sort
    words_def = []
    for id, word in enumerate(words):
        meaning_check = {}
        for provider in translate_providers:
            provider_meaning = provider(word)
            meaning_check.update(provider_meaning)
        result, translation = ask_which_meaning(id, meaning_check)
        words_def.append([word, result, translation])

    result = markdowning(words_def)
    markdown_header = "\#|ENG|Meaning|PL|\n"
    with open('result_markdown.md', 'w') as w:
        w.write(markdown_header)
        w.write(result)
    exit(1)
