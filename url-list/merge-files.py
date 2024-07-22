def read_words_to_dict(file_path, word_dict):
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            word_dict[word] = word_dict.get(word, 0) + 1

def write_dict_to_file(word_dict, output_file_path):
    with open(output_file_path, 'w') as file:
        for word in sorted(word_dict):
            file.write(word + '\n')

def main():
    file1 = 'nsfw-subs.txt'  # replace with your first file path
    file2 = 'new-nsfw-subs.txt'  # replace with your second file path
    output_file = file1 # 'combined-nsfw-list.txt'  # replace with your desired output file path

    word_dict = {}

    read_words_to_dict(file1, word_dict)
    read_words_to_dict(file2, word_dict)

    write_dict_to_file(word_dict, output_file)

if __name__ == "__main__":
    main()
