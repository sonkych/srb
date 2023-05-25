import requests
import json

# Get auth token from pyrus
def get_token(login, key):
    url = "https://api.pyrus.com/v4/auth"
    headers = {
        "content-type": "application/json"
    }

    params = {
        "login": login,
        "security_key": key
    }

    response = requests.get(url, params=params, headers=headers)
    answer = response.json()
    auth_token = answer.get("access_token")
    print(f"Статус Токена: {response.status_code}")
    return auth_token


# GET data from Form
def get_form(form_nr, auth_token):
    url = f"https://api.pyrus.com/v4/forms/" ## {form_nr}/register?&include_archived=y"
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + auth_token
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    convert_to_json(data, "form_register")
    # print(headers['Authorization'])
    print(f"Статус получения данных Формы: {response.status_code}")
    # print(data)
    return data


# GET data from Task
def get_task(task, auth_token):
    url = f"https://api.pyrus.com/v4/tasks/{task}"
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + auth_token
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    convert_to_json(data, "task")
    # print(headers['Authorization'])
    print(f"Статус получения данных Задачи: {response.status_code}")
    # print(data)
    return data


# Convert json to readable and write to json.file
def convert_to_json(data, filename):
    json_object = json.dumps(data, indent=5)
    with open(f"json/{filename}.json", 'w') as outfile:
        outfile.write(json_object)


# Send text to comments
def post_comment(task_id, auth_token):
    url = f'https://api.pyrus.com/v4/tasks/{task_id}/comments'

    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + auth_token
    }

    content = {"text": "Hello"}
    response = requests.post(url, data=json.dumps(content), headers=headers)
    print(f"Статус отправки данных в комментарий задачи: {response.status_code}")
    # convert_to_json(data, "comment")
    return response


# Send text to field in task
def post_to_field(field_id, task_id, auth_token):
    url = f'https://api.pyrus.com/v4/tasks/{task_id}/comments'
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + auth_token
    }

    content = {
        "field_updates": [{"id": field_id, "value": "hello from my PyCharm!"}]
    }
    response = requests.post(url, data=json.dumps(content), headers=headers)
    print(f"Статус отправки данных в поле задачи: {response.status_code}")
    convert_to_json(response.json(), "comment_to_field")
    return response


def post_guid_ti_field(task_id, auth_token):
    url = f'https://api.pyrus.com/v4/tasks/{task_id}/comments'
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + auth_token
    }

    content = {
        "field_updates": [{"id": 3, "value": [{"guid": "2dcb49ed-2bc3-460c-afbe-c45a24f97b9d"}]}]
    }
    response = requests.post(url, data=json.dumps(content), headers=headers)
    print(f"Статус отправки данных в поле задачи: {response.status_code}")
    convert_to_json(response.json(), "guid_to_field")
    return response
