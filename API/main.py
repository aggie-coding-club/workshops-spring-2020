from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)


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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
