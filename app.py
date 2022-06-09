from typing import Dict
from flask import Flask, render_template, request, url_for, jsonify
from sdf_wot_converter import (
    convert_sdf_to_wot_td,
    convert_sdf_to_wot_tm,
    convert_wot_td_to_sdf,
    convert_wot_td_to_wot_tm,
    convert_wot_tm_to_sdf,
    convert_wot_tm_to_wot_td,
)
import json

app = Flask(__name__)


@app.route("/convert/<command>", methods=["POST"])
def convert(command):
    if request.is_json:
        input = request.json

        return jsonify(_use_command(command, input))


@app.route("/", methods=["GET", "POST"])
def index():
    url_for("static", filename="chota.min.css")
    input1 = None
    input2 = None
    input1_type = None
    input2_type = None
    error = None
    if request.method == "POST":
        input1_type, input2_type = _get_input_types(request)
        input1, input2 = _load_inputs(request)

        try:
            input1, input2 = _process_inputs(request)

        except Exception as e:
            error = e

    return render_template(
        "index.html",
        input1=input1,
        input2=input2,
        input1_type=input1_type,
        input2_type=input2_type,
        error=error,
    )


def _process_inputs(request):
    input = _load_input(request)
    command = _get_command(request)

    if command is None:
        raise Exception("Unknown command")

    output = _use_command(command, input)
    return _dump_output(request, output)


def _use_command(command: str, input: Dict):
    input, sdf_mapping_files = _get_sdf_input(command, input)

    if command == "sdf-to-tm":
        output = convert_sdf_to_wot_tm(input, sdf_mapping_files=sdf_mapping_files)
    elif command == "sdf-to-td":
        output = convert_sdf_to_wot_td(input, sdf_mapping_files=sdf_mapping_files)
    elif command == "tm-to-sdf":
        output = convert_wot_tm_to_sdf(input)
    elif command == "tm-to-td":
        output = convert_wot_tm_to_wot_td(input)
    elif command == "td-to-sdf":
        output = convert_wot_td_to_sdf(input)
    elif command == "td-to-tm":
        output = convert_wot_td_to_wot_tm(input)
    else:
        output = input

    return output


def _get_sdf_input(command: str, input):
    sdf_mapping_files = None

    if command.startswith("sdf-to-") and isinstance(input, list):
        if len(input) > 1:
            sdf_mapping_files = input[1:]
        input = input[0]

    return input, sdf_mapping_files


def _load_input(request):
    input1, input2 = _load_inputs(request)

    if _is_left_to_right_conversion(request):
        input = input1
    else:
        input = input2

    return json.loads(input)


def _dump_output(request, output):
    indent = 2

    input1, input2 = _load_inputs(request)
    serialized_output = json.dumps(output, indent=indent)

    if _is_left_to_right_conversion(request):
        return input1, serialized_output
    else:
        return serialized_output, input2


def _is_left_to_right_conversion(request):
    return request.form.get("submit_input1") is not None


def _get_command(request):
    input_type_1, input_type_2 = _get_input_types(request)

    if not _is_left_to_right_conversion(request):
        input_type_1, input_type_2 = input_type_2, input_type_1

    return f"{input_type_1}-to-{input_type_2}"


def _get_input_types(request):
    return request.form["input1_type"], request.form["input2_type"]


def _load_inputs(request):
    return request.form["input1"], request.form["input2"]


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error/404.html", error=error, code=404), 404
