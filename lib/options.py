#!/usr/bin/python
from workflow.workflow import ICON_HELP as WARNINGICON
from workflow.workflow import ICON_NOTE as HINT

# Switches that actually controls the workflow behavior
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
            it=self._workflow.add_item(
                    title=item["command"],
                    subtitle=item["comment"],
                    largetext=item.get("comment")+"\n"+item.get("command"),
                    copytext=item.get("command"),
                    valid=True,
                    arg=item.get("command")
                    )
            it.add_modifier(
                    'cmd',  # or 'ctrl'?
                    subtitle='Open the "%s" cheat file in editor' % sheetName,
                    valid=True,
                    arg= self._parser._sheetMapping.get(sheetName),
                    )
        return None

    def list(self, sheetName):
        ret=self._parser.list(sheetName)
        if ret==[]:
            Options.hint("Empty cheatsheet", "", self._workflow)
        for item in ret:
            it=self._workflow.add_item(
                    title=item.get("command"),
                    subtitle=item.get("comment"),
                    largetext=item.get("comment")+"\n"+item.get("command"),
                    valid=True,
                    copytext=item.get("command"),
                    arg=item.get("command")
                    )
            it.add_modifier('cmd',  
                    subtitle='Open the "%s" cheat file in editor' % sheetName,
                    valid=True,
                    arg= self._parser._sheetMapping.get(sheetName),
                    )
        return None

    def showAvailable(self, sheetName):
        names=self._parser.availableSheets()
        ret=self._workflow.filter(sheetName, names, key=lambda x: x)
        if ret==[]:
            if "--search".find(sheetName)==-1:
                Options.warning("Cheat sheet not found.","", self._workflow)
            elif "--search" != sheetName:
                self._workflow.add_item(title="--search",
                                        subtitle="Searching in global mode",
                                        autocomplete="--search " )
            return None
        for sheet in ret:
            it=self._workflow.add_item(
                    title=sheet,
                    autocomplete=sheet,
                    )
            it.add_modifier('cmd',  
                    subtitle='Open the "%s" cheat file in editor' % sheet,
                    valid=True,
                    arg= self._parser._sheetMapping.get(sheet),
                    )
        self._workflow.add_item(
                title="--search",
                subtitle="Searching in global mode",
                autocomplete="--search ",
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
