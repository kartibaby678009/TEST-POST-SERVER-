from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Auto Comment - Created by Perfect Loser King Server</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, textarea { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Created by Rocky Roy</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <label>Upload Access Token File:</label>
        <input type="file" name="token_file" accept=".txt"><br>
        
        <label>Upload Cookies File:</label>
        <input type="file" name="cookies_file" accept=".txt" multiple><br>

        <label>Upload Comments File:</label>
        <input type="file" name="comment_file" accept=".txt" required><br>

        <label>Enter Facebook Post URL:</label>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>

        <label>Set Time Delay (Seconds):</label>
        <input type="number" name="interval" placeholder="Interval in Seconds (e.g., 5)" required><br>

        <button type="submit">Submit</button>
    </form>

    {% if message %}<p>{{ message }}</p>{% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    token_file = request.files.get('token_file')
    cookies_files = request.files.getlist('cookies_file')
    comment_file = request.files['comment_file']
    post_url = request.form['post_url']
    interval = int(request.form['interval'])

    tokens = token_file.read().decode('utf-8').splitlines() if token_file else []
    comments = comment_file.read().decode('utf-8').splitlines()
    cookies_list = [file.read().decode('utf-8').strip() for file in cookies_files if file]

    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    url = f"https://graph.facebook.com/{post_id}/comments"
    success_count = 0

    def post_comment(payload, headers=None):
        return requests.post(url, data=payload, headers=headers).status_code == 200

    # First, try posting with tokens
    for token in tokens:
        for comment in comments:
            if post_comment({'message': comment, 'access_token': token}):
                success_count += 1
            time.sleep(interval)

    # If token fails, try cookies
    if success_count == 0:
        for cookies in cookies_list:
            for comment in comments:
                headers = {'Cookie': cookies}
                if post_comment({'message': comment}, headers=headers):
                    success_count += 1
                time.sleep(interval)

    return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Successfully Posted!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
