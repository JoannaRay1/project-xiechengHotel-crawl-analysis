import requests,re
from openpyxl import workbook

start_url = 'https://hotels.ctrip.com/hotels/list?city=2&checkin=2022/06/16&checkout=2022/06/17&optionId=2&optionType=City&directSearch=0&display=%E4%B8%8A%E6%B5%B7&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1&pageNo={}'
headers = {#应对反爬机制
    'cookie': 'ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; MKT_CKID=1622722874094.5cqwg.okdg; _RGUID=9361c629-9489-4da6-8e9a-0065d3feaedc; _RDG=28fc2173fc604c27831ee6e0d2ca1960fb; _RSG=csKYKcYnXD9Sxg_JN60Qw8; IBU_TRANCE_LOG_P=24809970754; _ga=GA1.2.841147743.1622722874; _abtest_userid=8f0f1fef-ed95-49ab-a86b-ab81fce17a92; appFloatCnt=5; cticket=3458DF8F63C54ED77786CA9F3EC654DF9E4127106A29D9313515F7B7CD91AF6C; AHeadUserInfo=VipGrade=20&VipGradeName=%B2%AC%BD%F0%B9%F3%B1%F6&UserName=%CE%C2%CB%BC%C3%F4&NoReadMessageCount=0; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yojXN5UTMe2Bf2mUE6PlX6FyYlfjHJnCKESbRIWtYFLtm/6iBsO30fuPWT0fDkK22qcsBwc/e0Gt/llVWCt1sEjR1bM90gSFvy+/wfmaF4YWJCvdr1C2DLb/d2SAcdO/2F+qcqpUF6KaWA/z3WqCECEdjaAfmpTVpXbq88vf4zeDHYbVIuUm1v7tJpnSCnRffvEGpWX6jQS8eU2veg3m2FOpDzI+3k/DUGM73G2bAOkPhlNmiQqC8UIXG8w1s6rTFL16TqHByEOM9iaiH0wG5DKlg==; DUID=u=2041E8DE85BE682BF98BB0A86DD98032DD326BDF5E490B5584FF350B64DBD95C&v=0; IsNonUser=F; UUID=2F6E441BBB254CEA9EA80C8DDFE4EAB1; IsPersonalizedLogin=F; nfes_isSupportWebP=1; _gid=GA1.2.338709549.1623299508; MKT_Pagesource=PC; HotelCityID=2split%E4%B8%8A%E6%B5%B7splitShanghaisplit2021-6-10split2021-06-11split0; MKT_CKID_LMT=1623385994389; _RF1=183.217.154.116; intl_ht1=h4=111_55476058,32_6515791,32_1642814,32_426753,32_26539614,32_40363314; hotel=55476058; librauuid=5oZmuX34bDaOug4L; _bfa=1.1622722871475.ziedy.1.1623385988687.1623401889519.11.207.102002; _bfs=1.42; _uetsid=c3a51250c9a411eb9f83ff4aff0a99ce; _uetvid=ff7952d0c46611eb877efdefa380da7d; _jzqco=%7C%7C%7C%7C1623385994619%7C1.299949378.1622722874109.1623403553281.1623403604394.1623403553281.1623403604394.0.0.0.129.129; __zpspc=9.10.1623399431.1623403604.41%232%7Cwww.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; _bfi=p1%3D102002%26p2%3D102002%26v1%3D207%26v2%3D206',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}
url = 'https://m.ctrip.com/restapi/soa2/14605/gethotelcomment'
wb = workbook.Workbook()  # excel表格
ws = wb.active  # 表头
ws.append(['酒店名字', '用户id', '评论者', '评分', '入住时间', '发布时间', '入住目的', '房间', '内容', ])


def respoonse_data():
    for i in range(1, 4):  # 酒店翻页
        response = requests.get(start_url.format(i), headers=headers).text
        # print(response)
        hotelId_list = re.findall('"hotelId":(.*?),', response)  # 酒店id
        hotelNames = re.findall('"hotelName":"(.*?)","hotelId"', response)  # 酒店名字
        for hotelName, hotelId in zip(hotelNames, hotelId_list):
            print(hotelName, hotelId)
            response_pin(hotelName, hotelId)
def response_pin(hotelName,hotelId):
        for i in range(1, 5):#评论翻页
            head = {"cid": "09031092319319629941", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                    "syscode": "09", "auth": "", "xsid": "", "extension": []}
            data = {"hotelId": hotelId, "pageIndex": i, "tagId": 0, "pageSize": 20, "groupTypeBitMap": 2,
                    "needStatisticInfo": 0, "order": 0, "basicRoomName": "", "travelType": 1, "head": head}
            headers1 = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36',
            }
            response = requests.post(url=url, headers=headers1, json=data).json()
            # print(response)
            othersCommentList = response['othersCommentList']

            for CommentList in othersCommentList:
                # print(CommentList)

                content = CommentList['content'].replace('\n', '')  # 评论内容
                userNickName = CommentList['userNickName']  # 名字
                ids = CommentList['id']
                travelType = CommentList['travelType']  # 入住目的
                checkInDate = CommentList['checkInDate']  # 入住时间
                postDate = CommentList['postDate']  # 发布时间
                try:
                    baseRoomName = CommentList['baseRoomName']  # 房间类型
                except:
                    baseRoomName = ' '
                ratingPoint = CommentList['ratingPoint']  # 评分
                #userCommentCount = CommentList['userCommentCount']  # 点评数
                #ratingPointDesc = CommentList['ratingPointDesc']
                print(hotelName, ids, userNickName, ratingPoint, checkInDate, postDate, travelType, baseRoomName, content,
                      sep=' | ')
                ws.append([hotelName, ids, userNickName, ratingPoint, checkInDate, postDate, travelType, baseRoomName, content,])
def xlsx():
    wb.save('评论.xlsx')
if __name__ == '__main__':
    respoonse_data()
    xlsx()