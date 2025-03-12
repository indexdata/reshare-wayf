import json
from flask import Flask, request, redirect, make_response, render_template

app = Flask(__name__)

# Load TARGET_HOSTS from a JSON file
with open("config/target_hosts.json", "r") as file:
    TARGET_HOSTS = json.load(file)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=["GET", "POST"])
def handle_request(path):
    if 'reshareInst' not in request.cookies:
        if request.method == "POST" and "inst" in request.form:
            response = make_response(redirect(f"/{path}"))  # Redirect back to requested path
            response.set_cookie("reshareInst", request.form["inst"], max_age=3600)
            return response
        return render_template('wayf.html', target_hosts=TARGET_HOSTS)

    inst = request.cookies.get("reshareInst")
    target = TARGET_HOSTS.get(inst, {})
    target_host = target.get("host", "https://default.com")
    url = f"{target_host}/{path}"

    return redirect(url, code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
