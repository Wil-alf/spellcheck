import string

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

# Example Usage
dictionary = load_dictionary("words.txt")
input_sentence = "This is a sentnce with som misspelled words."
sentence_suggestions = spell_check_sentence(input_sentence, dictionary)

print("Sentence Suggestions:")
for word, suggestions in sentence_suggestions:
    print(f"Word: {word}")
    print("Suggestions:")
    for suggested_word, distance in suggestions:
        print(f"{suggested_word} (Distance: {distance})")
    print()