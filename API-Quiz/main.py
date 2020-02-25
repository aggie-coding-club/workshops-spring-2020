from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
import os
from datetime import datetime

app = Flask(__name__)
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
firestore_document = db.collection('apiDemo').document('ApiLeaderboard')


@app.route('/', methods=['GET', 'POST'])
def home():
    # GET
    if request.method == 'GET':

        # if get return a form
        return """
        <html>
            <form method = post enctype = multipart/form-data>
                <label> Enter query </label > <input type = "text" name = "query">
                <br>
                <input type = "submit">
            </form>
        </html>
        """

   # POST
    else:
        # get form query
        query = request.form['query']

        # get links from the user generated query
        resp = requests.get(
            "https://api.stackexchange.com/2.2/similar?order=desc&sort=relevance&title=" + query + "&site=stackoverflow")

        # get items form the API response
        items = resp.json()["items"]

        # get the first answered link
        link = ""
        for item in items:
            if item["is_answered"]:
                link = item["link"]
                break

        # if no answers return No Answer Exists
        if link == "":
            return """
            <html>
                <h1>No Answers exists</h1>
                <form method = post enctype = multipart/form-data>
                    <label> Enter query </label > <input type = "text" name = "query">
                    <br>
                    <input type = "submit">
                </form>
            </html>
            """

        # If link exists, redirect to it
        return redirect(link)


# new shit from here
@app.route('/gettingstarted', methods=['GET'])
def gettingStarted():
    return {"title": "Welcome to the Aggie Coding Club API Workshop activity! To get started, find the instructions section below",
            "instructions": "Congrats on making the first GET request. In order to continue to the next step, please make another HTTP request as described below. After the next request is made, you will receive certain riddles, puzzles, or ACC/A&M trivia. You must be making your requests through code (we will check!). The top winners will have the chance to win a prize TBD. Ready, GET set, POST!",
            "question": "",
            "next_request": {
                "method_type": "GET",
                "url": "https://api-acc.appspot.com/supersmashtrivia",
                "params": '[]',
                "hint": "no parameters for this request other than the url is needed"
            }
            }


@app.route('/supersmashtrivia', methods=['GET', 'POST'])
def supersmashtrivia():
    if request.method == 'GET':
        return {"title": "It's time for a little Super Smash trivia. Don't worry it's easy, especially if you been keeping up with our Kahoots ;)",
                "instructions": "well, looks like you are GETting the hang of This, Right? the Answer to the queStion below Has 1 word. you will need to make a post request in order to receive the next question. don't overthink it, but if you need a hint, look below in the next request data!",
                "question": "Workshop chair Edgar loves his super smash characters, but the way he describes the character Little Mac is one of great depth and revelation. Some agree, some disagree. The correct answer is hidden in plain sight. Read back into the instructions and submit the ONE word answer as the parameter described below!",
                "next_request": {
                    "method_type": "POST - Yes! You can send a POST and a GET request to the same route. Infact, a route can support as many methods as you want.",
                    "url": "https://api-acc.appspot.com/supersmashtrivia",
                    "params": {"answer": "YOUR ANSWER HERE"},
                    "hint": "CAPITALIZE on the fact that there are only a couple words different in the instructions. Just Read The Instructions and find the hidden answer."
                }

                }
    if request.method == 'POST':
        if (('answer' in request.get_json()) and (request.get_json()['answer'] == 'TRASH')):
            return {"title": "Hot Stuff! 1 Down just a BIT more to go. Are you reading carefully? DoNt woRRy, This oNe isn’t That haRd. Haha you tried to make a word out of that right? What did you GET? Alright keep going...",
                    "instructions": "This is fun right? Well, for this next step, open up your favorite browser and make sure your computer has the CAPACITY for this next question. Alright theres going to be some duck duck GOing and GOogling, but don’t look too deep, because you never know what you'll miss.",
                    "question": "The semester started out in HRBB, lots of great people, learning and projects. The room we were in was just down the hall. EVEN it was, but now not at all. ODD right? Well the first part of this question is anything but. The answer to the question is a 3 DIGIT INTEGER. ADD the room number of the old room to it’s room CAPACITY and you’ll get your answer. Don’t know the room capacity? Read the hint below.",
                    "next_request": {
                        "method_type": "POST",
                        "url": "https://api-acc.appspot.com/roomcapacity",
                        "params": {"answer": "YOUR_NUMBER_HERE"},
                        "hint": "make your search broad and your answer will come first, can’t find the page? The office of the registrar website will contain the answer, with a little additional digging."
                    }

                    }
        else:
            return {"title": "OOPS! Wrong answer! IT is definitely not OP. It's time for a little Super Smash trivia. Don't worry it's easy, especially if you been keeping up with our Kahoots ;)",
                    "instructions": "well, looks like you are GETting the hang of This, Right? the Answer to the queStion below Has 1 word. you will need to make a post request in order to receive the next question. don't overthink it, but if you need a hint, look below in the next request data!",
                    "question": "Workshop chair Edgar loves his super smash characters, but the way he describes the character Little Mac is one of great depth and revelation. Some agree, some disagree. The correct answer is hidden in plain sight. Read back into the instructions and submit the ONE word answer as the parameter described below!",
                    "next_request": {
                        "method_type": "POST - Yes! You can send a POST and a GET request to the same route. Infact, a route can support as many methods as you want.",
                        "url": "https://api-acc.appspot.com/supersmashtrivia",
                        "params": {"answer": "YOUR ANSWER HERE"},
                        "hint": "OOPS! Wrong answer! IT is definitely not OP. CAPITALIZE on the fact that there are only a couple words different in the instructions. Just Read The Instructions and find the hidden answer."
                    }

                    }


