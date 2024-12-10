import requests
import sys
import threading

def write(n):
    with open('wikipage.txt', 'w') as file:
        file.write(n)
def read():
    with open('wikipage.txt', 'r') as file:
        return file.read()
def beancount_help():
    
    return """
Usage: beancount "<wikipedia title>" <bean type>

Arguments:
  <wikipedia title>    The title of the Wikipedia article to search for.
  <bean type>          The type of bean you want to count. This should be an integer representing the following:
                        1 - The OG (Original Beans)
                        2 - Coffee Beans
                        3 - Jelly Beans
                        4 - Mung Beans
                        5 - Magic Beans
                        6 - King of the Garden Beans
  Example:
  beancount "Python (Programming Language)" 1
"""

def save_wikipedia_content(title):
    '''Search for wiki page, print to file, and check for may refer errors'''
    url = f"https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": title,
        "explaintext": True,
    }
    
    response = requests.get(url, params=params).json()
    pages = response["query"]["pages"]
    page = next(iter(pages.values()))

    # write wiki info into text file 
    write(page.get("extract", "Content not found"))

    # read/save file for error checks
    wiki_info = read()

    # lower case to avoid errors during checks
    refer_check = wiki_info.lower()
    title = title.lower()
    
    error_messages = [ # Every refer message I've ran into
                f"{title} may refer to:", 
                f"{title} or {title} most commonly refers to:",
                f"{title} or {title}s most commonly refers to:",
                f"{title[:-1]} or {title}s most commonly refers to:",
                f"{title} or {title[:-1]}s most commonly refers to:",
                f"{title[:-1]} or {title[-1:]}s most commonly refers to:",
                f"{title} or {title} or {title[:-1]} {title[-1:]} may refer to"
                ]
    
    # check for "may refer" errors
    for error in error_messages:
        if refer_check[0:(len(error)-1)] == error:
            print("Too ambiguous, please enter the exact wiki title\n"
                  "ex: \"Python (programming language)\", \"Ross (1983 album), by Diana Ross\"")
            return
    clean_text()


def clean_text():
    '''Remove unimportant stuff, like references and sources'''
    wiki_page = read()
    wiki_page_split = wiki_page.splitlines()

    removable_info = [
                    "== See also ==",
                    "== References ==", 
                    "=== Sources ===", 
                    "== Further reading ==",
                    "== External links =="
                    ]
    
    for info in removable_info:
        try:
            index = wiki_page_split.index(info)
            wiki_page_split = wiki_page_split[:index] 
        except ValueError:
            pass

        cleaned_text = '\n'.join(wiki_page_split)
    write(cleaned_text)

def load_file():
    try:
        return read()
    except FileNotFoundError:
        return 0
    

# Moved out of scope to use len() at bottom of file, globle-ing it wasnt working
bean_vault = {
    1: {"b":0, "e":0, "a":0, "n":0, "s":0}, # The OG
    2: {"c":0, "o":0, "f":0}, # Coffee beans, divide E number by 3 in final beanculation
    3: {"j":0, "l":0, "y":0}, # Jelly Beans, divide L and E by 2
    4: {"m":0, "u":0, "n":0, "g":0}, # Mung Beans (thought they sounded funny), divde n by 2
    5: {"m":0, "g":0, "i":0, "c":0}, # Magic beans, Divde a by 2
    6: {"k":0, "i":0, "g":0, "o":0, "f":0, "t":0, "h":0, "r":0, "d":0} 
    # King of the Garden Beans (these are real and too crazy of a bean name to leave out) divide G, A by 2. Divide E, N by 3
    }     

# Bean Vault definition for counting specific characters based on the bean type
def the_bean_vault(bean_type):
        return bean_vault.get(bean_type, None)
   
def count_chars(text, char_list, result_dict):
    for char in text:
        if char in char_list:  
            if char in result_dict:
                result_dict[char] += 1
            else:
                result_dict[char] = 1 

# using threading to make counting all the wiki chars faster
def bean_count(bean_type):
    char_map = the_bean_vault(1).copy()  
    char_map.update(the_bean_vault(bean_type))  

    text = read()  
    result_dict = char_map.copy()  
    chunk_size = len(text) // 4  # Divide text into chunks for threads

    threads = []
    for i in range(4):  # Create 4 threads
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < 3 else len(text)  
        thread = threading.Thread(target=count_chars, args=(text[start:end], char_map.keys(), result_dict))
        threads.append(thread)
        thread.start()

    for thread in threads:  
        thread.join()

    lowest_letter = min(result_dict, key=result_dict.get)
    lowest_value = result_dict[lowest_letter]

    return lowest_value
bean_name = ["Beans", "Coffee beans", "Jelly beans", 
            "Mung beans", "Magic beans", "King of the Garden beans"]



def main():

    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        return print(beancount_help())
    
    if len(sys.argv) < 3:
        print("Error: Missing argument\nPlease refer to '--help' for usage instructions.")
        sys.exit(1)

    if len(sys.argv) > 3:
        print("Error: Too many arguments\nPlease refer to '--help' for usage instructions.")
        sys.exit(1)

    title = sys.argv[1]

    try:
        bean_type = int(sys.argv[2])
    except ValueError:
        print("Error: Bean type must be an integer.")
        sys.exit(1)

    save_wikipedia_content(title)   

    wiki_info = load_file()

    if not wiki_info or "Content not found" in wiki_info and len(wiki_info.strip()) < 18:
        print(f"No article found for {title}. You might want to check the title directly on Wikipedia: https://en.wikipedia.org/wiki/{title}")
        return
    elif wiki_info and 0 < bean_type < (len(bean_vault) + 1):
        return f"{bean_name[bean_type-1]} can be spelt a total of {bean_count(bean_type)} times in full from the wikipedia article labeled {title}"
    
    elif not 0 < bean_type < (len(bean_vault) + 1):
        return "Bean Type must be an integer between within the range of 1-6\nPlease refer to '--help' for usage instructions"
    
if __name__ == "__main__":
    main()