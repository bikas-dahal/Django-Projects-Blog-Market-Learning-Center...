import requests


base_url = 'http://127.0.0.1:8000/api/'
url = f'{base_url}courses/'

available_courses = []

username = 'ripple'
password = 'daman123!'

while url is not None:
    print(f'Loading courses from {url}')
    r = requests.get(url)
    response = r.json()
    print(f'Response, {response}')
    url = response['next']
    print(f' url = {url}')
    courses = response['results']
    available_courses += [course['title'] for course in courses]
    print(f'List: {available_courses}')
print(f'Available courses: {", ".join(available_courses)}')

for course in courses:
    course_id = course['id']
    course_title = course['title']
    r = requests.post(
        f'{base_url}courses/{course_id}/enroll/',
        auth=(username, password)
    )
    if r.status_code == 200:
        # successful request
        print(f'Successfully enrolled in {course_title}')