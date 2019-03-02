import nltk
from textblob import Word
from textblob import TextBlob
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO


def parse(string):
    """
    Parse a paragraph. Devide it into sentences and try to generate quesstions from each sentences.
    """

    try:
        txt = TextBlob(string)
        # Each sentence is taken from the string input and passed to genQuestion() to generate questions.
        for sentence in txt.sentences:
            genQuestion(sentence)

    except Exception as e:
        raise e


def genQuestion(line):
    """
    outputs question from the given text
    """

    if type(line) is str:  # If the passed variable is of type string.
        line = TextBlob(line)  # Create object of type textblob.blob.TextBlob

    bucket = {}  # Create an empty dictionary

    for i, j in enumerate(
            line.tags):  # line.tags are the parts-of-speach in English
        if j[1] not in bucket:
            bucket[
                j[1]] = i  # Add all tags to the dictionary or bucket variable

    if verbose:  # In verbose more print the key,values of dictionary
        print('\n', '-' * 20)
        print(line, '\n')
        print("TAGS:", line.tags, '\n')
        print(bucket)

    question = ''  # Create an empty string

    # These are the english part-of-speach tags used in this demo program.
    # .....................................................................
    # NNS     Noun, plural
    # JJ  Adjective
    # NNP     Proper noun, singular
    # VBG     Verb, gerund or present participle
    # VBN     Verb, past participle
    # VBZ     Verb, 3rd person singular present
    # VBD     Verb, past tense
    # IN      Preposition or subordinating conjunction
    # PRP     Personal pronoun
    # NN  Noun, singular or mass
    # .....................................................................

    # Create a list of tag-combination

    l1 = ['NNP', 'VBG', 'VBZ', 'IN']
    l2 = ['NNP', 'VBG', 'VBZ']

    l3 = ['PRP', 'VBG', 'VBZ', 'IN']
    l4 = ['PRP', 'VBG', 'VBZ']
    l5 = ['PRP', 'VBG', 'VBD']
    l6 = ['NNP', 'VBG', 'VBD']
    l7 = ['NN', 'VBG', 'VBZ']

    l8 = ['NNP', 'VBZ', 'JJ']
    l9 = ['NNP', 'VBZ', 'NN']

    l10 = ['NNP', 'VBZ']
    l11 = ['PRP', 'VBZ']
    l12 = ['NNP', 'NN', 'IN']
    l13 = ['NN', 'VBZ']

    # With the use of conditional statements the dictionary is compared with the list created above

    if all(key in bucket for key in
           l1):  # 'NNP', 'VBG', 'VBZ', 'IN' in sentence.
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[
            bucket['NNP']] + ' ' + line.words[bucket['VBG']] + '?'
        answer = bucket['IN']

    elif all(key in bucket for key in l2):  # 'NNP', 'VBG', 'VBZ' in sentence.
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[
            bucket['NNP']] + ' ' + line.words[bucket['VBG']] + '?'
        answer = line.words[bucket['VBZ']]

    elif all(key in bucket for key in
             l3):  # 'PRP', 'VBG', 'VBZ', 'IN' in sentence.
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[
            bucket['PRP']] + ' ' + line.words[bucket['VBG']] + '?'
        answer = line.words[bucket['VBZ']]

    elif all(key in bucket for key in l4):  # 'PRP', 'VBG', 'VBZ' in sentence.
        question = 'What ' + line.words[bucket['PRP']] + ' ' + ' does ' + \
                   line.words[bucket['VBG']] + ' ' + line.words[
                       bucket['VBG']] + '?'
        answer = line.words[bucket['VBZ']]

    elif all(key in bucket for key in l7):  # 'NN', 'VBG', 'VBZ' in sentence.
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[
            bucket['NN']] + ' ' + line.words[bucket['VBG']] + '?'

    elif all(key in bucket for key in l8):  # 'NNP', 'VBZ', 'JJ' in sentence.
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[
            bucket['NNP']] + '?'
        answer = line.words[bucket['JJ']]

    elif all(key in bucket for key in l9):  # 'NNP', 'VBZ', 'NN' in sentence
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[
            bucket['NNP']] + '?'
        answer = line.words[bucket['NN']]

    elif all(key in bucket for key in l11):  # 'PRP', 'VBZ' in sentence.
        if line.words[bucket['PRP']] in ['she', 'he']:
            question = 'What' + ' does ' + line.words[
                bucket['PRP']].lower() + ' ' + line.words[
                           bucket['VBZ']].singularize() + '?'
            answer = line.words[bucket['VBZ']]

    elif all(key in bucket for key in l10):  # 'NNP', 'VBZ' in sentence.
        question = 'What' + ' does ' + line.words[bucket['NNP']] + ' ' + \
                   line.words[bucket['VBZ']].singularize() + '?'

    elif all(key in bucket for key in l13):  # 'NN', 'VBZ' in sentence.
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[
            bucket['NN']] + '?'

    # When the tags are generated 's is split to ' and s. To overcome this issue.
    if 'VBZ' in bucket and line.words[bucket['VBZ']] == "’":
        question = question.replace(" ’ ", "'s ")

    # Print the genetated questions as output.
    if question != '':
        print('\n', 'Question: ' + question)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()

def main():
    """
    Accepts a text file as an argument and generates questions from it.
    """
    # verbose mode is activated when we give -v as argument.
    global verbose
    verbose = True

    # Set verbose if -v option is given as argument.
    if len(sys.argv) >= 3:
        if sys.argv[2] == '-v':
            print('Verbose Mode Activated\n')
            verbose = True

    # Open the file given as argument in read-only mode.
    with open("Makan's notes", encoding="utf8") as file:
        textinput = file.read()
    print('\n-----------INPUT TEXT-------------\n')
    print(textinput, '\n')
    print('\n-----------INPUT END---------------\n')

    # Send the content of text file as string to function parse()
    parse(textinput)


if __name__ == "__main__":
    main()