# -*- coding: utf-8 -*-
from lxml import etree 
import re
# Remove uppercase and whitespace
def sanitize(text):
    return unicode(text.lower(),'utf-8').translate({ord(' '): u'-'})

# Handle empty cells
def empty_if_none(text):
    if text == None:
        return ''
    else:
        return text

#############################################################################
# these use some constants but it will be fine unless the google packet     #
# magically gains a new header                                              #

# Store header values in array
def store_header(table):
    store = []
    for count, row in enumerate(table.iter('tr')):
        if count < 2:
            store.append([])
            for cell in row.iter('td'):
                store[count].append(empty_if_none(cell.text))
                cell.getparent().remove(cell)
            row.getparent().remove(row)
    return store

# Flip top and bottom header
# except for in between switch values
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

# Get classnames to be added to respective columns
# of each header cells, add class attributes and colspan
# where specified to the header cells. Since colspan
# creates new cells, we delete the corresponding
# number of cells to merge
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
        else:
            cell.attrib['class'] = sanitize(cell.text)
    return classnames
#                                                                           #
#############################################################################

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

# Get country flag and code from names
# and delete name column
# also uses constants 'col-8' and 'location'
def add_country_flags(table,uc_look_up,png_look_up={}):
    for ct in table.xpath("//td[@class='col-8']"):
        row = ct.getparent()
        text = ct.text
        cell = row.xpath("./td[@class='location']")[0]
        code = uc_look_up[ct.text][1]
        if text in uc_look_up:
            flag = uc_look_up[ct.text][0]
            cell.text = flag + code
        elif text in png_look_up:
            image = etree.SubElement(cell,'img')
            image.attrib['src'] = png_look_up[text]
            image.tail = code
        else:
            print('Country %s not added!' % text)
        ct.text = ''

# Get tagpro.gg ids and return as list of pairs
# uses constant names 'profile-id' and 'tagpro'
def get_profile_ids(data):
    rows = data.findall('tr')
    responses_classnames = []
    for cell in rows[0]:
        responses_classnames.append(sanitize(cell.text))
    add_classes_to_table(data,responses_classnames)
    body = data.findall('tr')
    name_id_pairs = {} 
    found_names = False
    found_ids = False
    for row in rows[1:]:
        cells = row.findall('td')
        for j, cell in enumerate(cells):
            if responses_classnames[j] == 'what-is-your-tagpro-username?':
                found_names = True
                name = cell.text
            if responses_classnames[j] == 'what-is-your-tagpro-profile-id?':
                found_ids = True
                tp_id = cell.text
        if name != None:
            name_id_pairs[name] = tp_id
    if not found_names:
        print('column for TP name not found (getting ids)')
    if not found_ids:
        print('column for TP id not found')
    return name_id_pairs

# Insert profile ids at and of main table
def add_profile_ids(table,classnames,id_data):
    body = table.findall('./tr')
    found_names = False
    for i, row in enumerate(body):
        cells = row.findall('td')
        for j, cell in enumerate(cells):
            if classnames[j] == 'tagpro-username':
                found_names = True
                name = re.match('(^.*?)\s*$',
                        cell.text.split('(')[0]).group(1)
                new = etree.SubElement(row,'td')
                new.text = id_data[name]
                new.attrib['class'] = 'tp-profile'
    if not found_names:
        print('column for TP name not found (adding ids)')
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
        'ping'      : ping_case,
        'col-10'      : ping_case
        }
# header cells with more than 1 colspan
merge_cols = {
        'tagpro-username':'2',
        'location':'2',
        'ping':'2',
        }
# header cells with no extra rowspan
no_rowspan = {
        'ping',
        }
# country flag emojis and ISO codes
countries= {
        'Andorra': (u'\U0001f1e6\U0001f1e9','AND'),
        'Australia': (u'\U0001f1e6\U0001f1fa','AUS'),
        'Belgium': (u'\U0001f1e7\U0001f1ea','BEL'),
        'Bosnia and Herzegovina': (u'\U0001f1e7\U0001f1e6','BIH'),
        'Canada': (u'\U0001f1e8\U0001f1e6','CAN'),
        'Croatia': (u'\U0001f1ed\U0001f1f7','HRV'),
        'Denmark': (u'\U0001f1e9\U0001f1f0','DNK'),
        'Egypt': (u'\U0001f1ea\U0001f1ec','EGY'),
        'Finland': (u'\U0001f1eb\U0001f1ee','FIN'),
        'France': (u'\U0001f1eb\U0001f1f7','FRA'),
        'Germany': (u'\U0001f1e9\U0001f1ea','DEU'),
        'Hungary': (u'\U0001f1ed\U0001f1fa','HUN'),
        'Ireland': (u'\U0001f1ee\U0001f1ea','IRL'),
        'Norway': (u'\U0001f1f3\U0001f1f4','NOR'),
        'Poland': (u'\U0001f1f5\U0001f1f1','POL'),
        'Portugal': (u'\U0001f1f5\U0001f1f9','PRT'),
        'Romania': (u'\U0001f1e7\U0001f1f4','ROU'),
        'Scotland': ((  u'\U0001f3f4'
                     + u'\U000e0067'
                     + u'\U000e0062'
                     + u'\U000e0073'
                     + u'\U000e0063'
                     + u'\U000e0074'
                     + u'\U000e007f'),'SCT'),
        'Spain': (u'\U0001f1ea\U0001f1f8','ESP'),
        'Sweden': (u'\U0001f1f8\U0001f1ea','SWE'),
        'The Netherlands': (u'\U0001f1f3\U0001f1f1','NLD'),
        'UK': (u'\U0001f1ec\U0001f1e7','GBR'),
        'USA': (u'\U0001f1fa\U0001f1f8','USA')
        }
#countrypng = {
#        'Scotland': 'saltire.png'
#        }

# Read table and add class attributes
dptable = etree.parse('dptable.html')
main_header = rearrange_header(dptable.getroot(),store_header(dptable),(9,10))
main_classnames = process_header(main_header,merge_cols,{},no_rowspan)
add_classes_to_table(dptable,main_classnames,special_classnames)
add_country_flags(dptable,countries)

response_form = etree.parse('responses.html')
ids_from_responses = get_profile_ids(response_form.getroot())
add_profile_ids(dptable,main_classnames,ids_from_responses)

# Insert table into main document
parser = etree.HTMLParser()
doc = etree.parse('outline.html', parser)
body = doc.xpath("//div[@id='table-container-2']")[0]
body.append(dptable.getroot())
doc.write('draft-packet.html', pretty_print = True, method = 'html', encoding = 'utf-8')
