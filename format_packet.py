# -*- coding: utf-8 -*-
from lxml import etree

# Remove uppercase and whitespace
def sanitize(text):
    return unicode(text.lower(),'utf-8').translate({ord(' '): u'-'})

# Get classnames to be added to respective columns
# of each header cells, add class attributes and colspan
# where specified to the header cells. Since colspan
# creates new cells, we delete the corresponding
# number of cells to merge
#TODO scrap the whole thing - do in two passes,
# one to get info and another to create <thead>
def process_header(table,merge={},delete={},no_rowspan={}):
    classnames = []
    to_remove = []
    for i,cell in enumerate(table.iter('th')):
        if len(to_remove):
            cell.getparent().remove(cell)
            to_remove.pop()
            text = 'col-%d' % i
            classnames.append(text)
            cell.attrib['class'] = text
        else:
            if cell.text != None:
                text = sanitize(cell.text)
            else:
                text = 'col-%d' % i
            classnames.append(text)
            if text in delete:
                cell.getparent().remove(cell)
            else:
                cell.attrib['class'] = text
                if text not in no_rowspan:
                    cell.attrib['rowspan'] = '2'
                if text in merge:
                    colspan_val = merge[text]
                    to_remove = range(int(colspan_val)-1)
                    cell.attrib['colspan'] = colspan_val

    return classnames

# Add class attribute classname to element, admitting
# conditional formatting as defined in special_classnames
def add_class_to_element(classname,element,special_classnames={}):
    if special_classnames.has_key(classname):
        try:
            text = element.text.lower()
        except AttributeError:
            print('cell contains no text, won\'t add case')
            element.attrib['class'] = classname
            return
        cases = special_classnames[classname]
        if cases.has_key(text):
            element.attrib['class'] = '%s %s-%s' % (classname, classname, cases[text])
        else:
            print('no case %s in %s, won\'t add case' % (text, classname))
            element.attrib['class'] = classname
            return
    else:
        element.attrib['class'] = classname
    return

# Populate table body with class attributes
def add_classes_to_table(table,classnames,special_classnames={}):
    for i, row in enumerate(table.iter('tr')):
        cells = row.findall('td')
        if i != 0 and i != 1:
            for j, cell in enumerate(cells):
                classname = classnames[j]
                add_class_to_element(classname,cell,special_classnames)
        elif i == 1:
            for j, cell in enumerate(cells):
                classname = classnames[j]
                if cell.text != None:
                    add_class_to_element('%s %s' % (classname,sanitize(cell.text)),cell)
                else:
                    cell.getparent().remove(cell)
    return
            
# Define which content has special classes
mic_case = {
        'yes':'yes',
        'no' :'no'
        }
ping_case = {
        '<20' :'lt20'   ,
        '<40' :'lt40'   ,
        '<75' :'lt75'   ,
        '<100':'lt100',
        '>100':'gt100'
        }
special_classnames = {
        'microphone': mic_case,
        'ping'      : ping_case
        }
merge_cols = {
        'tagpro-name':'3',
        'location':'2',
        'ping':'2',
        }
no_rowspan = {
        'ping',
        }

# Read table and add class attributes
dptable = etree.parse('dptable.html')
classnames = process_header(dptable,merge_cols,{},no_rowspan)
add_classes_to_table(dptable,classnames,special_classnames)

# Insert table into main document
parser = etree.HTMLParser()
doc = etree.parse('outline.html', parser)
body = doc.xpath("//body/div[@id='table-container']")[0]
body.append(dptable.getroot())
doc.write('draft-packet.html', pretty_print = True, method = 'html', encoding = 'utf-8')
