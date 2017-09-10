# -*- coding: utf-8 -*-
from lxml import etree
from copy import deepcopy

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

def empty_if_none(text):
    if text == None:
        return ''
    else:
        return text

def store_header(table):
    store = []
    for count, row in enumerate(table.iter('tr')):
        if count < 2:
            store.append([])
            for cell in row.iter('td'):
                store[count].append(empty_if_none(cell.text))
                cell.getparent().remove(cell)
            row.getparent().remove(row)
    print('%d x %d' % (len(store),len(store[0])))
    return store

def rearrange_header(table,store,switch):
    header = etree.SubElement(table,'thead')
    row1 = etree.SubElement(header,'tr')
    for j, text in enumerate(store[1]):
        current = etree.SubElement(row1,'th')
        if switch[0] <= j and j <= switch[1]:
            current.text = store[0][j]
        else: 
            current.text = text
    row2 = etree.SubElement(header,'tr')
    for j, text in enumerate(store[0]):
        current = etree.SubElement(row2,'th')
        if switch[0] <= j and j <= switch[1]:
            current.text = store[1][j]
        else: 
            current.text = text
    return header

def process_header(header,merge={},delete={},no_rowspan={}):
    classnames = []
    to_remove = []
    row1 = header.findall('tr')[0]
    for i, cell in enumerate(row1.iter('th')):
        if len(to_remove):
            cell.getparent().remove(cell)
            to_remove.pop()
            text = 'col-%d' % i
            classnames.append(text)
            cell.attrib['class'] = text
        else:
            if cell.text != '':
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
    row2 = header.findall('tr')[1]
    for cell in row2.iter('th'):
        if cell.text == '':
            cell.getparent().remove(cell)
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
    body = table.findall('./tr')
    for i, row in enumerate(body):
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
        '< 10': 'lt10',
        '11-20':'11-20',
        '21-30':'21-30',
        '31-40':'31-40',
        '41-50':'41-50',
        '51-60':'51-60',
        '61-70':'61-70',
        '71-80':'71-80',
        '81-90':'81-90',
        '91-100':'91-100',
        '100+':'gt100'
        }
special_classnames = {
        'microphone': mic_case,
        'ping'      : ping_case
        }
merge_cols = {
        'tagpro-username':'2',
        'location':'2',
        'ping':'2',
        }
no_rowspan = {
        'ping',
        }

# Read table and add class attributes
dptable = etree.parse('dptable.html')
header = rearrange_header(dptable.getroot(),store_header(dptable),(9,10))
classnames = process_header(header,merge_cols,{},no_rowspan)
add_classes_to_table(dptable,classnames,special_classnames)

# Insert table into main document
parser = etree.HTMLParser()
doc = etree.parse('outline.html', parser)
body = doc.xpath("//body/div[@id='table-container']")[0]
body.append(dptable.getroot())
doc.write('draft-packet.html', pretty_print = True, method = 'html', encoding = 'utf-8')
