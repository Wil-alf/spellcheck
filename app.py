from flask import Flask, render_template, request
import string

app = Flask(__name__)

def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def wagner_fischer(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    if len_s1 > len_s2:
        s1, s2 = s2, s1
        len_s1, len_s2 = len_s2, len_s1

    current_row = range(len_s1 + 1)
    for i in range(1, len_s2 + 1):
        previous_row, current_row = current_row, [i] + [0] * len_s1
        for j in range(1, len_s1 + 1):
            add, delete, change = previous_row[j] + 1, current_row[j-1] + 1, previous_row[j-1]
            if s1[j-1] != s2[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[len_s1]

def spell_check(word, dictionary):
    suggestions = []

    for correct_word in dictionary:
        distance = wagner_fischer(word, correct_word)
        suggestions.append((correct_word, distance))

    suggestions.sort(key=lambda x: x[1])
    return suggestions[:3]

def spell_check_sentence(sentence, dictionary):
    sentence = sentence.lower()
    words = sentence.split()
    suggestions = []

    for word in words:
        word = word.translate(str.maketrans('', '', string.punctuation))
        word_suggestions = spell_check(word, dictionary)
        suggestions.append((word, word_suggestions))

    return suggestions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spellcheck', methods=['POST'])
def spellcheck():
    input_sentence = request.form['sentence']
    dictionary = load_dictionary("words.txt")
    sentence_suggestions = spell_check_sentence(input_sentence, dictionary)
    return render_template('result.html', sentence_suggestions=sentence_suggestions)

if __name__ == '__main__':
    app.run(debug=True)
