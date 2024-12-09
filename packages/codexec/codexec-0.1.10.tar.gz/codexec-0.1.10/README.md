# codexec

codexec is a Python package that allows you to execute code written in various programming languages (C, C++, Java, Python, and JavaScript) by making API calls to a server. The package takes code files and optional input files, executes the code, and returns the output.

## Features

- Execute code in multiple languages: C, C++, Java, Python, and JavaScript.
- Simple command-line interface (CLI) for executing code files.
- Supports optional input files for code that requires input.

## Usage

1. **Install the package**:

   You can install the `codexec` package using `pip`:

   ```bash
   pip install codexec
   ```

2. **Basic Usage**:

   You can run the `codexec` command in your terminal to execute code files.

   Example of executing a Python file:

   ```bash
   codexec path/to/your/code.py
   ```

3. **With Input File**:

   If your code requires input, you can specify an input file:

   ```bash
   codexec path/to/your/code.py -i path/to/input.txt
   ```

4. **Supported Languages**:

   - `C` (.c)
   - `C++` (.cpp)
   - `Java` (.java)
   - `Python` (.py)
   - `JavaScript` (.js)

## How it works?

Uses [codehelp.in](https://www.codehelp.in/quick-compiler) API under the hood.

> [credits](https://github.com/thepranaygupta/codehelp-compiler)
