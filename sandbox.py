#Archive
def getnames(text):
    person_list = []
    person_names = person_list

    def get_human_names(text):
        tokens = nltk.tokenize.word_tokenize(text)
        pos = nltk.pos_tag(tokens)
        sentt = nltk.ne_chunk(pos, binary=False)

        person = []
        name = ""
        for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1:  # avoid grabbing lone surnames
                for part in person:
                    name += part + ' '
                if name[:-1] not in person_list:
                    person_list.append(name[:-1])
                name = ''
            person = []

    #     print (person_list)

    names = get_human_names(text)
    for person in person_list:
        person_split = person.split(" ")
        for name in person_split:
            if wordnet.synsets(name):
                if (name in person):
                    person_names.remove(person)
                    break
    # print('Names')
    # print(person_names)
    name_gender = []
    for first_name in person_names:
        # first name
        first = first_name.split(' ')[0]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        genderchecker = r'http://www.namegenderpro.com/search-result/?gender_name='
        gender_url = genderchecker + first
        response = requests.get(gender_url)
        if response.status_code == 200:
            session = requests.Session()
            html = session.get(gender_url, headers=headers)
            soup = BeautifulSoup(html.content, 'html.parser')
            gender = soup.find('div', class_='searchresult_top_heading')
            gender = (gender.find('b')).text
            if gender in ['Male', 'Female', 'Unisex']:
                name_gender.append(first_name + '-' + gender)
    print(name_gender)
    return (name_gender)


def getnames2(text):
    pattern1 = "([A-ZÄÖÜß][a-zäßöü]+\s)(von|Von|da|Da|de|De|d'|du|Della|del|Del|della|di|y|Y'|[A-Z].)(\s[A-ZÄÖÜß][a-zäßöü,]+|[A-ZÄÖÜß][a-zäßöü,]+)"  # Von/von--Good
    pattern2 = '([A-ZÄÖÜß][a-zäöüéàèéùâêßîôûçëïü]+[- ][A-ZÄÖÜß][a-zäßöüééàèùâêîôûçëïü]+)'  # -- 2words
    pattern3 = '([A-ZÄÖÜß][a-zäöüééàèùâßêîôûçëïü]+[- ][A-ZÄÖÜß][a-zäöüééàèùâêßîôûçëïü]+[ -][A-ZÄÖÜß][a-zäöüéàèùâêßîôûçëïü]+)'  # --3words
    pattern4 = '([A-ZÄÖÜß][a-zäöüéàèùâßêîôûçëïü]+ [- ][A-ZÄÖÜß][a-zäöüéàèéùâßêîôûçëïü]+[ -][A-ZÄÖÜß][a-zäöüééàèùâêîôûçßëïü]+[ -][A-ZÄÖÜß][a-zäöüéàèùâßêîéôûçëïü]+)'  # 4words
    pat_regex = re.compile("|".join("({})".format(x) for x in [pattern4, pattern3, pattern2, pattern1]))
    matches = pat_regex.findall(text)
    # matches = re.findall(pattern, text)
    for_filter = list(set(matches))
    name = []
    # print(for_filter)
    for_filter2 = [list(set(x)) for x in for_filter if x]
    for elem in for_filter2:
        for sub in elem:
            if len(sub.split(' ')) > 1 and sub.split(' ')[0] != '':
                print(sub)
                name.append(sub)
    name_gender = []
    for first_name in name:
        first = first_name.split(' ')[0]
        print(first)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        genderchecker = r'http://www.namegenderpro.com/search-result/?gender_name='
        gender_url = genderchecker + first
        response = requests.get(gender_url)
        if response.status_code == 200:
            session = requests.Session()
            html = session.get(gender_url, headers=headers)
            soup = BeautifulSoup(html.content, 'html.parser')
            gender = soup.find('div', class_='searchresult_top_heading')
            gender = (gender.find('b')).text
            if gender in ['Male', 'Female', 'Unisex']:
                name_gender.append(first_name + '-' + gender)
    #print(name_gender)
    return (name_gender)
