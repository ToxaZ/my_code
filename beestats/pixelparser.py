__author__ = 'ffuuugor'
import sys
import logging
import json
import re
import urllib

logging.basicConfig(filename='pixelparser.log', level=logging.DEBUG)


def parse(infile, outfile):
    fin = open(infile, "r")

    user_to_landing = {}
    lines = []

    for line in fin:
        ts = line.split(" ")[0].split(".")[0]

        ip = line.split(" ")[1]

        if ip.startswith("46.250."):
            continue
        if int(ts) < 1423356174:
            continue

        params_line = "?".join(line.split(" ")[2].split("?")[1:])
        params = {}
        for tuple in params_line.split("&"):
            if "=" in tuple:
                key = tuple.split("=")[0]
                val = tuple.split("=")[1].split("?")[0]

                params[key] = re.sub("[^0-9a-zA-Z/\.]", "", urllib.unquote(val))

        if params.get("name") == "Submitted":
            print params["number"], params["location"]
        if "user_cookie" in params and "landingType" in params:
            user_to_landing[params["user_cookie"]] = params["landingType"]

        params["time"] = ts
        params["ip"] = ip

        if "" in params:
            del params[""]

        lines.append(params)

    for line in lines:
        if "landingType" not in line:
            if "user_cookie" not in line:
                logging.error("Unexpected line: %s", json.dumps(line))
                continue

            user = line["user_cookie"]

            if user not in user_to_landing:
                logging.error("Unexpected user %s" % user)
                continue

            landing_type = user_to_landing[user]
            line["landingType"] = landing_type

    json_lines = [json.dumps(line) for line in lines]

    open(outfile, 'w').write("[%s]" % ",\n".join(json_lines))


if __name__ == "__main__":
    parse("nginx-pixel.log", "landing_events.json")
    # parse(sys.argv[1], sys.argv[2])
