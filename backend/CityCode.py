import requests
import json
import pandas as pd


def get_sido_info():
    down_url = "https://new.land.naver.com/api/regions/list?cortarNo=0000000000"
    r = requests.get(
        down_url,
        data={"sameAddressGroup": "false"},
        headers={
            "Accept-Encoding": "gzip",
            "Host": "new.land.naver.com",
            "Referer": "https://new.land.naver.com/complexes/102378?ms=37.5018495,127.0438028,16&a=APT&b=A1&e=RETAIL",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        },
    )
    r.encoding = "utf-8-sig"
    temp = json.loads(r.text)
    try:
        temp = pd.DataFrame(temp["regionList"])[["cortarNo", "cortarName"]]
    except:
        temp = []
    return temp


def get_gungu_info(sido_code):
    down_url = "https://new.land.naver.com/api/regions/list?cortarNo=" + sido_code
    r = requests.get(
        down_url,
        data={"sameAddressGroup": "false"},
        headers={
            "Accept-Encoding": "gzip",
            "Host": "new.land.naver.com",
            "Referer": "https://new.land.naver.com/complexes/102378?ms=37.5018495,127.0438028,16&a=APT&b=A1&e=RETAIL",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        },
    )
    r.encoding = "utf-8-sig"
    temp = json.loads(r.text)
    try:
        temp = pd.DataFrame(temp["regionList"])[["cortarNo", "cortarName"]]
    except:
        temp = []
    return temp


def get_dong_info(gungu_code):
    down_url = "https://new.land.naver.com/api/regions/list?cortarNo=" + gungu_code
    r = requests.get(
        down_url,
        data={"sameAddressGroup": "false"},
        headers={
            "Accept-Encoding": "gzip",
            "Host": "new.land.naver.com",
            "Referer": "https://new.land.naver.com/complexes/102378?ms=37.5018495,127.0438028,16&a=APT&b=A1&e=RETAIL",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        },
    )
    r.encoding = "utf-8-sig"
    temp = json.loads(r.text)
    try:
        temp = pd.DataFrame(temp["regionList"])[["cortarNo", "cortarName"]]
    except:
        temp = []
    return temp


def get_apt_list(dong_code):
    down_url = (
        "https://new.land.naver.com/api/regions/complexes?cortarNo="
        + dong_code
        + "&realEstateType=APT&order="
    )
    r = requests.get(
        down_url,
        data={"sameAddressGroup": "false"},
        headers={
            "Accept-Encoding": "gzip",
            "Host": "new.land.naver.com",
            "Referer": "https://new.land.naver.com/complexes/102378?ms=37.5018495,127.0438028,16&a=APT&b=A1&e=RETAIL",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        },
    )

    r.encoding = "utf-8-sig"
    temp = json.loads(r.text)
    try:
        temp = pd.DataFrame(temp["complexList"])[["complexNo", "complexName"]]
    except:
        temp = []
    return temp


def get_apt_info(apt_code):
    down_url = "https://new.land.naver.com/api/complexes/overview/" + apt_code
    r = requests.get(
        down_url,
        data={"sameAddressGroup": "false"},
        headers={
            "Accept-Encoding": "gzip",
            "Host": "new.land.naver.com",
            "Referer": "https://new.land.naver.com/complexes/"
            + apt_code
            + "?ms=37.482968,127.0634,16&a=APT&b=A1&e=RETAIL",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        },
    )
    r.encoding = "utf-8-sig"
    temp = json.loads(r.text)
    return temp


if __name__ == "__main__":
    sido_list = get_sido_info()
    gungu_list = get_gungu_info(sido_list["cortarNo"][0])
    dong_list = get_dong_info(gungu_list["cortarNo"][0])
    apt_list = get_apt_list(dong_list["cortarNo"][0])
    apt_info = get_apt_info(apt_list["complexNo"][0])

    print(sido_list)
    print(gungu_list)
    print(dong_list)
    print(apt_list)
    for dict_key, dict_item in apt_info.items():
        print("key", dict_key, "item", dict_item)
