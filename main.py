import functions

translate_providers = [functions.merriam_intermediate,
                       functions.oxford,
                       functions.merriam_collegiate]
words = ["amazing"]
words_def = []
for id, word in enumerate(words):
    meaning_check = {}
    for provider in translate_providers:
        provider_meaning = provider(word)
        meaning_check.update(provider_meaning)
    result, translation = ask_which_meaning(id, meaning_check)
    words_def.append([word, result, translation])
result = markdowning(words_def)
with open('result_markdown.md', 'w') as w:
    w.write(result)
exit(1)
