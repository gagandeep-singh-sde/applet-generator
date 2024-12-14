# encoding=utf-8
import codecs


def ReadToolboxDB(filepath):
    """
    Read the main database file and parse its content.
    """
    database = []
    with codecs.open(filename=filepath, mode="r", encoding="utf-8") as reader:
        entries = "".join(reader.readlines()).split("\r\n\r\n\\")

    for entry in entries:
        single_entry = {"keys": []}

        lines = entry.split("\r\n\\")
        for field in lines:
            if len(field.strip()) <= 0:
                continue
            key, value = _parse_field(field)
            if key:
                single_entry["keys"].append(key)
                if key not in single_entry:
                    single_entry[key] = []
                single_entry[key].append(value)

        database.append(single_entry)
    return database


def _parse_field(field):
    """
    Parse a field from the database entry.
    """
    if "_sh " in field or "_DateStampHasFourDigitYear" in field:
        print("\r\nskipping ", field)
        return None, None
    elif field.strip().find(" ") == -1:
        key = field.strip()
        value = ""
        if field.find(" ") > -1:
            value = " "
        return key, value
    else:
        key, value = field.strip().split(" ", 1)
        return key.strip(), value.strip()
