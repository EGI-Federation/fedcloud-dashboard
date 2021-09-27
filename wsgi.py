from flask import Flask
from find_endpoints import find_endpoint

app = Flask(__name__)

@app.route("/")
def main():
    #return "<p>Hello, World!</p>"
    endpoints = find_endpoint("org.openstack.horizon")
    answer = ""
    for site, service_type, endpoint in endpoints:
        #print(endpoint)
        #answer = answer + f"<p>{endpoint}</p>"
        answer = answer + f"<p><a href=\"{endpoint}\">{endpoint}</a></p>"

    return answer

if __name__ == "__main__":
    main()
