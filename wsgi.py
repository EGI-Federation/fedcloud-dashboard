from flask import Flask
from update_endpoints import update_endpoints

app = Flask(__name__)

@app.route("/")
def main():
    #return "<p>Hello, World!</p>"
    endpoints = read_endpoints()
    answer = ""
    for site, endpoint in endpoints:
        #print(endpoint)
        #answer = answer + f"<p>{endpoint}</p>"
        answer = answer + f"<p>Site:{site}: <a href=\"{endpoint}\">{endpoint}</a></p>"

    return answer

if __name__ == "__main__":
    main()
