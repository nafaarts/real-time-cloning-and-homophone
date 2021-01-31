import re
from phonetisch import soundex, caverphone


class syllable:

    def __init__(self, consonant=None, vocal=None, double_consonant=None):
        self.consonant = ['b', 'c', 'd', 'f', 'g', 'h', 'j',
                          'k', 'l', 'm', 'n', 'p', 'q', 'r',
                          's', 't', 'v', 'w', 'x', 'y', 'z',
                          'ng', 'ny', 'sy', 'ch', 'dh', 'gh',
                          'kh', 'ph', 'sh', 'th']+(consonant or [])

        self.double_consonant = ['ll', 'ks',
                                 'rs', 'rt']+(double_consonant or [])

        self.vocal = ['a', 'e', 'i', 'o', 'u']+(vocal or [])

    def split_letters(self, string):
        letters = []
        arrange = []

        while string != '':
            letter = string[:2]

            if letter.lower() in self.double_consonant:

                if string[2:] != '' and string[2].lower() in self.vocal:
                    letters += [letter[0]]
                    arrange += ['c']
                    string = string[1:]

                else:
                    letters += [letter]
                    arrange += ['c']
                    string = string[2:]

            elif letter.lower() in self.consonant:
                letters += [letter]
                arrange += ['c']
                string = string[2:]

            elif letter.lower() in self.vocal:
                letters += [letter]
                arrange += ['v']
                string = string[2:]

            else:
                letter = string[0]

                if letter.lower() in self.consonant:
                    letters += [letter]
                    arrange += ['c']
                    string = string[1:]

                elif letter.lower() in self.vocal:
                    letters += [letter]
                    arrange += ['v']
                    string = string[1:]

                else:
                    letters += [letter]
                    arrange += ['s']
                    string = string[1:]

        return letters, ''.join(arrange)

    def split_syllables_from_letters(self, letters, arrange):
        consonant_index = re.search('vc{2,}', arrange)
        while consonant_index:
            i = consonant_index.start()+1
            letters = letters[:i+1]+['|']+letters[i+1:]
            arrange = arrange[:i+1]+'|'+arrange[i+1:]
            consonant_index = re.search('vc{2,}', arrange)

        vocal_index = re.search(r'v{2,}', arrange)
        while vocal_index:
            i = vocal_index.start()
            letters = letters[:i+1]+['|']+letters[i+1:]
            arrange = arrange[:i+1]+'|'+arrange[i+1:]
            vocal_index = re.search(r'v{2,}', arrange)

        vcv_index = re.search(r'vcv', arrange)
        while vcv_index:
            i = vcv_index.start()
            letters = letters[:i+1]+['|']+letters[i+1:]
            arrange = arrange[:i+1]+'|'+arrange[i+1:]
            vcv_index = re.search(r'vcv', arrange)

        sep_index = re.search(r'[cvs]s', arrange)
        while sep_index:
            i = sep_index.start()
            letters = letters[:i+1]+['|']+letters[i+1:]
            arrange = arrange[:i+1]+'|'+arrange[i+1:]
            sep_index = re.search(r'[cvs]s', arrange)

        sep_index = re.search(r's[cvs]', arrange)
        while sep_index:
            i = sep_index.start()
            letters = letters[:i+1]+['|']+letters[i+1:]
            arrange = arrange[:i+1]+'|'+arrange[i+1:]
            sep_index = re.search(r's[cvs]', arrange)

        return ''.join(letters).split('|')

    def split_syllables(self, string):
        letters, arrange = self.split_letters(string)
        return self.split_syllables_from_letters(letters, arrange)

    def soundex(self, string):
        syllable = self.split_syllables(string)

        with open("word/word_bank.txt", "r") as f:
            data = f.readlines()

        symbols = [",", " ", ".", "!", "?"]

        sentence = []
        sentence2 = ""

        for kata in syllable:
            x = soundex.encode_word(kata)
            for line in data:
                y = soundex.encode_word(line.strip())
                if x == y:
                    sentence += line
                    sentence2 += line
                    break
                elif kata in symbols:
                    sentence += kata
                    sentence2 += kata
                    break

        result = ""
        for kata in sentence2:
            if kata == '\n':
                result += " "
            else:
                result += kata

        return result


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Split string into syllables token.")
    parser.add_argument("string", help="string to be splitted.")

    args = parser.parse_args()

    ss = syllable()

    syllables = ss.soundex(args.string)

    print(syllables)
