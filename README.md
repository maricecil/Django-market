
# 1. 개요
- 프로젝트명: 학교마켓, 중고 학교용품 거래 플랫폼
- 개발기간: 2024.12.16 ~ 2024.12.27(10일간)

## 1.1 목적:
- 학생들의 중고 교복, 교재, 학용품 거래를 위한 온라인 플랫폼 구축
- 검증된 사용자가 상품을 등록하고, 검색하고, "좋아요"를 표시
- 다른 판매자를 팔로우하여 상품을 추적할 수 있는 마켓플레이스 역할 

## 1.2 대상:
- 중고 교복/교재/학용품을 거래하려는 학생
- 자녀의 학교용품을 구매/판매하려는 학부모
- 학교 커뮤니티 구성원

## 1.3 목표:
- 안전하고 원활한 사용자 등록 및 로그인 경험 제공
- 필수 사용자 정보를 담은 간단한 프로필 페이지 제공
- 카테고리별 상품 등록 및 검색 기능 제공
- 기본적인 소셜 상호 작용 활성화 (팔로우, 좋아요)


# 2. 사용자 흐름
비로그인 상태에서도 상품을 볼 수 있으나 프로필 및 상품등록, 찜하기, 채팅하기 기능은 로그인하여 사용할 수 있습니다. 

## 2.1 가입/로그인:
회원가입을 클릭한 후 이메일, 사용자 이름, 비밀번호를 입력합니다. 등록이 성공적으로 완료되면 사용자는 메인 페이지로 리디렉션됩니다.

## 2.2 프로필 페이지:
사용자 이름, 사진, 지역 및 학교정보, 개인 정보를 선택적으로 저장할 수 있고, 프로필에 반영됩니다. 

## 2.3 상품 등록 페이지:
- 카테고리와 상태, 사이즈, 거래방법을 선택할 수 있고, 상품명과 가격, 설명, 사진을 등록할 수 있습니다. 
- 상품을 등록하면 같은 페이지에서 내가 등록한 상품을 확인할 수 있습니다. 
  
## 2.4 관심 상품 페이지:
- 찜하기를 누른 상품이 저장되고, 거래가 완료된 상품은 거래 완료라고 표시되어 있습니다. 
- 같은 페이지에서 채팅 목록을 확인할 수 있습니다. 거래가 완료되면 판매자만 거래완료 버튼을 누를 수 있고, 채팅에 참여한 구매자만 후기를 등록할 수 있습니다.

## 2.5 상품 세부 정보 페이지:
- 상품 등록 페이지에서 설정한 이미지, 상태, 사이즈, 거래방법과 설명이 로드 됩니다. 
- 찜하기를 누르면 장바구니에 추가되고, 채팅하기를 누르면 채팅 창에서 대화를 시작할 수 있습니다.
- 프로필 페이지에서 등록한 판매자 정보가 표시됩니다. 팔로워, 팔로잉 수가 표시되어 있고, 스스로를 팔로잉 할 수는 없습니다. 팔로우를 클릭하면 사용자가 목록에 추가되고, 팔로우 수가 증가합니다.
- 판매자와 거래한 모든 거래 후기가 표시됩니다.
- 판매자가 등록한 다른 상품도 확인할 수 있습니다. 
- 등록된 상품을 수정하거나 삭제할 수 있습니다.

## 2.6 메인 페이지:
- 로그인 전 최상단의 헤더에는 회원가입과 로그인 버튼이 있고, 로그인 후에는 로그아웃 버튼만 보입니다. 
- 검색창과 찜하기, 상품등록, 마이페이지 버튼을 통해 쉽게 상품을 검색하고 관리할 수 있습니다. 
- 필터를 통해 더욱 쉽고 빠르게 원하는 상품을 거래할 수 있습니다.


# 3. 주요 기능
## 3.1 사용자 계정 기능
- 가입: 이메일, 사용자 이름, 비밀번호 필수
- 로그인/로그아웃: 표준 Django 인증
- 프로필 페이지:
  * 사용자 이름과 등록 날짜
  * 판매/찜한 상품 목록
  * 팔로워/팔로잉 수
  * 프로필 이미지(선택)
  * 채팅 목록 및 알림

## 3.2 상품 관리 기능
- 카테고리:
  * 교복 (동복/하복/체육복/생활복/엑세서리)
  * 교재 (교과서/참고서/문제집)
  * 학용품 (필기구/문구류/체육용품/미술용품/음악용품/기타학습도구)
- 상품 등록:
  * 카테고리 선택
  * 제목/설명
  * 가격
  * 상태 (새상품/중고)
  * 대표 이미지 1장 (선택: 추가 이미지)
  * 조회수, 찜하기 수 표시
- 상품 수정/삭제
- 상품 검색:
  * 카테고리별 보기
  * 키워드 검색 (상품명, 학교명)
  * 기본 정렬 (최신순/가격순)

## 3.3 소셜 기능
- 찜하기: 관심 상품 저장
- 팔로우: 판매자 팔로우/언팔로우
- 채팅: 상품별 1:1 채팅
- 리뷰: 판매자 리뷰 작성

## 3.4 알림 기능
- 새로운 메시지 알림
- 읽지 않은 메시지 카운트
- 상품별 메시지 관리
  
## 3.5 권한 관리
- 비로그인 사용자:
  * 랜딩 페이지만 접근 가능
  * 로그인 필요 안내
- 로그인 사용자:
  * 전체 기능 사용 가능
  * 자신의 상품만 수정/삭제 가능


# 4. 기술 스택
- 백엔드 프레임워크: 
  - Django: 강력하고 빠른 서버 측 개발
  - 기본 Django 인증 시스템
  - Pillow: 이미지 처리
  - SQLite(개발) / PostgreSQL(배포)

- 프런트엔드:
  - Django 템플릿: 서버 사이드 렌더링
  - TailwindCSS: 유틸리티 중심의 CSS 프레임워크
  - 최소한의 JavaScript: 필요한 경우에만 사용

- Django를 사용하여 사용자 인증, 데이터베이스 마이그레이션 및 CRUD 작업을 신속하게 처리하도록 했습니다.
- Django 템플릿과 TailwindCSS를 사용하여 깔끔한 반응형 UI를 빠르게 구현했습니다.

Django==5.0
Pillow==10.1.0
python-dotenv==1.0.0
django-tailwind==3.8.0
django-browser-reload==1.12.1
django-compressor==4.4
django-htmx==1.17.2
whitenoise==6.6.0
gunicorn==21.2.0
psycopg2-binary==2.9.9  

# 5. 향후 개선 계획
아직까지 구현되지 못한 기능들을 구현하여 완성도를 높이고자 합니다.
- 첫 접속시 로그아웃상태
- 좋아요 취소 기능
- 채팅창 유저별 관리
- 채팅창 페이지 신설
- 상단 알림기능
- 무한스크롤
- 검색 및 필터기능
- 지역api
![과제ERD](https://github.com/user-attachments/assets/0bd7c16f-abea-48b0-96fb-698d8b5fc4ff)
