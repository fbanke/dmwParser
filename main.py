from lxml import etree
from sqlitedict import SqliteDict
import os
os.unlink('./dmw.sqlite')

dmw_dict = SqliteDict('./dmw.sqlite', autocommit=True) #initialize dictionary

context = etree.iterparse('temp.xml')

#get rid of the namespace in the tag
def namespacesuppressor(tag):
   if tag.startswith("{"):
       tag = element.tag.split('}', 1)[1]  # strip namespace
   return tag


def writetodb(key, value):
    with SqliteDict('./dmw.sqlite'):
        dmw_dict[key] = value

key = ""
value = ""
for event, element in context:
    #print(element.tag)
    if element.tag.find('RegistreringNummerNummer') != -1:  # because this is the key
        element.tag = namespacesuppressor(element.tag)
        #print(element.tag.strip(),'|',element.text.strip()) #debug
        key = element.text
        #print(key) #Debug

    if element.tag.find('RegistreringNummerNummer') != 1:  # because everything else is a value
        if len(element.text.strip()) != 0:
            element.tag = namespacesuppressor(element.tag)
            (element.tag.strip(),'|',element.text.strip())
            if len(value) > 0:
                value = value + element.tag.strip() + '|' + element.text.strip() + '|'
            else:
                value = element.tag.strip() + '|' + element.text.strip() + '|'
            # print(value) #Debug
            writetodb(key, value)
    element.clear()

    #Clear Parent(s) of element
    while element.getprevious() is not None:
        del element.getparent()[0]

print (dmw_dict['CJ29403'])
dmw_dict.close()