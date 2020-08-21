import requests

#/telegram/<userid>
telegram_api = "http://127.0.0.1:8080"

def get_telegram_api_userid(userid):
    try:
        res = requests.get(f"{telegram_api}/telegram/{userid}").text
    except Exception as e:
        print("10.", e) 
        res = "not"
    if res == "not":
        return "NULL"
    else:
        try:
           return eval(res)
        except:
            return "NULL"
def get_telegram_api_usermane(username):
    try:
        res = requests.get(f"{telegram_api}/telegram/{username}").text
    except Exception as e: 
        print("23.", e)
        return "NULL"
    
    return res
if __name__ == "__main__":
    print(get_telegram_api_usermane("@username"))