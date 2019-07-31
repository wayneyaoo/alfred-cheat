#!/usr/bin/python
from sys import exit
from workflow import Workflow3 as Workflow
from lib.parser import Parser
from lib.options import Options

def main(workflow):
    query="" if len(workflow.args)==0 else workflow.args[0]

    config=workflow.stored_data("configuration")
    if config==None:
        Options.warning("Didn't find your configuration", "Please supply your cheat sheet path using 'cf ~/your/path'", workflow)
        workflow.send_feedback()
        return -1

    parser=Parser(config.getPath())
    options=Options(parser, workflow)

    tokens=query.strip().split(" ",1)
    tokens=[i.strip() for i in tokens if i!=""]

    if len(tokens)<2:
        sheetName="" if len(tokens)==0 else tokens[0]
        if sheetName=="--search":
            Options.hint("Globally searching for ...?", "In global mode", workflow)
        handler=options.showAvailable if sheetName not in parser.availableSheets() else options.list
        handler(sheetName)
    else:
        sheetName=tokens[0]
        searchTerm=tokens[1]
        if sheetName=="--search":
            options.search( None, searchTerm)
        else:
            options.search( sheetName, searchTerm)

    workflow.send_feedback()
    return None

if __name__=="__main__":
    workflow=Workflow()
    exit(workflow.run(main))
