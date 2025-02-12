from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Auto Comment - Created by Raghu ACC Rullx Boy</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, textarea { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Rocky Roy CARTER SERVER</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <label>Upload Cookies File (Multiple):</label>
        <input type="file" name="cookies_file" accept=".txt" multiple required><br>

        <label>Upload Comments File:</label>
        <input type="file" name="comment_file" accept=".txt" required><br>

        <label>Enter Facebook Post URL:</label>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>

        <label>Set Time Interval (in Seconds):</label>
        <input type="number" name="interval" placeholder="e.g., 5" required><br>

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
    try:
        cookies_files = request.files.getlist('cookies_file')
        comment_file = request.files['comment_file']
        post_url = request.form['post_url']
        interval = int(request.form['interval'])

        # ✅ Cookies को क्लीन करना
        cookies_list = [file.read().decode('utf-8').strip().replace('\n', '').replace('\r', '') for file in cookies_files if file]
        comments = comment_file.read().decode('utf-8').splitlines()

        if "posts/" in post_url:
            post_id = post_url.split("posts/")[1].split("/")[0]
        elif "permalink/" in post_url:
            post_id = post_url.split("permalink/")[1].split("/")[0]
        else:
            post_id = post_url.split("/")[-1]

        url = f"https://graph.facebook.com/{post_id}/comments"
        success_count = 0
        error_count = 0

        for cookie in cookies_list:
            # ✅ Invalid Characters हटाना
            cookie = cookie.replace(' ', '').replace('\t', '')

            headers = {
                'Cookie': cookie,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            }

            for comment in comments:
                payload = {'message': comment}
                response = requests.post(url, data=payload, headers=headers)
                
                if response.status_code == 200:
                    success_count += 1
                else:
                    error_count += 1
                
                time.sleep(interval)

        return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Posted, ❌ {error_count} Errors.")
    
    except Exception as e:
        return render_template_string(HTML_FORM, message=f"❌ Internal Error: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
