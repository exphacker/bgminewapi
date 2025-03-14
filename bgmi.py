from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

headersList = {
 "Host": "www.unipin.com",
 "accept": "application/json, text/javascript, */*; q=0.01",
 "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,zh-CN;q=0.6,zh;q=0.5",
 "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
 "cookie": "_scid_r=NZLpR8b8G2MfHWAGR2mgjC8npcRn8UXJAlG9zQ;_ga_09T7E74QTG=GS1.1.1741958039.1.1.1741958087.12.0.0;_ym_uid=1741958041300451511;_ga=GA1.1.1251543512.1741958039;redeem_banner=yes;_ScCbts=%5B%5D;_ym_d=1741958041;_fbp=fb.1.1741958039072.740508206936530972;_gcl_au=1.1.513295458.1741958039;_gid=GA1.2.84284798.1741958039;_scid=OhLpR8b8G2MfHWAGR2mgjC8npcRn8UXJ;_sctr=1%7C1741890600000;_ym_isad=2;region=IN;unipin_session=eyJpdiI6ImFkU29DSzIrUjRFanNyY2J1d2tzNFE9PSIsInZhbHVlIjoicFZ2clNISGNrK2NMOXdzRjhzTlFGdmN0RmFpbXBYT2ZpQTNVdFwvY0I4a1Z2dmYzeGx4YlZyeTdEQ0dyUVRMSFN4bzM1ZWxyWndXUlVVQlRLbE9OMGRoNHhnK0hpRVgxMEhvUHkxd0ZZanlXSUxTakV3S2p4NEUyelFMNFAyQlNTIiwibWFjIjoiMDk1ZDhlNzk0ZTc0NTA3MGQyOGJhYWVlNDE4OTdiZGIwMzk0YjcwMzY5NGYyN2I1NzQ4NjAyNDhiYTAwYzIyNyJ9;XSRF-TOKEN=eyJpdiI6ImszRHNHRFdTOUluY0Q0V2J6ZFNJeWc9PSIsInZhbHVlIjoidTFrWDVMWUFDZEwwTXF5WVwvXC9SWFwvZ01Bd3dHMktwWWV6SlQ0YTBOSTJDRFBGUDN5aXJxNjlWczR5T2JyMVllSyIsIm1hYyI6ImE3MWU3ZGY0MmVhNzdkMjI0NjU0YzQzNDM4MDM0MWNmNGJiMWRjNGQyYjgxZWFlNGNiMWQ2YjFmYWQzMzk5NTAifQ%3D%3D",
 "origin": "https://www.unipin.com",
 "priority": "u=1, i",
 "referer": "https://www.unipin.com/in/bgmi",
 "sec-fetch-dest": "empty",
 "sec-fetch-mode": "cors",
 "sec-fetch-site": "same-origin",
 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
 "x-csrf-token": "1wavzaXvne40bEXhWtWVa5W9NE6Sm6on30n4qFTc",
 "x-requested-with": "XMLHttpRequest" 
}


def get_checkout_details(dyn):
    url = f"https://www.unipin.com/in/bgmi/checkout/{dyn}"
    response = requests.get(url, headers=headersList)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("div", class_="details-row")
        for row in rows:
            label = row.find("div", class_="details-label text-white-50")
            value = row.find("div", class_="details-value")
            if label and value and "Username" in label.get_text(strip=True):
                return value.get_text(strip=True)
    return None


@app.route("/get_user", methods=["POST", "GET"])
def get_user():
    uid = request.args.get("uid") or request.json.get("uid")
    if not uid:
        return "Uid is Required", 400


    reqUrl = "https://www.unipin.com/in/bgmi/inquiry"
    payload = f"rgid=WURTVm0wM1FzNGR1WS9jMkp1d2puQT09&userid={uid}&did=5209&pid=764&influencer=&cust_email=expviphacker7@gmail.com"
    response = requests.post(reqUrl, data=payload, headers=headersList)

    if response.status_code == 200:
        try:
            json_response = response.json()
            if json_response.get("status") == "1":
                dyn = json_response.get("message")
                username = get_checkout_details(dyn)
                return username if username else "Username not found", 200
            else:
                return "Incorrect Uid or Player Id", 400
        except requests.exceptions.JSONDecodeError:
            return jsonify({"error": "Failed to decode JSON response"}), 500
    else:
        return jsonify({"error": f"Request failed with status code {response.status_code}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)