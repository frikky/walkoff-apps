import requests
import time
import urllib3

timeout=10
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    url = ""
    username = ""
    pw = "" 
    auth = (username, pw)
    query = ""

    test_search(url, auth)

def test_search(url, auth, query):
    # Might need timestamp, dunno how long it currently searches?
    #"search": "| search index=freshcatch",
    query = {
        "search": r'| search %s' % query,
        "exec_mode": "normal",
        "count": 1,
        "earliest_time": "-1h",
        "latest_time": "now"
    }

    print("Current search: %s" % query["search"])
    try:
        ret = run_search(auth, url, query)
    except requests.exceptions.ConnectTimeout as e:
        print("Err: %s" % e)
        return 0 

    if ret.status_code != 201:
        print(ret.text)
        print(ret.status_code)
        return 0 

    search_id = ret.json()["sid"]

    print("Search ID: %s" % search_id)

    ret = get_search(auth, url, search_id)
    if len(ret.json()["entry"]) == 1:
        count = ret.json()["entry"][0]["content"]["resultCount"]
        print("Result: %d" % count)
        return count
    else:
        return 0

def get_search(auth, url, search_sid):
    # Wait for search to be done?
    url = '%s/services/search/jobs/%s?output_mode=json' % (url, search_sid)

    time.sleep(0.2)
    maxrunduration = 30
    ret = ""
    while(True):
        try:
            ret = requests.get(url, auth=auth, timeout=timeout, verify=False)
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            continue

        try:
            content = ret.json()["entry"][0]["content"]
        except KeyError as e:
            print("\nKEYERROR: %s\n" % content)
            time.sleep(1)
            continue

        try:
            if content["resultCount"] > 0 or content["isDone"] or content["isFinalized"] or content["runDuration"] > maxrunduration:
                print(content)
                break
        except KeyError:
            try:
            	print(ret.json()["messages"])
            except KeyError:
                print(content)
            
        time.sleep(1)

    return ret



def run_search(auth, url, query):
    url = '%s/services/search/jobs?output_mode=json' % (url)

    ret = requests.post(url, auth=auth, data=query, timeout=timeout, verify=False)

    return ret

main()
