import json
import os

def get_data():
    with open('./db/data.json', 'r') as file:
        data = json.load(file)
    return data

def calculate(volume, choice):
    volumes = get_data()
    volume = float(volume)
    volume = float(volume / 1000)
    items = []
    for i in volumes:
        items.append(i)
    valor = volumes.get(items[choice]) * volume
    return valor

def salvar(key, new_data):
    data = get_data()
    with open('./db/data.json', 'w') as file:
        data[key] = new_data
        json.dump(data, file)

def resetar():
    with open('./db/backup.json', 'r') as file:
        data = json.load(file)
        with open('./db/data.json', 'w') as file2:
            file2.write(json.dumps(data))

if __name__ == '__main__':
    print(calculate(1000, 1))

