from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Auto Comment - Created by Rocky Roy</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, textarea { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Created by Rocky Roy</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <input type="file" name="token_file" accept=".txt"><br>
        <input type="file" name="cookies_file" accept=".txt"><br>
        <input type="file" name="comment_file" accept=".txt" required><br>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>
        <input type="number" name="interval" placeholder="Interval in Seconds (e.g., 5)" required><br>
        <button type="submit">Submit Your Details</button>
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
    cookies_file = request.files.get('cookies_file')
    comment_file = request.files.get('comment_file')
    post_url = request.form['post_url']
    interval = int(request.form['interval'])

    comments = comment_file.read().decode('utf-8').splitlines()
    tokens = token_file.read().decode('utf-8').splitlines() if token_file else []
    cookies_list = cookies_file.read().decode('utf-8').splitlines() if cookies_file else []

    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    url = f"https://graph.facebook.com/{post_id}/comments"
    success_count = 0

    # First try with tokens
    for token in tokens:
        for comment in comments:
            payload = {'message': comment, 'access_token': token}
            response = requests.post(url, data=payload)

            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 400:
                continue  # Invalid token, skip
            else:
                continue  # Other errors, skip

            time.sleep(interval)

    # If token fails, try with cookies
    for cookies in cookies_list:
        headers = {'Cookie': cookies, 'User-Agent': 'Mozilla/5.0'}
        for comment in comments:
            payload = {'message': comment}
            response = requests.post(url, data=payload, headers=headers)

            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 400:
                continue  # Invalid cookies, skip
            else:
                continue  # Other errors, skip

            time.sleep(interval)

    return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Successfully Posted!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
