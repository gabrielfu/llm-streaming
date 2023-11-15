import requests


def run(route, attr):
    print("======================================")
    print(f"route: {route}, resp.{attr}()")
    print("======================================")
    resp = requests.post("http://127.0.0.1:5001" + route, stream=True)
    for line in getattr(resp, attr)():
        if line:
            print(line)
            print("--------------------")


run("/stream", "iter_content")
run("/sse", "iter_lines")
