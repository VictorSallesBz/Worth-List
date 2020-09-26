from tweepy import Cursor, API, OAuthHandler
from re import sub
from nltk.tokenize import word_tokenize
from itertools import combinations, permutations
from os import system, name, listdir
from unidecode import unidecode


# Clear screen.
# Paths archives.
# If the OS is Windows
if name == 'nt':
    CLEAR = 'cls'
    # Leaked database
    PATH_LEAK_PASSWORDS = 'Files\Wordlist to Analyze.txt'
    # Leaked database data
    PATH_DATA = 'Files\Data.txt'
    # Most used password formats
    PATH_FORMATS = 'Files\Formats.txt'
    # Reference words for password creation
    PATH_WORDS = 'Files\Words.txt'
    # Generated Word list
    PATH_WORDLIST = 'Files\Wordlist.txt'
    # Collected Tweets
    PATH_TWEETS = 'Files\Tweets.txt'
    # Stopwords
    PATH_STOPWORDS = 'Files\Stopwords.txt'
    # Path that stores words that can be used as references
    # The words of the collected tweets will be compared to the words in that folder
    PATH_REFERENCES = 'Files\References\\'
# If the OS is Linux
else:
    CLEAR = 'clear'
    PATH_LEAK_PASSWORDS = 'Files/Wordlist to Analyze.txt'
    PATH_DATA = 'Files/Data.txt'
    PATH_FORMATS = 'Files/Formats.txt'
    PATH_TWEETS = 'Files/Tweets.txt'
    PATH_WORDS = 'Files/Words.txt'
    PATH_WORDLIST = 'Files/Wordlist.txt'
    PATH_LITTLE_STOPWORDS = 'Files/Little Stopwords.txt'
    PATH_STOPWORDS = 'Files/Stopwords.txt'
    PATH_REFERENCES = 'Files/References/'


# Analyzes word lists and generates a file
# With the most used password formats and
# Some other data such as size,
# Positions that contain letter numbers etc ...
def wordlist_analyzer(formats_quantity, min_password_length, max_password_length):
    # Variable for examining common password sizes
    size = [0] * max_password_length
    # Variable to know how common uppercase letters are in passwords
    uppercase = [0] * max_password_length
    # Variable to know how common lowercase letters are in passwords
    lowercase = [0] * max_password_length
    # Variable to know how common numbers are in passwords
    number = [0] * max_password_length
    # Variable to know how common special characters are in passwords
    symbol = [0] * max_password_length
    # Password formats
    password_formats = []
    # Position of a format in the list
    position_formats = []

    # Read file passwords
    # If have a word with unreadable characters, that word will be discarded.
    with open(PATH_LEAK_PASSWORDS, 'r', errors="ignore") as passwords_file:
        passwords = passwords_file.read().split()

    # Password analysis
    for password in passwords:
        # It serves to know if the format is new and needs to be added
        # Or if it is repeated and should not be added again
        add = True
        # Better to save the length in a variable than to call a function over and over to calculate
        # Since we are going to deal with many passwords
        # Any improvement to speed up the process is welcome
        length = len(password)
        if length < min_password_length or length >= max_password_length:
            continue
        size[length] += 1
        password_format = []
        # Checks the character type and writes the password format
        # Uppercase = X, Lowercase = y, Number = 9, Symbol = @
        for i in range(length):
            if password[i].isupper():
                password_format.append('X')
                uppercase[i] += 1
            elif password[i].islower():
                password_format.append('y')
                lowercase[i] += 1
            elif password[i].isdigit():
                password_format.append('9')
                number[i] += 1
            elif not password[i].isalnum():
                password_format.append('@')
                symbol[i] += 1

        current_format = ''.join(password_format)

        # Checks if the same format already exists
        # If it exists, +1 is added to the format
        # If it does not exist, it is added to the list of formats and 1 added to the format
        # It serves to discover the most common formats
        position = 0
        for written_format in password_formats:
            if current_format == written_format:
                position_formats[position] += 1
                add = False
            else:
                position += 1
        if add:
            password_formats.append(current_format)
            position_formats.append(1)
        else:
            add = True

    # ********--------********--------********--------********--------********
    # ********--------********      DATA WRITING      ********--------********
    # ********--------********--------********--------********--------********

    format_data_file = open(PATH_DATA, 'w', encoding='utf8')
    formats_file = open(PATH_FORMATS, 'w')

    format_data_file.write("FORMAT DATA\n")
    for i in range(formats_quantity):
        # Receive the highest index on the list
        # In our case it is the index of the most common format
        position = position_formats.index(max(position_formats))
        format_data_file.write('Passwords with {} format: {}\n'.format(password_formats[position], position_formats[position]))
        formats_file.write(password_formats[position] + '\n')
        password_formats.pop(position)
        position_formats.pop(position)
        if position_formats == []:
            break

    # Writing the Size data
    format_data_file.write("\nSIZE DATA\n")
    for i in range(max_password_length):
        if size[i] != 0:
            format_data_file.write('Passwords with size {}: {}\n'.format(i, size[i]))

    # Writing of uppercase data
    format_data_file.write("\nUPPERCASE DATA\n")
    for i in range(max_password_length):
        if uppercase[i] != 0:
            format_data_file.write('Passwords with uppercase in position {}: {}\n'.format(i+1, uppercase[i]))

    # Writing of lowercase data
    format_data_file.write("\nLOWERCASE DATA\n")
    for i in range(max_password_length):
        if lowercase[i] != 0:
            format_data_file.write('Passwords with lowercase in position {}: {}\n'.format(i+1, lowercase[i]))

    # Writing of number data
    format_data_file.write("\nNUMBER DATA\n")
    for i in range(max_password_length):
        if number[i] != 0:
            format_data_file.write('Passwords with number in position {}: {}\n'.format(i+1, number[i]))

    # Writing of symbol data
    format_data_file.write("\nSYMBOL DATA\n")
    for i in range(max_password_length):
        if symbol[i] != 0:
            format_data_file.write('Passwords with symbol in position {}: {}\n'.format(i+1, symbol[i]))

    format_data_file.close()
    formats_file.close()


