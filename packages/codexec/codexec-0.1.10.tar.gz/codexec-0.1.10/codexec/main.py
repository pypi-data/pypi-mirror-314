import argparse
import requests
import os
import itertools
import sys


def readfile(filepath):
    try:
        file = open(filepath, "r")
        return file.read()
    except Exception as e:
        print(e)


def getlangcode(filepath):
    langcode = -1
    _, ext = os.path.splitext(filepath)
    if ext[1:] == "c":
        langcode = 50
    elif ext[1:] == "cpp":
        langcode = 76
    elif ext[1:] == "java":
        langcode = 62
    elif ext[1:] == "py":
        langcode = 71
    elif ext[1:] == "js":
        langcode = 63
    return langcode


def execode(url, code, input, langcode):
    payload = {"languageCode": langcode, "input": input, "code": code}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)


def main():
    parser = argparse.ArgumentParser(
        prog="codexec",
        description="compiles and executes code files written in c, cpp, java, python and javascript",
    )
    parser.add_argument("codefile", help="path to code file(.c, .cpp, .java, .py, .js)")
    parser.add_argument("-i", "--inputfile", help="path to input file(.txt)")

    args = parser.parse_args()

    codefile = args.codefile
    inputfile = args.inputfile
    code = ""
    input = ""
    output = ""

    url = "https://code-engine.codehelp.in/api/v1/quick-compiler/run"

    code = readfile(codefile)
    langcode = getlangcode(codefile)
    if langcode < 0:
        sys.exit("code provided is irrelevant")
    if inputfile:
        input = readfile(args.inputfile)

    response = execode(url, code, input, langcode)
    if isinstance(response, dict) and "data" in response:
        output = response["data"].get("stdout", "no output available")
        if output == None:
            output = response["data"].get("compile_output", "no output available")

    print(output)


if __name__ == "__main__":
    main()
