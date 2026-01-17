import requests

def login(user, password):
    url = 'https://sigarra.up.pt/feup/pt/mob_val_geral.autentica'
    body = {'pv_login': user, 'pv_password': password}
    r = requests.post(url, data=body)
    if r.status_code == 200:
        return r.cookies

    print(r.text)
    
    raise Exception('Login not successful')

def get_current_enrollments_api(up_number, cookies):
    url = 'https://sigarra.up.pt/feup/pt/mob_fest_geral.perfil'
    params = {'pv_codigo': up_number}
    r = requests.get(url, params=params, cookies=cookies)
    if r.status_code == 200:
        data = r.json()
        courses = [course['cur_id'] for course in data['cursos']]
        print(courses)
        return courses
    
    raise Exception('Could not get current enrollments for ' + str(up_number))

def get_current_enrollments_scrapping(up_number, cookies):
    url = 'https://sigarra.up.pt/feup/pt/fest_geral.cursos_list'
    params = {'pv_num_unico': up_number}
    r = requests.get(url, params=params, cookies=cookies)
    if r.status_code == 200:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')
        divs = soup.find_all('div', {'class': 'estudante-lista-curso-nome'})
        hrefs = [div.a['href'] for div in divs if div.a is not None]
        courses_string = [href.split('=')[1].split('&')[0] for href in hrefs]
        courses = [int(code) for code in courses_string]
        return courses
    
    raise Exception('Could not get current enrollments for ' + str(up_number))

def get_course_name_scrapping(course_code):
    url = 'https://sigarra.up.pt/feup/pt/cur_geral.cur_view'
    params = {'pv_curso_id': course_code}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')
        title_div = soup.find('div', {'id': 'conteudoinner'}).find_all('h1')[1]
        if title_div:
            return title_div.text.strip()
        return "Unknown Course"
    
    raise Exception('Could not get course name for ' + str(course_code))