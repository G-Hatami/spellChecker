import re
import time


# Read dictionary
def readFile(filename):
    word_list = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            line = line.strip()  # This will remove '\n' and any other surrounding whitespace
            word_list.append(line)
    return word_list


# DP algorithm

def levenshtein_distance(s1, s2):
    # Create a matrix to store the distances
    dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

    # Initialize the matrix
    for i in range(len(s1) + 1):
        dp[i][0] = i
    for j in range(len(s2) + 1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(dp[i - 1][j] + 1,  # Deletion
                           dp[i][j - 1] + 1,  # Insertion
                           dp[i - 1][j - 1] + cost)  # Substitution

    return dp[len(s1)][len(s2)]


def spell_check(word1, dictionary1):
    if word1 in dictionary1:
        return [word1]  # The word is correctly spelled
    else:
        # Find the closest words in the dictionary
        min_distance = float('inf')
        closest_words = []
        for dict_word in dictionary1:
            distance = levenshtein_distance(word1, dict_word)
            if distance < min_distance:
                min_distance = distance
                closest_words = [dict_word]
            elif distance == min_distance:
                closest_words.append(dict_word)
        return closest_words


# Read the dictionary file
dictionary_file_path = "F:\\PRGRMMING\\python-projects\\spell-checking\\spell-checking\\testDictionary.txt"
given_words = readFile(dictionary_file_path)
dictionary = set(given_words)  # Convert list to set for quick lookup


# Function to clean the input text
def remove_punctuation(text):
    # Remove punctuation using regex
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    # Convert text to lowercase
    cleaned_text = cleaned_text.lower()
    return cleaned_text


# Get user input
user_input = input("Provide your words:\n")
start_time = time.time()
# Clean the input via removing all the punctuation
cleaned_input = remove_punctuation(user_input)

# Convert the input to a data structure to work on words independently
words = cleaned_input.split()

# Check the spelling of each word
# In this part , we use the corrected_words as a key-value pair which represents every word in input as key and
# The list of all the words with similar and closest distance as values
corrected_words = {}  # Dictionary in Python is a collection of key-value pairs
for word in words:
    corrected_words[word] = spell_check(word, dictionary)

# Print the results
# The word , is the original input(key) and the corrections show the lists of all values
for word, corrections in corrected_words.items():
    if len(corrections) == 1 and word == corrections[0]:
        print(f'Word: {word}, State: Founded')
    else:
        print(f"Word: {word}, State: Not found, Suggestions: {corrections}")

end_time = time.time()

print(f"Time duration would be {end_time - start_time}")
