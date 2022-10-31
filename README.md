# project_slack_lunchbot
**전경련회관 지하 1층에는** **구내 식당** 이 있는데, 물가가 오른 탓인지 요새 메뉴 복불복이 심해져서😮‍💨 점심 메뉴를 미리 확인한 후 구내식당에 가고는 합니다. 구내식당 메뉴표는 매주 월요일, 영양사님께로부터 직접 메일로 전달받는데 매번 메일을 확인하는 게 번거로운 관계로 자동으로 식단표를 받아볼 수는 없을까 하는 고민이 들었습니다.

![2022-10-28_12-08-29.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/192926a3-5e87-4130-b0e9-a503256b9777/2022-10-28_12-08-29.png)

사내에서 사용하는 메시저로 **슬랙** 을 사용하기도 하거니와 사내 구성원들과 함께 메뉴를 공유할 수 있기에 슬랙 채널을 통해서 그 날 식단표를 직접 받아보기로 결정하였습니다.

# 구성 프로세스

프로세스는 다음과 같이 구성하였습니다.

1. 메일로 받은 사진을 분석해서 **식단표에서 텍스트를 추출** 한다.
    
    [[Python] 이미지**에서 테이블 추출**](https://www.notion.so/Python-afa66d47bede4d538c0890b631c670db)
    
2. 추출한 **텍스트를 슬랙봇을 통해서 전송** 한다.
    
    [슬랙 API를 이용한 Slack Bot 생성](https://www.notion.so/API-Slack-Bot-7175ca21f1e445d88a7b08c7ff611caf)
    
3. 위의 작업들을 **GitHub Actions 을 이용하여 자동화** 한다.
    
    [**GitHub Actions 을 이용한 배포 자동화**](https://www.notion.so/GitHub-Actions-2b2ecc24f9074abd8f16d23eba41d989)
    

# 결과

슬랙봇이 매일 아침 10시 30분에 통해서 점심 식단표를 다음과 같이 전송합니다.

![2022-10-28_14-53-52.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3036ea75-e901-4975-849e-9e5cbcb0066f/2022-10-28_14-53-52.png)
