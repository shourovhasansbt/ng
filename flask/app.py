from flask import Flask, request, render_template_string
import requests
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Response</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f9f9f9;
        }
        h1 {
            color: #333;
        }
        pre {
            background-color: #e8e8e8;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 14px;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>API Response</h1>
    {% if error %}
        <p class="error">{{ error }}</p>
    {% else %}
        <pre>{{ response }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        phone_number = request.form.get("phone_number")
        
        url = "https://app2.mynagad.com:20002/api/user/check-user-status-for-log-in"
        params = {'msisdn': phone_number}
        headers = {
            'X-KM-User-AspId': '100012345612345',
            'X-KM-User-Agent': 'ANDROID/1164',
            'X-KM-DEVICE-FGP': '5AB18952A962A31MM9A89524F6282F78905DDE9F94656B5C1CFCEDNN74AE660E',
            'X-KM-Accept-language': 'bn',
            'X-KM-AppCode': '01',
            'Host': 'app2.mynagad.com:20002',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.14.9'
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                json_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
                return render_template_string(HTML_TEMPLATE, response=json_response, error=None)
            else:
                error_message = f"Error: {response.status_code}, {response.text}"
                return render_template_string(HTML_TEMPLATE, response=None, error=error_message)
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, response=None, error=str(e))
    
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Nagad API Checker</title>
        </head>
        <body>
            <h1>Enter Phone Number</h1>
            <form method="post">
                <input type="text" name="phone_number" placeholder="Enter phone number" required>
                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
