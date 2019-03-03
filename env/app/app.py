import re
from nltk.tokenize import RegexpTokenizer

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SemanticRolesOptions, ConceptsOptions


import paralleldots



from flask import Flask, render_template, request
from flask_material import Material
app = Flask(__name__)


Material(app)
@app.route('/')
def hello():
   return render_template('index.html')


@app.route('/send', methods = ['GET', 'POST'])
def login_page():
   #error = ''
   try:

       if request.method == "POST":

           text = request.form['age']
           print(text)
           #attempted_password = request.form['password']

           rtext, rlabel, rvalue = redictedText(text)
           context = {
               'rtext': rtext,
               'rlabel': rlabel,
               'rvalue': rvalue,
               'rinputtext':text
           }


           return render_template("print.html", context = context)

   except Exception as e:
       # flash(e)
       return render_template("index.html")

"""
@app.route('/send/<age>')
def send(age):
   context = {
       "rtext": redictedText(age)
   }
   return render_template('send.html', context = context)
   """

# def send():
#     if request.method == 'POST':
#         age = request.form['age']
#
#         return render_template('send.html', age = age)
#
#     return render_template(('index.html'))



def redictedText(text):



   paralleldots.set_api_key("RPy5b3CAGG60DZvjDRHNcVKEzybZvlUQF3zEUntDHIU")
   possibleGender = ['he', 'she', 'male', 'female', 'transgender', 'lesbain', 'his', 'her', 'him']

  # print("Enter any input")

   # tokenized = sent_tokenize(text)
   # print(tokenized)

   tokenizer = RegexpTokenizer(r'\w+')
   txt = tokenizer.tokenize(text)
   resultedText = " ".join(txt)
   # print(resultedText)

   aadhar = (re.findall(r'\d{1,12}', text))

   num = []
   num += aadhar
   num += possibleGender

   # print(num)

   print("\n")

   try:
       wordsFromApi = []
       response = paralleldots.ner(resultedText)
       # print(response)

       # print(response['entities'])
       res = response['entities']
       for i in range(len(res)):
           dic = res[i]
           # print(dic['name'])
           wordsFromApi += (dic['name'].split())

       num += wordsFromApi
       # print(num)

   except Exception as e:
       print(str("failed to recognize your text. please check your internet connection :("))

   redictedText = ""
   resultedList = resultedText.split()
   for i in resultedList:
       # print(i)
       if (i in num) or ((i.lower()) in num):
           redictedText += "*"
       else:
           redictedText += i
       redictedText += " "

   # using IBM api
   natural_language_understanding = NaturalLanguageUnderstandingV1(
       username='8b8545e7-9755-4efa-b65a-53fcbbe340ac',
       password='IakHD0SFzN5a',
       version='2018-11-16')

   response = natural_language_understanding.analyze(
       text=text,
       features=Features(entities=EntitiesOptions(sentiment=True))).get_result()


   resultFromIBM = []
   relevanceFromIBM = []
   for key in response['entities']:
       # print(key)
       resultFromIBM.append(key['text'])
       relevanceFromIBM.append(key['relevance'])
   arr = [str(r) for r in resultFromIBM]

   return redictedText, arr, relevanceFromIBM

if __name__ == "__main__":
   app.run()