import requests
from flask import Flask, make_response, request, render_template, render_template_string
import random
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index2.html')

def easy_mode_data(num_words=4,delimiter="-",case_opt="lower",min_chars=4,max_chars=5,lang="en"):
    print("Easy")
    word_file="words.txt"
    word_source = [line.strip() for line in open(word_file, 'r')]
    word_list=[]
    for i in range(num_words):
        word=random.sample(word_source,1)[0]
        while (len(word) < min_chars or len(word) > max_chars):
            word=random.sample(word_source,1)[0]
        word_list.append(word)
    random_words=word_list
    return random_words

def advanced_mode_data(num_words=4,delimiter="-",case_opt="lower",min_chars=4,max_chars=5,lang="en"):
    print("advanced")
    word_list=[]
    API_URL = "https://random-word-api.herokuapp.com/word?"
    URL=API_URL+"lang="+lang+"&length="
    for i in range(int(num_words)):
        random_word_length=random.choice([min_chars,max_chars])
        try:
            word=requests.get(URL+str(random_word_length))
            word.raise_for_status()
            random_word = word.json()[0]
            word_list.append(random_word)
        except Exception as e:
             word = "Error"
    random_words=word_list
    return random_words


@app.route("/<mode>")
@app.route("/<api>/<mode>")
def easy_mode_web(api=None,mode=None):
    num_words = request.args.get('num_words', default = 4, type = int)
    delimiter = request.args.get('delim', default = "-", type = str)
    case_opt = request.args.get('case', default = "lower", type = str)
    min_chars = request.args.get('min_chars', default = 4, type = int)
    max_chars = request.args.get('max_chars', default = 5, type = int)
    match mode:
        case "easy":
            template='easy2.html'
            lang = "en"
            languages = "en"
            word_list = easy_mode_data(num_words,delimiter,case_opt,min_chars,max_chars,lang)
        case "advanced":
            template='advanced2.html'
            lang = request.args.get('lang', default = "en", type = str)
            languages = ["en","es","it","de","fr","zh"]
            word_list = advanced_mode_data(num_words,delimiter,case_opt,min_chars,max_chars,lang)
        case _:
            lang = "en" 

    brute_force_estimate = brute_force_time(10000,num_words, 60)

    match api:
        case "api":
            response = {"password" : '-'.join(word_list),
                        "brute_force_time": brute_force_estimate, 
                        "word count": num_words,
                        "delimiter": delimiter,
                        "case option": case_opt,
                        "min word chars": min_chars,
                        "max word chars": max_chars,
                        "language": lang}
        case _:
                response = render_template(template,words=word_list, crack=brute_force_estimate, delimiter=delimiter, current_num_words=num_words, min_word_length=min_chars, max_word_length=max_chars, lang=lang, languages=languages )
    return response



def brute_force_time(word_list_size, num_words, guesses_per_second):
    total_combinations = word_list_size ** num_words
    average_guesses = total_combinations / 2
    time_seconds = average_guesses / guesses_per_second
    time_years = time_seconds / (60 * 60 * 24 * 365.25)
    response = '{0:.2f}'.format(time_years)
    response = "Approx "+response+" years to brute force"
    return response

if __name__ == "__main__":
    app.run(static_folder='static/', debug=True)

