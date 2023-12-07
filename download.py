import requests, os
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

HOME = Path(__file__).parent
COOKIE = (HOME/"cookie.txt").read_text().strip()

parser = ArgumentParser()
parser.add_argument("-d", "--day", type=int, default=datetime.now().day, help="The day")
parser.add_argument("-y", "--year", type=int, default=datetime.now().year, help="The year")
args = parser.parse_args()

folder_name = f"Day_{args.day}"
os.makedirs(HOME/folder_name, exist_ok=True)

url = f"https://adventofcode.com/{args.year}/day/{args.day}"
response = requests.get(url)

if response.status_code == 200:
    data = response.text
    with open(HOME/folder_name/"test.txt", "w") as file:
        file.write(data.split("<pre><code>")[1].split("</code></pre>")[0].removesuffix("\n"))
else:
    print(f"Failed to download data from {url}")


url = f"https://adventofcode.com/{args.year}/day/{args.day}/input"
response = requests.get(url, cookies={"session": COOKIE})

if response.status_code == 200:
    data = response.text
    with open(HOME / folder_name / "input.txt", "w") as file:
        file.write(data.removesuffix("\n"))
else:
    print(f"Failed to download data from {url}")


template = """\
from pathlib import Path

HOME = Path(__file__).parent

with open(HOME/"test.txt") as f:
    pass
"""

for part in range(1, 3):
    if not (HOME / folder_name / f"p{part}.py").exists():
        with open(HOME / folder_name / f"p{part}.py", "w") as file:
            file.write(template)