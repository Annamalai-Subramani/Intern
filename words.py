import os

# Function to load words from text files in a folder
def load_word_list_from_folder(folder_path, encoding='utf-8'):
    word_list = []
    for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), 'r', encoding=encoding) as file:
            word_list += file.read().splitlines()
    return word_list


positive_words = load_word_list_from_folder("D:/Projects/Intern/Intern/positive/", encoding='latin-1')
negative_words = load_word_list_from_folder("D:/Projects/Intern/Intern/negative/", encoding='latin-1')
stopword = load_word_list_from_folder("D:/Projects/Intern/Intern/stopwords/", encoding='latin-1')


print("Positive words:", len(positive_words))
print("Negative words:", len(negative_words))
print("Stopwords:", len(stopword))