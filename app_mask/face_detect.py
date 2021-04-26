import requests
import base64

ak = 'QsPqs20yfvQ7QcdnYfdWC5Ei'
sk = 'EEMdjil0u1CW5uI3ts1mLD0VCQvTGYs6'


def get_at(api_key, secret_key):
    host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + api_key + \
           "&client_secret=" + secret_key
    response = requests.get(host)
    if response:
        data = response.json()
        at = data["access_token"]
        return at


def mask_detect(path):
    return_data = {'info': [], 'num': 0, 'msg': ''}
    access_token = get_at(ak, sk)
    detect_request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect" + "?access_token=" + access_token
    search_request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search" + "?access_token=" + access_token
    with open(path, 'rb') as f:
        p_data = f.read()
        p_data = base64.b64encode(p_data)
        data = str(p_data, "utf-8")
        f.close()
    params = "{\"image\":\"" + str(data) + "\",\"image_type\":\"BASE64\",\"face_field\":\"mask\"}"
    headers = {'content-type': 'application/json'}
    response1 = requests.post(detect_request_url, data=params, headers=headers)
    res_data = response1.json()
    face_num = res_data['result']['face_num']
    if face_num != 0:
        for n in range(face_num):
            mask_data = res_data['result']['face_list'][n]['mask']
            is_mask = mask_data['type']
            return_data['info'].append({'is_mask': 0, 'student_id': 0})
            if is_mask == 1:
                return_data['info'][n]['is_mask'] = 1
            elif is_mask == 0:
                return_data['info'][n]['student_id'] = 'unknown'
    else:
        return [{'msg': 'WRONG', 'num': 0, 'info': ""}]
    # ----------------------------

    params = "{\"image\":\"" + str(data) + "\",\"image_type\":\"BASE64\",\"group_id_list\":\"students\"," \
                                           "\"quality_control\":\"LOW\",\"liveness_control\":\"NORMAL\"} "
    headers = {'content-type': 'application/json'}
    response2 = requests.post(search_request_url, data=params, headers=headers)
    res_data2 = response2.json()
    if res_data2['error_msg'] == 'SUCCESS':
        for n in range(face_num):
            return_data['info'][n]['student_id'] = res_data2['result']['user_list'][n]['user_id']
    return_data['msg'] = 'SUCCESS'
    return_data['num'] = face_num
    return return_data


def face_register(path, trans_id):
    access_token = get_at(ak, sk)
    with open(path, 'rb') as f:
        p_data = f.read()
        p_data = base64.b64encode(p_data)
        data = str(p_data, "utf-8")
        f.close()
    request_url = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add' + "?access_token=" + access_token
    params = "{\"image\":\"" + data + "\",\"image_type\":\"BASE64\"," \
                                      "\"group_id\":\"students\",\"user_id\":\"" + trans_id + \
             "\",\"quality_control\":\"LOW\",\"liveness_control\":\"NORMAL\"} "
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    return response.json()['error_msg']


def user_delete(trans_id):
    user_face_token = user_get(trans_id)
    if user_face_token == -1:
        return {"msg": "FAIL"}
    access_token = get_at(ak, sk)
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/delete"
    params = "{\"user_id\":\""+str(trans_id)+"\",\"group_id\":\"students\",\"face_token\":\""+str(user_face_token)+"\"}"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response.json()['error_msg'] == 'SUCCESS':
        return {"msg": "SUCCESS"}
    else:
        return {"msg": "FAIL"}


def user_get(trans_id):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/getlist"
    params = "{\"user_id\":\"" + str(trans_id) + "\",\"group_id\":\"students\"}"
    access_token = get_at(ak, sk)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response.json()["error_msg"] == "SUCCESS":
        return response.json()['result']['face_list'][0]['face_token']
    else:
        return -1



if __name__ == "__main__":
    print(user_delete(1))
