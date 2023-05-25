import requests
import pandas as pd


# выделяет id из url
def get_file_id(url):
    return url.split('id=')[1]


# подается список со ссылками на файлы, затем фильтруется по пустым полям и размеру файла более 10кб
# далее id добавляется в ключ "files"
def get_url(file):
    attachments = []
    if file.get("value") is not None:

        for i in file['value']:
            if i['size'] > 10000:
                attachments.append(i['id'])
            else:
                pass
        return attachments

    else:
        return "no file"


# form_nr = 1134549 HC Finances RED
def get_task_list_red(form_content):
    task_list = []

    for task in form_content['tasks']:
        task_dict = {}
        task_dict['date'] = task['fields'][3]['value']
        task_dict['invoice'] = task['fields'][4]['value']
        company = task['fields'][5]
        if company.get("value") is not None:
            task_dict['company'] = company['value']['values'][1]
        else:
            task_dict['company'] = "no data"
        task_dict['netto'] = task['fields'][8]['value']
        task_dict['vat'] = task['fields'][9]['value']
        task_dict['total'] = task['fields'][10]['value']
        task_dict['currency'] = task['fields'][11]['value']['choice_names'][0]

        files = task['fields'][7]
        task_dict['files'] = get_url(files)

        task_list.append(task_dict)
    return task_list


# form_nr = 1125654 HC Finances GREEN
def get_task_list_green(form_content):
    task_list = []

    for task in form_content['tasks']:
        task_dict = {}
        task_dict['date'] = task['fields'][4]['value']
        task_dict['invoice'] = task['fields'][16]['value']
        company = task['fields'][0]
        if company.get("value") is not None:
            task_dict['company'] = company['value']['values'][0]
        else:
            task_dict['company'] = "no data"
        task_dict['netto'] = task['fields'][8]['value']
        task_dict['vat'] = task['fields'][9]['value']
        task_dict['total'] = task['fields'][10]['value']
        task_dict['currency'] = task['fields'][17]['value']['choice_names'][0]

        files = task['fields'][27]
        task_dict['files'] = get_url(files)

        task_list.append(task_dict)
    return task_list


def download_attachment_by_id(id, token, file_path, file_name):
    url = f"https://api.pyrus.com/v4/files/download/{id}"

    headers = {
        "Content-Type": "application/octet-stream",
        "Authorization": "Bearer " + token
    }
    response = requests.get(url, headers=headers)

    content_type = response.headers.get("Content-Type")
    if "pdf" in content_type:
        extension = ".pdf"
    elif "jpeg" in content_type:
        extension = ".jpeg"
    elif "png" in content_type:
        extension = ".png"
    elif "msword" in content_type:
        extension = ".xdoc"
    else:
        # Add other content types as needed
        print(content_type)
        raise Exception("Unsupported content type")

    with open(f"{file_path}/{file_name}{extension}", "wb") as file:
        file.write(response.content)


def sort_by_date(list_of_dicts):
    from datetime import datetime, timedelta

    start_date = datetime.strptime("2022-12-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-01-31", "%Y-%m-%d")

    filtered_list = [task for task in list_of_dicts if
                     start_date <= datetime.strptime(task["date"], "%Y-%m-%d") <= end_date]


def main(token, form_nr, task_list, currency):
    count = 0
    for task in task_list:
        if task['files'] != "no file" and task['currency'] == currency:
            filename = f"{task['date']} {task['invoice']} {task['company']}"
            file_name = filename.replace("/", "_")
            path_name = f"{form_nr}/{currency}"

            for i in task['files']:
                download_attachment_by_id(i, token, path_name, f"{file_name}[{i}]")
                count += 1
        else:
            pass
    print("Total number of iterations:", count)


def save_to_excel(task_list, filename, save=bool):
    pd.options.display.max_rows = None
    pd.options.display.max_columns = 9
    pd.options.display.max_colwidth = 1000
    pd.options.display.width = None
    df = pd.DataFrame(task_list)
    df.index += 1
    print(df)
    if save:
        return df.to_excel(f"{filename}.xlsx", index=False)
    else:
        pass