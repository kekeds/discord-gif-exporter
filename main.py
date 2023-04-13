import requests, base64, string
from colorama import Fore as f
import os; os.system("cls")
import ctypes

normal_chars=string.ascii_letters+string.digits+"/.:"
good_gifs=list()

class stats():
    valid=0
    invalid=0
    total=0
    checked=0

def get_gifs(token):
    return requests.get("https://discord.com/api/v9/users/@me/settings-proto/2",headers={
        "authorization": token,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }).text

def filter(req):
    req_decoded = base64.b64decode(req.encode()).decode('unicode_escape')
    filtered_chars = ''.join(char for char in req_decoded if char in normal_chars or char == '\n')

    return filtered_chars.splitlines()

def extract(gifs):
    for gif in gifs:
        try:
            new_gif=gif.split("https://")[1].split(".gif")[0]
            new_gif=f"https://{new_gif}.gif"
            good_gifs.append(new_gif)
            print(f"{f.YELLOW}FOUND GIF {new_gif}")
        except IndexError:
            pass

    return good_gifs

def check(gifs):
    valid_gifs=list()
    stats.total=len(gifs)

    for gif_url in gifs:
        req=requests.get(gif_url,allow_redirects=True)
        if req.ok:
            print(f"{f.LIGHTGREEN_EX}VALID GIF: {req.url}")
            valid_gifs.append(req.url)
            stats.valid+=1

        else:
            print(f"{f.RED}INVALID GIF: {gif_url}")
            stats.invalid+=1

        stats.checked+=1
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"kek gif exporter - valid: {str(stats.valid)} | invalid: {str(stats.invalid)} | checked: {str(stats.checked)}/{str(stats.total)}"
        )

    return valid_gifs

token=input("my token: ")
valid_gifs=check(extract(filter(get_gifs(token))))

print(f.LIGHTWHITE_EX+("="*50)+"\n")
print(f"{f.LIGHTGREEN_EX}valid: {str(stats.valid)} {f.LIGHTWHITE_EX}| {f.RED}invalid: {str(stats.invalid)}")

with open("gifs.txt","w+") as file:
    for valid_gif in valid_gifs:
        file.write(valid_gif+"\n")

input(f"{f.LIGHTWHITE_EX}\n[!] saved gifs to file")