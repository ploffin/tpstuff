# -*- coding: utf-8 -*-
from lxml import etree

# Remove uppercase and whitespace
def sanitize(text):
    return unicode(text.lower(),'utf-8').translate({ord(' '): u'-'})

# Get classnames to be added to respective columns
# of each header cells, and add class attributes
# to the header cells
def process_header(table):
    header = table.find('.//thead')
    classnames = []
    for i, cell in enumerate(header.iter('th')):
        if cell.text != None:
            text = sanitize(cell.text)
        else:
            text = 'col-%d' % i
        classnames.append(text)
        cell.attrib['class'] = text
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
        if i != 0 and i != 1:
            cells = row.findall('td')
            for j, cell in enumerate(cells):
                classname = classnames[j]
                add_class_to_element(classname,cell,special_classnames)
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

# Read table and add class attributes
dptable = etree.parse('dptable.html')
classnames = process_header(dptable)
add_classes_to_table(dptable,classnames,special_classnames)

# Insert table into main document
parser = etree.HTMLParser()
doc = etree.parse('outline.html', parser)
body = doc.find('.//body')
body.append(dptable.getroot())
doc.write('draft-packet.html', pretty_print = True, method = 'html', encoding = 'utf-8')
