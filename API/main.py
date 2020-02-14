from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return """
        <html>
            <form method = post enctype = multipart/form-data>
                <label> Enter query </label > <input type = "text" name = "query">
                <br>
                <input type = "submit">
            </form>
        </html>
        """
    else:
        query = request.form['query']
        resp = requests.get(
            "https://api.stackexchange.com/2.2/similar?order=desc&sort=relevance&title="+query+"&site=stackoverflow")
        items = resp.json()["items"]
        links = ""
        for item in items:
            if item["is_answered"]:
                links = item["link"]
                break
        print(links)
        if links == "":
            return """
            <html>
                <h1>No Webpage exists</h1>
                <form method = post enctype = multipart/form-data>
                    <label> Enter query </label > <input type = "text" name = "query">
                    <br>
                    <input type = "submit">
                </form>
            </html>
            """
        return redirect(links)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