@app.route('/roomcapacity', methods=['POST'])
def roomcapacity():
    if (('answer' in request.get_json()) and (request.get_json()['answer'] == 259 or request.get_json()['answer'] == '259')):
        return {
            "title": "Rooting for you! You are so very CLOSE. Don’t get too ahead of yourself or you might DELETE information you need. One POST away from claiming a spot on the board. But how is your code looking?",
            "instructions": "Copy and paste is a strategy but you will need a couple more numbers to complete this challenge. Alright this is gonna be another POST request but you got this in the bag. Hope you didn’t close out that last tab, you will need it again ;). Alright open up that website one more time. The answer will be a 4 DIGIT number. Don’t forget to PUT your full name. Continue to the instructions..",
            "question": "HERE we are. In this room the website PICTURES.",
            "next_request": {
                "method_type": "PUT",
                "url": "https://api-acc.appspot.com/mytimetoshine",
                "params": {"answer": "YOUR_NUMBER_HERE", "name": "Your name here or LittleMacTrash"},
                "hint": "Let’s go!!! You are on the clock!"
            }

        }

    else:
        return {
            "title": "OOPS! CANT COUNT?!? answer = HRBB 124 room capacity + 124! 1 Down just a BIT more to go. Are you reading carefully? DoNt woRRy, This oNe isn’t That haRd. Haha you tried to make a word out of that right? What did you GET? Alright keep going...",
            "instructions": "This is fun right? Well, for this next step, open up your favorite browser and make sure your computer has the CAPACITY for this next question. Alright theres going to be some duck duck GOing and GOogling, but don’t look too deep, because you never know what you'll miss.",
            "question": "The semester started out in HRBB, lots of great people, learning and projects. The room we were in was just down the hall. EVEN it was, but now not at all. ODD right? Well the first part of this question is anything but. The answer to the question is a 3 DIGIT INTEGER. ADD the room number of the old room to it’s room CAPACITY and you’ll get your answer. Don’t know the room capacity? Read the hint below.",
            "next_request": {
                "method_type": "POST",
                "url": "https://api-acc.appspot.com/roomcapacity",
                "params": {"answer": "YOUR_NUMBER_HERE"},
                "hint": "OOPS! CANT COUNT?!? answer = HRBB 124 room capacity + 124! make your search broad and your answer will come first, can’t find the page? The office of the registrar website will contain the answer, with a little additional digging."
            }

        }


@app.route('/mytimetoshine', methods=['PUT'])
def mytimetoshine():
    if (('answer' in request.get_json()) and ('name' in request.get_json()) and (request.get_json()['answer'] == 1124 or request.get_json()['answer'] == '1124')):
        print(firestore_document.get().to_dict())
        winner = firestore_document.get().to_dict()['Winner']
        winner.append(
            (request.get_json()['name'] + " - " + str(datetime.now())))
        firestore_document.update({'Winner': winner})
        return "Please confirm that you name is on the board. \n BAZINGA! You got it. Yell BAZINGA or LITTLEMACTRASH and we will be with you shortly."

    else:
        return {
            "title": "Rooting for you! You are so very CLOSE. Don’t get too ahead of yourself or you might DELETE information you need. One POST away from claiming a spot on the board. But how is your code looking?",
            "instructions": "Copy and paste is a strategy but you will need a couple more numbers to complete this challenge. Alright this is gonna be another POST request but you got this in the bag. Hope you didn’t close out that last tab, you will need it again ;). Alright open up that website one more time. The answer will be a 4 DIGIT number. Don’t forget to PUT your full name. Continue to the instructions..",
            "question": "HERE we are. In this room the website PICTURES.",
            "next_request": {
                "method_type": "PUT",
                "url": "https://api-acc.appspot.com/mytimetoshine",
                "params": {"answer": "YOUR_NUMBER_HERE", "name": "Your name here or LittleMacTrash"},
                "hint": "WHOOPS! answer =  GO TO CLOCK... Let’s go!!! You are on the clock!"
            }

        }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
