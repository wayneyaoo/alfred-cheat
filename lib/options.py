#!/usr/bin/python
from workflow.workflow import ICON_HELP as WARNINGICON
from workflow.workflow import ICON_NOTE as HINT

# Switches that autually controls the workflow behavior
class Options:
    def __init__(self, parser, workflow):
        self._parser=parser
        self._workflow=workflow
        return None

    def search(self, sheetName, keyword):
        if sheetName==None:
            ret=self._parser.searchAcrossAll(keyword, self._workflow)
        else:
            if sheetName not in self._parser.availableSheets():
                Options.warning("Cheat sheet not found.","", self._workflow)
                return None
            ret=self._parser.searchInSheet(keyword, sheetName, self._workflow)
        if ret==[]:
            Options.warning("Not found", "No match found for search {}".format(keyword), self._workflow)
            return None
        for item in ret:
            self._workflow.add_item(
                    title=item["command"],
                    subtitle=item["comment"],
                    copytext=item.get("command"),
                    valid=True,
                    arg=item.get("command")
                    )
        return None

    def list(self, sheetName):
        ret=self._parser.list(sheetName)
        if ret==[]:
            Options.hint("Empty cheatsheet", "", self._workflow)
        for item in ret:
            self._workflow.add_item(
                    title=item.get("command"),
                    subtitle=item.get("comment"),
                    valid=True,
                    copytext=item.get("command"),
                    arg=item.get("command")
                    )
        return None

    def showAvailable(self, sheetName):
        names=self._parser.availableSheets()
        ret=self._workflow.filter(sheetName, names, key=lambda x: x)
        if ret==[]:
            Options.warning("Cheat sheet not found.","", self._workflow)
            return None
        for sheet in ret:
            self._workflow.add_item(
                    title=sheet,
                    autocomplete=sheet,
                    )
        return None

    @staticmethod
    def warning(msg,subtitle,workflow):
        workflow.warn_empty(
                title=msg,
                subtitle=subtitle,
                icon=WARNINGICON,
                )
        return None

    @staticmethod
    def hint(msg, subtitle, workflow):
        workflow.warn_empty(
                title=msg,
                subtitle=subtitle,
                icon=HINT,
                )
        return None
