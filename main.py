import os
from app import create_app
from flask import jsonify
from dotenv import load_dotenv

app = create_app()

#default route
@app.route("/")
def home():
    return jsonify({ "message": "Welcome to travel API" })

if __name__ == "__main__":
    
    load_dotenv()
    
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(rule)
    
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port)