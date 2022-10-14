import requests
import re

species = {
    "12":  "Rode Wouw",
    "13":  "Blauwe Kiekendief",
    "14":  "Grauwe Kiekendief",
    "74":  "Boomvalk",
    "81":  "Bruine Kiekendief",
    "82":  "Buizerd",
    "117": "Havik",
    "178": "Sperwer",
    "188": "Torenvalk",
    "321": "Ruigpootbuizerd",
    "325": "Slechtvalk",
    "326": "Smelleken",
    "346": "Visarend",
    "349": "Wespendief",
    "353": "Zeearend",
    "364": "Zwarte Wouw",
    "1385": "Grijze Wouw",
}

date_after = "2021-01-01"


def getPage(url):
    f = f = requests.get(url)
    return f.text.split('\n')

def compose_url( species, page):
    base_url = 'https://waarnemingen.be/species/<SPECIES>/photos/?date_after={}}?likes=1&page=<PAGE>'.format(date_after)
    return (base_url.replace("<SPECIES>", species)).replace("<PAGE>", page)


def number_of_pages(lines):
    pages = 1
    for l in lines:
        if "&amp;page=" in l:
            m = re.search('>(\d+)<', l)
            if m:
                pages = max(int(m.group(1)),pages)
    return(pages)

def new_entry():
    return {"image": "", "observer": "", "observation": ""}

def get_images(lines, sp):
    list = {}


    regex_photo = '<a href="/media/photo/([0-9]+.jpg)" class="lightbox-gallery-image" tabindex="-1">'
    regex_observation = '/observation/([0-9]+)/'
    regex_user = '<i class="fas fa-user fa-fw"></i>(.+)'
    _id = ""
    for l in lines:
        if '<figure class="lightbox-gallery">' in l:
            _id = ""
        m = re.search( regex_photo, l)
        if m:
            if m.group(1) not in list.keys():
                _id = m.group(1)
                list[_id] = new_entry()
            list[_id]["species"] = species[sp]

        if _id != "":
            m = re.search(regex_observation, l)
            if m:
                list[_id]["observation"] = m.group(1)
            m = re.search(regex_user, l)
            if m:
                list[_id]["observer"] = m.group(1).strip()
    return list

specs = {}
for spec in species.keys():
    pages = 1
    tot_pages = -1
    while True:
        print("Getting images list for {} page {}".format(species[spec],pages))
        Page = getPage(compose_url(spec, "{}".format(pages)))
        if tot_pages == -1:
            tot_pages = number_of_pages(Page)
        specs = specs | get_images(Page , spec)
        pages+=1
        if pages > tot_pages:
            break

f = open("quizInfo.txt","w")
f.write("var quizInfo= [][]string{\n")
for data in specs.keys():
    f.write('     {{"{}","{}","{}","{}"}},\n'.format(data, specs[data]["species"], specs[data]["observation"], specs[data]["observer"]))
f.write("}")