# Generates the word list with the reference words
def generates_wordlist(formats_quantity, min_password_length, max_password_length):
    # Separates the words from the numbers in the reference list
    words, numbers = separate_strings_numbers()
    # Asks if the list will be with permutation or combination
    choice = 0
    while choice != 1 and choice != 2:
        try:
            choice = int(input("Do you want a heavy or light list?\n"
                               "Light lists are combinations: ABC -> AB, AC, BC\n"
                               "Heavy lists are permutations: ABC -> AB, AC, BA, BC, CA, CB\n\n"
                               "1 - Light list\n"
                               "2 - Heavy list\n"))
        except:
            input("Choice must be 1 or 2!\n\n"
                  "Press Enter to continue: ")

    if choice == 1:
        # Generates combined words and numbers
        combined_words = strings_combinations(words, max_password_length)
        combined_numbers = numbers_combinations(numbers, max_password_length)
    else:
        # Generates permutations words and numbers
        combined_words = strings_permutations(words, max_password_length)
        combined_numbers = numbers_permutations(numbers, max_password_length)

    # Generates a dictionary by organizing elements of equal sizes
    dictionary_words = separates_elements_by_size(combined_words)
    dictionary_numbers = separates_elements_by_size(combined_numbers)

    # Divides the formats to make it easier to generate passwords in the format
    splitted_formats = split_formats(formats_quantity, min_password_length, max_password_length)

    # Generates passwords with formats from the format list
    passwords = generates_passwords(splitted_formats, dictionary_words, dictionary_numbers)

    # Write passwords to the Wordlist file
    write_passwords(passwords)


# Separates strings from numbers
# Reads the file with the reference words and returns
# 2 lists. 1 with words and another with numbers.
def separate_strings_numbers():
    words = []
    numbers = []
    # Separate words and numbers into 2 lists
    with open(PATH_WORDS, 'r') as words_file:
        line = words_file.read().splitlines()
        for word in line:
            try:
                # Try convert to number
                int(word)
                # Takes the last 2 numbers of possible years. Ex .: 1995 -> 95
                # Until 2050 it's works XD
                if word > 1900 and word < 2050:
                    year = word[-2] + word[-1]
                    numbers.append(year)
                numbers.append(word)
            # If you can't convert, it is a word
            except:
                words.append(word)
    return words, numbers


