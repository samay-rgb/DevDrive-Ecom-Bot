from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from flask import Flask, render_template, request
from chatterbot.response_selection import get_random_response
import logging
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)


def remove_hyphens(statement):
    """
    Remove hypnens.
    """
    statement.text = statement.text.replace('-', '')
    return statement


app = Flask(__name__)
bot = ChatBot(name='Anakin', read_only=True,
              response_selection_method=get_random_response,
              storage_adapter='chatterbot.storage.SQLStorageAdapter',
              database_uri='sqlite:///database.sqlite3',
              logic_adapters=[
                  {
                      'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                      'input_text': 'empty',
                      'output_text': ''
                  },
                  {
                      'import_path': 'chatterbot.logic.BestMatch',
                      'default_response': 'i honestly have no idea how to respond to that',
                      'maximum_similarity_threshold': 0.9
                  },
                  {
                      'import_path': 'chatterbot.logic.MathematicalEvaluation'
                  }

              ]

              )
bot.preprocessors.append(
    remove_hyphens
)
trainer = ChatterBotCorpusTrainer(bot)
trainer.train(
    "data/greetings.yml",
    "data/ecom.yml"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    req = request.args.get("msg")
    if req.lower() == 'bye' or req.lower() == 'thanks' or req.lower() == 'get lost':
        return ("Hope I was able to help you.Thank you.Have a good day")
    elif (req.lower().find("search") != -1):
        #item=req[6:]+"on flipkart"
        try:
            from googlesearch import search
        except ImportError:
            print("No module named 'google' found")

        query = req[6:]+" on flipkart"
        # print("Bot: Select any link and find your desired product on flipkart ,amazon and other trusted sites. Happy shopping!")
        for j in search(query, tld="co.in", num=5, stop=5, pause=2):
            return j

    else:
        response = bot.get_response(req)
        return str(response)


if __name__ == "__main__":
    app.run(debug=True)
