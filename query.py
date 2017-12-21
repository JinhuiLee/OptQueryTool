import requests
from pyquery import PyQuery as pq

STATUS_OK = 0
STATUS_ERROR = -1

def poll_optstatus(casenumber):
    """
    poll USCIS case status given receipt number (casenumber)
    Args:
        param1: casenumber the case receipt number
    Returns:
        a tuple (status, details) containing status and detailed info
    Raise:
        error:
    """
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language':
        'en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3',
        'Cache-Control': 'no-cache',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'egov.uscis.gov',
        'Referer': 'https://egov.uscis.gov/casestatus/mycasestatus.do',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }
    url = "https://egov.uscis.gov/casestatus/mycasestatus.do"
    data = {"appReceiptNum": casenumber, 'caseStatusSearchBtn': 'CHECK+STATUS'}

    res = requests.post(url, data=data, headers=headers)
    doc = pq(res.text)
    status = doc('h1').text()
    code = STATUS_OK if status else STATUS_ERROR
    details = doc('.text-center p').text()
    i765 = "I-765" in details or "new card" in details
    return (i765, code, status, details)

start = 1890010000

count = 500
for i in range(start, start - count,-1):
    i765, code, status, detail = poll_optstatus("YSC" + str(i))
    if i765:
        print "YSC" + str(i), code, status, detail.split(",")[0]
    