# Generates combined words
def strings_combinations(words, max_password_length):
    combined_words = []

    for word in words:
        split_words = word.split()
        initial_letter = []
        initial_word = []
        size = len(split_words)
        # Word combinations
        for x in range(size):
            for comb in combinations(split_words, x + 1):
                tmp = ''.join(comb)
                if len(tmp) <= max_password_length:
                    combined_words.append(tmp)

            # Initial letter combinations
            aux = split_words[x]
            if size != 1:
                initial_word.append(aux)
                initial_letter.append(aux[0])
        for x in range(len(initial_letter) + 1):
            for comb in combinations(initial_letter, x):
                tmp = ''.join(comb)
                if len(tmp) <= max_password_length:
                    combined_words.append(tmp)

        # Combinations of words and initial letters
        index = []
        for x in range(len(initial_letter)):
            index.append(x)
        for x in range(len(index) + 1):
            for comb in combinations(index, x):
                if comb != ():
                    aux = []
                    for i in range(len(initial_word)):
                        if i in comb:
                            aux.append(initial_word[i])
                        else:
                            aux.append(initial_letter[i])
                        tmp = ''.join(aux)
                        if len(tmp) <= max_password_length:
                            combined_words.append(tmp)

    combined_words = set(combined_words)
    # Combinations generates an empty element
    try:
        combined_words.remove('')
    except:
        pass
    return combined_words


# Generates permutations words
def strings_permutations(words, max_password_length):
    permutation_words = []

    for word in words:
        split_words = word.split()
        initial_letter = []
        initial_word = []
        size = len(split_words)

        # Word permutations
        for x in range(size):
            for comb in permutations(split_words, x + 1):
                tmp = ''.join(comb)
                if len(tmp) <= max_password_length:
                    permutation_words.append(tmp)

            # Initial letter permutations
            aux = split_words[x]
            if size != 1:
                initial_word.append(aux)
                initial_letter.append(aux[0])
        for x in range(len(initial_letter) + 1):
            for comb in permutations(initial_letter, x):
                tmp = ''.join(comb)
                if len(tmp) <= max_password_length:
                    permutation_words.append(tmp)

        # Combinations of words and initial letters
        index = []
        for x in range(len(initial_letter)):
            index.append(x)
        for x in range(len(index) + 1):
            for comb in permutations(index, x):
                if comb != ():
                    aux = []
                    for i in range(len(initial_word)):
                        if i in comb:
                            aux.append(initial_word[i])
                        else:
                            aux.append(initial_letter[i])
                        tmp = ''.join(aux)
                        if len(tmp) <= max_password_length:
                            permutation_words.append(tmp)

    permutation_words = set(permutation_words)
    # Combinations generates an empty element
    try:
        permutation_words.remove('')
    except:
        pass
    return permutation_words


# Generates combined numbers
def numbers_combinations(numbers, max_password_length):
    combined_numbers = []
    for x in range(len(numbers) + 1):
        for comb in combinations(numbers, x):
            tmp = ''.join(comb)
            if len(tmp) <= max_password_length:
                combined_numbers.append(tmp)

    combined_numbers = set(combined_numbers)
    # Combinations generates an empty element
    try:
        combined_numbers.remove('')
    except:
        pass
    return combined_numbers


# Generations permutations numbers
def numbers_permutations(numbers, max_password_length):
    permutation_numbers = []
    for x in range(len(numbers) + 1):
        for comb in permutations(numbers, x):
            tmp = ''.join(comb)
            if len(tmp) <= max_password_length:
                permutation_numbers.append(tmp)

    permutation_numbers = set(permutation_numbers)
    # Combinations generates an empty element
    try:
        permutation_numbers.remove('')
    except:
        pass
    return permutation_numbers


# Generates a dictionary by organizing elements of equal sizes
# Receives a list and returns a dictionary
def separates_elements_by_size(elements):
    dictionary = {}
    for element in elements:
        size = len(element)
        if size in dictionary:
            dictionary[size].append(element)
        else:
            dictionary[size] = [element]

    return dictionary


