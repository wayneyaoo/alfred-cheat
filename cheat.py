#!/usr/bin/python
from sys import exit
from workflow import Workflow3 as Workflow
from lib.parser import Parser
from lib.options import Options


def main(workflow):
    # Try to read configuration from local disk
    config = workflow.stored_data("configuration")
    if config is None:
        Options.warning("Didn't find your configuration", "Please supply your cheat sheet path using 'cf ~/your/path'", workflow)
        workflow.send_feedback()
        return -1

    parser = Parser(config.getPath())
    # Note: by pasing workflow as a variable, its state is changed in Options.py logic
    options = Options(parser, workflow)

    # Query is whatever comes after "cheat". Stored in one single variable
    query = "" if len(workflow.args) == 0 else workflow.args[0]
    tokens = query.strip().split(" ", 1)  # len 2 list
    tokens = [i.strip() for i in tokens if i != ""]

    if len(tokens) == 0:
        options.showAvailable()
        workflow.send_feedback()
        return None

    if len(tokens) == 1 and tokens[0] in ("--search", "-s"):
        Options.hint("Globally searching for ...?", "In global mode", workflow)
        workflow.send_feedback()
        return None

    if len(tokens) == 1 and tokens[0] not in parser.availableSheets():
        options.showAvailable(tokens[0])
        workflow.send_feedback()
        return None

    if len(tokens) == 1:
        options.list(tokens[0])
        workflow.send_feedback()
        return None

    sheetName = None if tokens[0] in ["--search", "-s"] else tokens[0]
    searchTerm = tokens[1]
    options.searchInSheetByKeyword(sheetName, searchTerm)

    workflow.send_feedback()
    return None


if __name__ == "__main__":
    workflow = Workflow()
    exit(workflow.run(main))
