<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #2c3338;
            color: white;
            text-align: center;
            padding: 20px;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 30px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
            margin: 5px;
            background-color: #333;
            border: 1px solid #444;
            color: white;
        }
        button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .error {
            color: #ff4444;
            margin: 10px 0;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #333;
            border-radius: 5px;
        }
        .result a {
            color: #4CAF50;
            text-decoration: none;
        }
        .result a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>URL Shortener</h1>
        
        <form method="POST">
            <input type="text" name="url" placeholder="Enter a long URL" required>
            <input type="text" name="custom_code" placeholder="Custom short code (optional)">
            <button type="submit">Shorten</button>
        </form>

        {% if error %}
        <div class="error">
            {{ error }}
        </div>
        {% endif %}

        {% if short_url %}
        <div class="result">
            <p>Your shortened URL:</p>
            <a href="{{ short_url }}" target="_blank">{{ short_url }}</a>
        </div>
        {% endif %}
    </div>
</body>
</html>