# Divides the formats to make it easier to generate passwords in the format
def split_formats(formats_quantity, min_password_length, max_password_length):
    splitted_formarts = []

    with open(PATH_FORMATS, 'r') as formats_file:
        password_formats = formats_file.read().splitlines()
        for password_format in password_formats:
            if len(password_format) < min_password_length or len(password_format) > max_password_length:
                continue
            index = 0
            splitted_formart = []
            current_format = ''
            while index < len(password_format):
                if password_format[index] == 'X' or password_format[index] == 'y':
                    while password_format[index] == 'X' or password_format[index] == 'y':
                        current_format += password_format[index]
                        index += 1
                        # Stop before it breaks out of range
                        if index == len(password_format):
                            break
                elif password_format[index] == '@':
                    while password_format[index] == '@':
                        current_format += '@'
                        index += 1
                        # Stop before it breaks out of range
                        if index == len(password_format):
                            break
                elif password_format[index] == '9':
                    while password_format[index] == '9':
                        current_format += '9'
                        index += 1
                        # Stop before it breaks out of range
                        if index == len(password_format):
                            break
                else:
                    print("Invalid Format!!!\n")
                    break
                splitted_formart.append(current_format)
                current_format = ''
            splitted_formarts.append(splitted_formart)
            if len(splitted_formarts) == formats_quantity:
                return splitted_formarts
    return splitted_formarts
            

# Generates passwords with formats from the format list
def generates_passwords(splitted_formarts, dictionary_words, dictionary_numbers):
    # Special characters used
    symbols = ['@', '#', '!', '$', '%', '&', '*']
    passwords = []
    for splitted_formart in splitted_formarts:
        try:
            splitted_password = []
            for element in splitted_formart:
                temporary_password = []
                # Generates a list of words formatted in upper and lower case
                if 'y' in element or 'X' in element:
                    splitted_words = []
                    for word in dictionary_words[len(element)]:
                        # Splitted word for capitalization
                        splitted_word = []
                        # Auxiliary splitted word with their uppercase and lowercase letters in their places
                        aux_word = []
                        # Capitalize the letters
                        for c in word:
                            splitted_word.append(c)
                        for i in range(len(element)):
                            if element[i] == 'X':
                                aux_word.append(splitted_word[i].upper())
                            else:
                                aux_word.append(splitted_word[i])
                        # Word with their uppercase and lowercase letters in their places
                        splitted_words.append(''.join(aux_word))
                    # If it is a continuation of a password
                    if splitted_password:
                        for x in splitted_password:
                            for y in splitted_words:
                                temporary_password.append(x + y)
                    # If it is a new password
                    else:
                        for word in splitted_words:
                            splitted_password.append(word)
                elif '9' in element:
                    # If it is a continuation of a password
                    if splitted_password:
                        for x in splitted_password:
                            for y in dictionary_numbers[len(element)]:
                                temporary_password.append(x + y)
                    # If it is a new password
                    else:
                        for number in dictionary_numbers[len(element)]:
                            splitted_password.append(number)
                elif '@' in element:
                    list_symbols = []
                    for comb in permutations(symbols, len(element)):
                        list_symbols.append(''.join(comb))
                    # If it is a continuation of a password
                    if splitted_password:
                        for x in splitted_password:
                            for y in list_symbols:
                                temporary_password.append(x + y)
                        splitted_password = temporary_password
                        temporary_password = []
                    # If it is a new password
                    else:
                        for symbol in list_symbols:
                            splitted_password.append(symbol)
                if temporary_password:
                    splitted_password = temporary_password
            for password in splitted_password:
                passwords.append(password)
        # If there is an exception, it is because
        # There are no words or numbers the size of the password format.
        except:
            print("Could not generate password in the format: ", ''.join(splitted_formart))

    return passwords


# Write passwords to the Wordlist file
def write_passwords(passwords):
    with open(PATH_WORDLIST, 'w') as wordlist_file:
        for x in passwords:
            wordlist_file.write(x + '\n')


