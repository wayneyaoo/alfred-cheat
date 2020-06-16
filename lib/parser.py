#!/usr/bin/python
import os, re
from workflow import MATCH_ALL, MATCH_ALLCHARS

class Parser:
    def __init__(self,path):
        self._path=path
        self._sheetMapping={} # {cheatsheet: /home/somedir/cheatsheet}
        self._available=self._enumAvailableSheets()
        return None

    def availableSheets(self):
        'Access to the private variable _available'
        return self._available

    def _enumAvailableSheets(self):
        'Fills the _available and _sheetMapping variables with names and {name: path} set at initiation'
        ret=[]
        for root, dirname, files in os.walk(self._path,followlinks=True):
            dirname[:]=[d for d in dirname if not d.startswith(".")]
            files=[f for f in files if not f.startswith(".")]
            ret.extend(files)
            # update the cheat sheet mapping so that we can find the file location
            self._sheetMapping.update({cheatsheet: "".join([root,"/",cheatsheet]) for cheatsheet in files})
        return ret


    def list(self, sheetName):
        'Returns all the entries of cheatsheet "sheetName" whenever possible'
        return [] if sheetName not in self._available else self.__parseSheet(sheetName) # return value: [{}, {}, {}, ...]

    def searchInSheet(self, keyword, sheetName, workflow):
        'Searches keyword inside the cheatsheet "sheetname"'
        return self.filter(self.__parseSheet(sheetName), keyword, workflow)

    def searchAcrossAll(self, keyword, workflow):
        'Searches keyword inside all available cheatsheets (--search option)'
        ret=[]
        for sheet in self._available:
            ret.extend(self.__parseSheet(sheet,specify_sheet=True))
        return self.filter(ret, keyword, workflow) # [{}, {}, {}...]

    def __parseSheet(self, filename, specify_sheet=False):
        'Private method to parse the file'
        with open(self._sheetMapping.get(filename), 'r') as f:
            content=f.read().decode('utf-8',"replace").strip("\n")
        # Tokenize to get each "item" by spliting the "\n\n" (possibly with white space characters).
        # This rule must be respected
        content=re.split("\n\s*\n",content)
        content=[item.strip() for item in content]
        items=[]
# Adds title
        if content[0][0:2]=="!!":
            command=content.pop(0)[2:50].strip()
        else:
            command=os.path.basename(filename)
        type="title"
        comment=""
        items.append((type,comment, command))
# Adds contents        
        for item in content:
            if item[0:2]=="/*":
#               type="invisible"
                command=""
            elif item[0:2]=="//":
                type="section"
                command=item[2:80].strip()
                comment=""                
            else:
                type="entry"
                lines=item.split("\n")
                comment_list=[line[1:] for line in lines if line.startswith('#')]
                command_list=[line for line in lines if not line.startswith('#')]
                comment=", ".join(comment_list)
                command=u"  \u28B8  ".join(command_list)
            if command !="": items.append((type,comment, command))
        if specify_sheet:
            return [dict(comment=comment, command=command, type=type, sheet=filename) for type,comment,command in items] 
            # [{comment/command/type}, {}, {}...]
        else: 
            return [dict(comment=comment, command=command, type=type) for type,comment,command in items] 
            # [{comment/command/type}, {}, {}...]

    def filter(self, content, keyword, workflow):
        'Filter for the "searchInSheet" method'
        def searchIndex(item):
            return u" ".join([item["comment"],item["command"]])
        return workflow.filter(keyword, content,key=searchIndex, match_on=MATCH_ALL ^ MATCH_ALLCHARS, min_score=50)
