import json

def save_json(data, path, encoding="utf-8", ensure_ascii=False, indent=4):
    with open(path, "w", encoding=encoding) as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)