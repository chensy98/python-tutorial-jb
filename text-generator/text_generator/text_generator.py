import random

from nltk import WhitespaceTokenizer


def token_statistics(filename):
    wpt = WhitespaceTokenizer()
    token_list = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            for word in wpt.tokenize(line):
                token_list.append(word)
    return token_list


def trigram_analysis(token_list):
    trigram_list = []
    for i in range(len(token_list) - 2):
        trigram_list.append((token_list[i], token_list[i + 1], token_list[i + 2]))
    return trigram_list


def markov_chain_generator(trigram_list):
    markov_dict = {}
    for trigram in trigram_list:
        tuple_ = (trigram[0], trigram[1])
        markov_dict.setdefault(tuple_, [])
        markov_dict[tuple_].append(trigram[2])
    return markov_dict


def sentence_generator(head, markov_dict):
    text = ' '.join(head)
    count = 2
    while True:
        nxt = random.choice(markov_dict[head])
        text += ' ' + nxt
        head = (head[1], nxt)
        count += 1
        if count >= 5 and head[1].endswith(('.', '!', '?')):
            break
    print(text)


def main():
    corpus_file = input()
    token_list = token_statistics(corpus_file)
    trigram_list = trigram_analysis(token_list)
    trigram_markov_dict = markov_chain_generator(trigram_list)
    for i in range(10):
        head = random.choice(trigram_list)[:2]
        while not head[0][0].isupper() or head[0].endswith(('.', '!', '?')) or head[1].endswith(('.', '!', '?')):
            head = random.choice(trigram_list)[:2]
        sentence_generator(head, trigram_markov_dict)


if __name__ == '__main__':
    main()
