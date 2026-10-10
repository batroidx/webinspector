import re
from bs4 import BeautifulSoup as Bs

TOKEN_RE = re.compile(r'\(([^()]+)\)|(\S+)')

def parse_wsi_request(text, html):
    if text.strip() == "":
        return html

    parsed_result = []
    result = ""

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        tokens = [
            m.group(1) if m.group(1) is not None else m.group(2)
            for m in TOKEN_RE.finditer(line)
        ]
        parsed_result.append(tokens)

    for i, line in enumerate(parsed_result):
        match line[0].upper():
            case "FROM":
                if not line[tok := 2].upper() == "GET":
                    raise Exception(f"On line {i+1}, token {tok}:`get` expected, {line[tok]} received")
                elif line[tok := 2].upper() == "GET":
                    soup = Bs(html, "lxml")
                    result += f"Get `{line[1]}`:\n"
                    for j, el in enumerate(soup.select(line[1])):
                        if line[3] == "value":
                            result += f"({j+1}) {el.text}\n"
                        elif line[3].startswith("@"):
                            attr = line[3].lstrip("@")
                            value = el.get(attr)
                            result += f"({j+1}) {value if value is not None else '<no ' + attr + '>'}\n"
                        else:
                            raise Exception(f"On line {i+1}, token 3:Unknown filter")
                    result += "\n\n"
            case _:
                raise Exception(f"On line {i+1}:Unknown instruction")

    return result