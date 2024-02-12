import os
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from words import positive_words,negative_words,stopword
import pandas as pd

nltk.download('punkt')
# Load stop words
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

positive = [word for word in positive_words if word not in stopword]
negative = [word for word in negative_words if word not in stopword]

# Function to calculate positive score
def calculate_positive_score(text):
    return sum(1 for word in word_tokenize(text) if word.lower() in positive)

# Function to calculate negative score
def calculate_negative_score(text):
    return sum(1 for word in word_tokenize(text) if word.lower() in negative)

# Function to calculate polarity score
def calculate_polarity_score(positive_score, negative_score):
    return (positive_score - negative_score) / (positive_score + negative_score + 0.000001)

# Function to calculate subjectivity score
def calculate_subjectivity_score(positive_score, negative_score, total_words):
    return (positive_score + negative_score) / (total_words + 0.000001)

# Function to calculate average sentence length
def calculate_avg_sentence_length(text):
    sentences = sent_tokenize(text)
    total_words = sum(len(word_tokenize(sentence)) for sentence in sentences)
    total_sentences = len(sentences)
    return total_words / (total_sentences + 0.000001)

# Function to calculate percentage of complex words
def calculate_percentage_complex_words(text):
    words = word_tokenize(text)
    complex_words = sum(1 for word in words if syllable_count(word) > 2)
    return (complex_words / (len(words) + 0.000001)) * 100

# Function to calculate fog index
def calculate_fog_index(avg_sentence_length, percentage_complex_words):
    return 0.4 * (avg_sentence_length + percentage_complex_words)

# Function to calculate average number of words per sentence
def calculate_avg_words_per_sentence(text):
    words = word_tokenize(text)
    total_words = len(words)
    total_sentences = len(sent_tokenize(text))
    return total_words / (total_sentences + 0.000001)

# Function to calculate complex word count
def calculate_complex_word_count(text):
    words = word_tokenize(text)
    return sum(1 for word in words if syllable_count(word) > 2)

# Function to calculate syllable count per word
def syllable_count(word):
    vowels = 'aeiouy'
    word = word.lower()
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if count == 0:
        count += 1
    return count

# Function to calculate personal pronouns count
def calculate_personal_pronouns(text):
    pronouns = ['I', 'we', 'my', 'ours', 'us']
    return sum(1 for word in word_tokenize(text) if word.lower() in pronouns)

# Function to calculate average word length
def calculate_avg_word_length(text):
    words = word_tokenize(text)
    total_characters = sum(len(word) for word in words)
    total_words = len(words)
    return total_characters / (total_words + 0.000001)

def calculate_syllable_per_word(text):
    words = word_tokenize(text)
    syllable_counts = [syllable_count(word) for word in words]
    total_syllables = sum(syllable_counts)
    total_words = len(words)
    if total_words == 0:
        return 0  # Avoid division by zero
    syllable_per_word = total_syllables / total_words
    return syllable_per_word

# Function to remove punctuation from text
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

# Function to count words after removing stop words and punctuation
def count_cleaned_words(text):
    words = word_tokenize(text)
    cleaned_words = [word for word in words if word.lower() not in stop_words]
    cleaned_words = [remove_punctuation(word) for word in cleaned_words]
    cleaned_words = list(filter(None, cleaned_words))
    return len(cleaned_words)

# Directory where article files are stored
article_folder = "articles/"

# Dictionary to store results
results = {}

# Calculate variables for each file in the article folder
for filename in os.listdir(article_folder):
    with open(os.path.join(article_folder, filename), 'r', encoding='utf-8') as file:
        text = file.read()
    cleaned_text = remove_punctuation(text)
    total_words = count_cleaned_words(cleaned_text)
    positive_score = calculate_positive_score(cleaned_text)
    negative_score = calculate_negative_score(cleaned_text)
    polarity_score = calculate_polarity_score(positive_score, negative_score)
    subjectivity_score = calculate_subjectivity_score(positive_score, negative_score, total_words)
    avg_sentence_length = calculate_avg_sentence_length(cleaned_text)
    percentage_complex_words = calculate_percentage_complex_words(cleaned_text)
    fog_index = calculate_fog_index(avg_sentence_length, percentage_complex_words)
    avg_words_per_sentence = calculate_avg_words_per_sentence(cleaned_text)
    syllable_per_word = calculate_syllable_per_word(text)
    complex_word_count = calculate_complex_word_count(cleaned_text)
    personal_pronouns_count = calculate_personal_pronouns(cleaned_text)
    avg_word_length = calculate_avg_word_length(cleaned_text)
    
    # Store results for each file in the dictionary
    results[filename] = {
        "POSITIVE SCORE": positive_score,
        "NEGATIVE SCORE": negative_score,
        "POLARITY SCORE": polarity_score,
        "SUBJECTIVITY SCORE": subjectivity_score,
        "AVG SENTENCE LENGTH": avg_sentence_length,
        "PERCENTAGE OF COMPLEX WORDS": percentage_complex_words,
        "FOG INDEX": fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE": avg_words_per_sentence,
        "COMPLEX WORD COUNT": complex_word_count,
        "WORD COUNT": total_words,
        "SYLLABLE PER WORD": syllable_per_word,  
        "PERSONAL PRONOUNS": personal_pronouns_count,
        "AVG WORD LENGTH": avg_word_length
    }

# Create a DataFrame from the dictionary
df = pd.DataFrame.from_dict(results, orient='index')

# Save the DataFrame to an Excel file
df.to_excel("output.xlsx")