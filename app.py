from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from converter import convert_sdf_to_wot_tm_from_json
from converter import convert_wot_tm_to_sdf_from_json

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    url_for("static", filename="chota.min.css")
    if request.method == "POST":
        # TODO: Refactor
        input1_type = request.form["input1_type"]
        input2_type = request.form["input2_type"]
        input1 = request.form["input1"]
        input2 = request.form["input2"]

        if request.form.get("submit_input2"):
            direction = "left"
        else:
            direction = "right"

        try:
            if input1_type == "SDF":
                if input2_type == "WoT TM":
                    if direction == "right":
                        input2 = convert_sdf_to_wot_tm_from_json(input1)
                    else:
                        input1 = convert_wot_tm_to_sdf_from_json(input2)
                elif input2_type == "SDF":
                    if direction == "right":
                        input2 = input1
                    else:
                        input1 = input2
            elif input1_type == "WoT TM":
                if input2_type == "SDF":
                    if direction == "right":
                        input2 = convert_wot_tm_to_sdf_from_json(input1)
                    else:
                        input1 = convert_sdf_to_wot_tm_from_json(input2)
                elif input2_type == "WoT TM":
                    if direction == "right":
                        input2 = input1
                    else:
                        input1 = input2
        except Exception as e:
            return render_template(
                "index.html",
                input1=input1,
                input2=input2,
                input1_type=input1_type,
                input2_type=input2_type,
                error=e,
            )

        return render_template(
            "index.html",
            input1=input1,
            input2=input2,
            input1_type=input1_type,
            input2_type=input2_type,
        )
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(error):
    print(error)
    return render_template("error/404.html", error=error, code=404), 404
