from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Auto Comment - Created by Rocky Roy CARTER SERVER</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, textarea { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Created by Rocky Roy CARTER SERVER</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <label>Upload Cookies File:</label>
        <input type="file" name="cookies_file" accept=".txt" required><br>

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
    cookies_file = request.files['cookies_file']
    comment_file = request.files['comment_file']
    post_url = request.form['post_url']
    interval = int(request.form['interval'])

    cookies_list = cookies_file.read().decode('utf-8').splitlines()
    comments = comment_file.read().decode('utf-8').splitlines()

    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    success_count = 0

    def post_comment_with_cookies(cookies, comment):
        url = f"https://m.facebook.com/{post_id}/add_comment/"
        headers = {
            'Cookie': cookies,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile; rv:102.0) Gecko/102.0 Firefox/102.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {'comment_text': comment}
        response = requests.post(url, data=payload, headers=headers)
        return response.status_code == 200

    for cookies in cookies_list:
        for comment in comments:
            if post_comment_with_cookies(cookies, comment):
                success_count += 1
                print(f"✅ Comment Successful: {comment}")
            else:
                print(f"❌ Failed to Comment: {comment}")
            time.sleep(interval)

    return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Successfully Posted!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
