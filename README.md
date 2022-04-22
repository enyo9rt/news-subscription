# news-subscription
## 팀명
하모니(Harmony)
## 참여 인원
- 팀장: 문현준
- 팀원: 김예진
- 팀원: 최찬혁
- 비고: 성원준(하차)
## 프로젝트 개요
본인이 관심있어 하는 카테고리의 뉴스가 포털 등에 업데이트 되었을 때 구독자가 희망하는 시간에 구독자의 이메일로 알림을 보내주는 서비스
## 기능 소개
1. 네이버의 뉴스 크롤링 및 카드 뷰에 배치<br><br>
   네이버 뉴스에서 일부를 크롤링하여 웹 사이트에 카드 뷰 형식으로 나타냄.<br><br>
2. 날씨 API를 사용하여 현재 위치 날씨 정보 제공<br><br>
   openweathermap 오픈 API 및 Google geolocation API를 통해 사용자 현재 위치 기반 날씨 정보를 가져와 웹 페이지에서 표시함.<br><br>
3. 각 뉴스 클릭 시 상세 페이지 이동 및 댓글, 좋아요 기능 추가<br><br>
   각 뉴스를 클릭하면 상세 페이지를 띄우고 댓글, 좋아요 기능을 할 수 있게 함.<br>(미니 프로젝트 단계에서는 각 뉴스 상세페이지가 아닌 고정 페이지로 이동하는 것에 초점을 맞춤)<br><br>
4. 메일 전송 시스템<br><br>
   - 회원가입 시 완료 알림 이메일 발송
   - 뉴스 구독 시 구독 완료 알림 메일 전송<br><br>
5. 로그인
## 사용 API 
|기능|Method|URL|request|response|
|:----:|:---:|:-----:|:-----:|:-----:|
|뉴스 목록 전체 조회|GET|/api/posts||뉴스 목록 리스트|
|뉴스 상세 페이지|GET|/api/posts/{id}|{'post_id':post_id}|뉴스 상세 페이지 이동|
|댓글작성|POST|/api/comment|{'comments':comments}|DB 저장결과|
|로그인|GET|/api/login||로그인 페이지|
|로그인|POST|/api/login|{'email':email, 'password':password}|로그인 결과|
|회원가입|GET|/api/register||회원가입 페이지|
|회원가입|POST|/api/register|{'email':email, 'password':password}|회원가입 결과|
|날씨 & 현재 위치 조회|GET|/api/weather||날씨와 현재 위치 정보 획득|
