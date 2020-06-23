import sys,os,workflow

def html_header():
    filename=os.getcwd() + "/my_style.css"
    file=open(filename,'r')
    style=file.read()
    file.close() 
    return "<!DOCTYPE html>\n<html>\n<body>\n<head>\n<style>\n"\
            + style + "</style>\n</head>\n\n<table>\n\n"

def html_footer():
    return "</table>\n</html>\n</body>\n"

def html_title(title):
    return "<tr><td class=\"title_cell\">" + title + "</td><td class=\"title_cell\"> &nbsp; </td></tr></table><table>\n"

def html_line(entry, position):
    if position==0:
         part="<tr><td class=\"column1\">" + entry + "</td>\n"
         return part
    else: 
         part="<td class=\"column2\">" + entry + "</td></tr>\n"
         return part

def html_section(entry, actual_position):
    # Fills the last column if needed 
    if actual_position==1:
         part="<td class=\"column2\">&nbsp;</td></tr>\n"
    else: 
        part=""
    # Adds the section title
    part += "<tr><td class=\"column1\"><div class=\"section\">"\
         + entry + "</div></td><td class=\"column2\"> &nbsp; </td></tr>\n"
    return part
    
def standard_entry(command,comment,position):
    comment_html=comment.encode('ascii','xmlcharrefreplace').decode('utf-8')
    command_html=command.encode('ascii','xmlcharrefreplace').decode('utf-8')
    return html_line("<div class=\"comment\">"+comment_html \
                                    +"</div>\n<div class=\"command\">"+command_html+"</div>",position)
    
def create_html(entries):
    html_page_list=[]
# Write title
    line=entries.pop(0)
    type=line.get("type")
    if type=="title":
        html_page_list.append(html_title(line.get("command")))
# Begin to write the lines
    col=0 # 0 = left column / 1 = right column
    for entry in entries:
        if entry['type'] == 'section':
            line=entry['command']
            line=line.encode('ascii','xmlcharrefreplace').decode('utf-8')
            html_page_list.append(html_section(line, col))
            col=0
        elif entry['type'] == 'entry':
            html_page_list.append(standard_entry(entry['command'],entry['comment'],col))
            col=1-col
        else:
            pass
# Fills the last column in the last row if needed
    if col==1:
        html_page_list.append(html_line("",1))
# Finally write the html page
    html_page= html_header() + "\n".join(html_page_list) + html_footer()
    return html_page


def create_html_global_search(entries,keyword,sheetName):
    html_page_list=[]
# Write title
    if sheetName==None:
        html_page_list.append(html_title("Global search term: " + keyword))
    else:
        html_page_list.append(html_title("Local search of term \'" + keyword +"\' in \'"+ sheetName + "\'"))
# Begin to write the lines
    col=0
    for entry in entries:
        if entry['type']=='entry':
            if sheetName==None:
                sheet="["+entry.get('sheet')+"]  "
            else:
                sheet=""
            html_page_list.append(standard_entry(entry['command'],sheet+entry['comment'],col))
            col=1-col
# Fills the last column in the last row if needed
    if col==1:
        html_page_list.append(html_line("",1))
# Finally write the html page
    html_page= html_header() + "\n".join(html_page_list) + html_footer()
    return html_page

