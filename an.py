from flask import Flask, render_template_string, request
import time
import random
import os

app = Flask(__name__)

# HTML + CSS Embedded in Python
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carter by Rocky Roy</title>
    <style>
        body {
            background: linear-gradient(to right, red, white, blue, gold);
            color: white;
            text-align: center;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 400px;
            margin: auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 10px;
            box-shadow: 0px 0px 10px gold;
        }
        h1 {
            color: gold;
            text-shadow: 2px 2px 10px white;
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border: 1px solid gold;
            background: rgba(255, 255, 255, 0.2);
            color: white;
        }
        button {
            background-color: gold;
            color: black;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0px 0px 10px white;
        }
        .background {
            background-image: url('https://source.unsplash.com/600x400/?crazy');
            background-size: cover;
            background-position: center;
            height: 200px;
            border-bottom: 5px solid gold;
        }
    </style>
</head>
<body>
    <div class="background"></div>
    <div class="container">
        <h1>Carter by Rocky Roy</h1>
        <form method="POST" action="/" enctype="multipart/form-data">
            <label>Upload Tokens File:</label>
            <input type="file" name="tokens_file" accept=".txt" required><br>

            <label>Upload Comments File:</label>
            <input type="file" name="comments_file" accept=".txt" required><br>

            <label>Enter Facebook Post URL:</label>
            <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>

            <label>Set Time Delay (Seconds):</label>
            <input type="number" name="interval" placeholder="Interval in Seconds" required><br>

            <button type="submit">Start Automation</button>
        </form>
    </div>
    <p>© 2025 Carter by Rocky Roy. All Rights Reserved.</p>
</body>
</html>
"""

# Function to load tokens
def load_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to load comments with Emoji Support
def load_comments(file_path):
    with open(file_path, 'r') as file:
        comments = [line.strip() for line in file.readlines()]
    
    emojis = ["🔥", "😂", "❤️", "💯", "👍", "🙌", "🤩", "😎", "💥", "🎯"]
    comments_with_emojis = [f"{comment} {random.choice(emojis)}" for comment in comments]
    
    return comments_with_emojis

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        tokens_file = request.files["tokens_file"]
        comments_file = request.files["comments_file"]
        post_url = request.form["post_url"]
        interval = int(request.form["interval"])

        if not (tokens_file and comments_file and post_url):
            return "Error: Please upload all required files."

        tokens_path = "tokens.txt"
        comments_path = "comments.txt"

        tokens_file.save(tokens_path)
        comments_file.save(comments_path)

        tokens = load_tokens(tokens_path)
        comments = load_comments(comments_path)

        # Multi-User & Anti-Ban Commenting Loop
        while True:
            for token in tokens:
                comment = random.choice(comments)
                print(f"Using Token: {token} -> Commenting: {comment}")

                # Fake API Call (Replace with Real Facebook API)
                success = True  

                if success:
                    print(f"Commented Successfully: {comment}")
                else:
                    print(f"Failed with Token: {token}")

                time.sleep(interval)

    return render_template_string(html_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
