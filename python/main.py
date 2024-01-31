"""
2024-01-30
John Robinson

A Google cloud functions code that will build a speed trace simulation based on input parameters.


To test locally:

    /JR-SRUSA.github.io/python> functions-framework --target=http_accel_graph --source=main.py --port=8123
    OR
    /JR-SRUSA.github.io/python> functions-framework --target=http_accel_sol --source=main.py --port=8123

Then go to:

    http://127.0.0.1:8123/accel-graph?power_kw=200&mass_kg=200&cda_m2=0.25

To deploy from the console:

    > gcloud functions deploy accel-graph --gen2 --runtime=python312 --region=us-central1 --source=. --entry-point=http_accel_graph --trigger-http --allow-unauthenticated
    OR
    > gcloud functions deploy accel-sol --gen2 --runtime=python312 --region=us-central1 --source=. --entry-point=http_accel_sol --trigger-http --allow-unauthenticated

"""
import flask
import functions_framework
import json

import tp_spd_sim


EXAMPLE_SPEED_URL = "Ex: https:url/accel-graph?power_kw=200&mass_kg=200&cda_m2=0.25"
EXAMPLE_SPEED_ARGS = "?power_kw=200&mass_kg=200&cda_m2=0.25"


@functions_framework.http
def http_accel_sol(request: flask.Request) -> json:
    """
    HTTP GCloud Function.

    Can be requested from the Github pages site (CORS headers included)
    """
    print(request.url_root)
    if request.url_root == 'http://localhost:8123/':
        # Default to "debug from localhost" mode if the request comes from localhost:8123
        headers = {"Access-Control-Allow-Origin": "http://localhost:8000"}
    else:
        headers = {"Access-Control-Allow-Origin": "https://jr-srusa.github.io"}

    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        # headers = {
        #     "Access-Control-Allow-Origin": "https://jr-srusa.github.io",
        #     "Access-Control-Allow-Methods": "GET",
        #     "Access-Control-Allow-Headers": "Content-Type",
        #     "Access-Control-Max-Age": "3600",
        # }
        headers["Access-Control-Allow-Methods"] = "GET"
        headers["Access-Control-Allow-Headers"] = "Content-Type"
        headers["Access-Control-Max-Age"] = "3600"

        return ("", 204, headers)

    request_args = request.args

    request_arg_keys = ["power_kw", "cda_m2", "mass_kg"]
    accel_params = {}

    for arg_key in request_arg_keys:
        if request_args and arg_key in request_args:
            try:
                accel_params[arg_key] = float(request_args[arg_key])
            except ValueError:
                example_url = request.base_url + 'accel-sol/' + EXAMPLE_SPEED_ARGS
                return f"All input parameters must be able to be read as a number. <br><br><a href='{example_url}'>{example_url}</a>"
        else:
            example_url = request.base_url + 'accel-sol/' + EXAMPLE_SPEED_ARGS
            return f"All input parameters must be able to be read as a number. <br><br><a href='{example_url}'>{example_url}</a>"

    sol = tp_spd_sim.solve_accel(accel_params)
    json_response = flask.jsonify({
        'time_s': list(sol.t),
        'velocity_ms': list(sol.y[1]),
    })

    return (json_response, 200, headers)


@functions_framework.http
def http_accel_graph(request: flask.Request) -> str:
    """HTTP Cloud Function.

    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_args = request.args

    request_arg_keys = ["power_kw", "cda_m2", "mass_kg"]
    accel_params = {}

    for arg_key in request_arg_keys:
        if request_args and arg_key in request_args:
            try:
                accel_params[arg_key] = float(request_args[arg_key])
            except ValueError:
                example_url = request.base_url + 'accel-graph/' + EXAMPLE_SPEED_ARGS
                return f"All input parameters must be able to be read as a number. <br><br><a href='{example_url}'>{example_url}</a>"
        else:
            example_url = request.base_url + 'accel-graph/' + EXAMPLE_SPEED_ARGS
            return f"All input parameters must be able to be read as a number. <br><br><a href='{example_url}'>{example_url}</a>"

    graph = tp_spd_sim.accel_graph(accel_params)

    return graph