# Collect target tweets
def collect_tweets():
    # API authentication
    API_KEY = input("What's your API KEY? ")
    API_SECRET = input("What's your API SECRET? ")
    ACESS_TOKEN = input("What's your ACESS TOKEN? ")
    TOKEN_SECRET = input("What's your TOKEN SECRET? ")
    auth = OAuthHandler('API_KEY', 'API_SECRET')
    auth.set_access_token('ACESS_TOKEN', 'TOKEN_SECRET')
    api = API(auth)
    user = input("Enter the target's @:\n"
                 "Example VictorSalles__ <-- My Twitter :)\n"
                 "@")

    # Collect and write tweets to the file
    with open(PATH_TWEETS, 'w', encoding="utf-8") as tweet_file:
        try:
            for status in Cursor(api.user_timeline,
                                 id=user,
                                 count=200,
                                 tweet_mode='extended').items():

                tweets = sub(r'http\S+', '\n', status.full_text)
                tweet_file.write(tweets)
            input("Collected Tweets\n\n"
                  "Press Enter for continue... ")
        except:
            input("Invalid API credentials or User not found!\n\n"
                  "Press Enter for continue... ")


# Analyzes tweets and generates a file
# With the reference words for creating passwords
def tweets_analyzer():
    # Read tweets and tokenize
    with open(PATH_TWEETS, 'r', encoding="utf-8")as tweets_file:
        tweets = tweets_file.read()
    tokens = word_tokenize(unidecode(tweets))
    # Lowercase and punctuation or emoticons
    # Assuming there may be a loss of information, like @Lakers. or Neymar!
    # However, as we will make a count of the most cited words
    # I believe that this loss will not be relevant
    words = []
    for token in tokens:
        if token.isalnum():
            words.append(token.lower())
    # Gets the path of each file containing reference words
    # And generates a list of reference words
    reference_words = []
    for file in listdir(PATH_REFERENCES):
        path_file = PATH_REFERENCES + file
        with open(path_file, 'r', encoding='utf8') as references_file:
            references = references_file.read().split()
            for word in words:
                if word in references:
                    reference_words.append(word)
    return reference_words


# Returns the number of the choice
def menu(entry):
    choice = 0
    # Main menu
    if entry == 0:
        while choice < 1 or choice > 4:
            system(CLEAR)
            try:
                choice = int(input("1 - Analyze word list\n"
                                   "2 - Generate word list from file\n"
                                   "3 - Generate word list from Twitter - (coming soon)\n"
                                   "4 - Exit\n"
                                   "Choice: "))
            except:
                print("Only numbers are allowed!\n\n"
                      "Press Enter for continue... ")
        return choice

    # Analyze or generate word list
    elif entry == 1 or entry == 2:
        while True:
            system(CLEAR)
            try:
                formats_quantity = int(input("How many formats do you want to use? "))
                break
            except:
                input("Only numbers are allowed!\n\n"
                      "Press Enter for continue... ")
        while True:
            try:
                min_password_length = int(input("What is the minimum password length? "))
                max_password_length = int(input("What is the maximum password length? "))
                break
            except:
                input("Only numbers are allowed!\n\n"
                      "Press Enter for continue... ")
        # Analyze word list
        if entry == 1:
            # +1 because the size in wordlist_analyzer
            # Gets len + 1, because its position 0 is not used
            return formats_quantity, min_password_length, max_password_length + 1
        # Generate word list
        elif entry == 2:
            return formats_quantity, min_password_length, max_password_length


# Main Function
def main():
    option = 0
    while option != 4:
        # Main menu
        option = menu(0)

        # Analyze word list
        if option == 1:
            formats_quantity, min_password_length, max_password_length = menu(1)
            wordlist_analyzer(formats_quantity, min_password_length, max_password_length)

        # Generate word list
        elif option == 2:
            formats_quantity, min_password_length, max_password_length = menu(2)
            generates_wordlist(formats_quantity, min_password_length, max_password_length)

        # Generate word list with Twitter
        elif option == 3:
            print("This function will be available soon :)\n")
            input("Press Enter for continue... ")

    print("See you later, Bye :)\n")


main()
