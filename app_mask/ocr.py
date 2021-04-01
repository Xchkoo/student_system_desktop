import requests
import base64
import time
from app_mask import face_detect

ak = 'BuWEEPE7UUg5dGmGObDyEX1s'
sk = 'ddkiWK91Yudkb5P0iMsh9LR4WCnkwIdO'


def ocr(path):
    at = face_detect.get_at(ak, sk)
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request"
    result_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/get_request_result"
    f = open(path, 'rb')
    img = base64.b64encode(f.read())
    request_params = {"image": img}
    request_url = request_url + "?access_token=" + at
    result_url = result_url + "?access_token=" + at
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=request_params, headers=headers)
    print(response.json())
    request_id = response.json()['result'][0]['request_id']
    print(request_id)
    time.sleep(6)
    result_params = {"request_id": str(request_id), "result_type": "excel"}
    result = requests.post(result_url, data=result_params, headers=headers)
    print(result.json())


if __name__ == '__main__':
    ocr("../表格数据.jpg")
