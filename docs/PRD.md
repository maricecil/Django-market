# 중고 학교용품 거래 장터 제품요구사항 문서(PRD)

## 1. 프로젝트 개요

프로젝트명: 학교마켓 - 중고 학교용품 거래 플랫폼 (MVP)

목적:
학생들의 중고 교복, 교재, 학용품 거래를 위한 최소한의 완전한 기능을 갖춘 온라인 플랫폼을 만드는 것입니다. 검증된 사용자가 상품을 등록하고, 검색하고, "좋아요"를 표시할 수 있을 뿐만 아니라 다른 판매자를 팔로우하여 상품을 추적할 수 있는 마켓플레이스 역할을 합니다.

대상:
- 중고 교복/교재/학용품을 거래하려는 학생
- 자녀의 학교용품을 구매/판매하려는 학부모
- 학교 커뮤니티 구성원

목표:
- 안전하고 원활한 사용자 등록 및 로그인 경험 제공
- 필수 사용자 정보를 담은 간단한 프로필 페이지 제공
- 카테고리별 상품 등록 및 검색 기능 제공
- 기본적인 소셜 상호 작용 활성화 (팔로우, 좋아요)


##2. 사용자 흐름
고급 사용자 여정
1. 랜딩페이지(비로그인 상태):
사용자에게는 브랜딩과 간단한 지침이 포함된 최소한의 홈페이지가 표시됩니다.
마켓플레이스에 액세스하려면 "가입" 또는 "로그인"하라는 메시지가 표시됩니다.

2. 가입/로그인:
회원가입을 클릭한 후 이메일, 사용자 이름, 비밀번호를 입력합니다.
등록이 성공적으로 완료되면 사용자는 프로필 페이지로 리디렉션됩니다.
로그인 시 사용자 인증을 거쳐 메인 아이템 목록 페이지로 리디렉션됩니다.

3. 프로필 페이지(로그인 상태):
사용자 이름, 등록 날짜, 사용자가 나열한 항목 및 "원함"(즐겨찾기)으로 표시한 항목이 표시됩니다.
다른 사용자의 프로필을 팔로우/언팔로우할 수 있는 옵션과 함께 팔로어 및 팔로어 수를 표시합니다.
계정 세부정보를 수정하거나 로그아웃할 수 있는 링크입니다.

4. 항목 목록 페이지:
로그인하면 사용자는 간단하고 스크롤 가능한 목록 형식으로 항목을 찾아볼 수 있습니다.
검색창은 학교 이름, 사이즈, 교복 종류 등 키워드별로 항목을 필터링하기 위해 상단에 제공됩니다.
각 항목 항목에는 썸네일, 제목 및 "좋아요" 수가 표시됩니다.

5. 항목 세부정보 페이지:
이미지, 설명, 크기, 상태, 가격, 판매자 이름 등 전체 항목 세부 정보를 표시합니다.
사용자가 해당 아이템을 원하거나 저장하려는 경우 '좋아요' 버튼이 표시됩니다.
현재 사용자가 항목의 소유자인 경우 항목을 편집하거나 삭제할 수 있습니다.

6. 상품 관리(판매자용):
프로필 페이지 또는 전용 "내 아이템" 섹션에서 사용자는 새 아이템 목록을 생성할 수 있습니다(이미지 업로드, 설명 입력 등).
사용자는 상세페이지 또는 관리페이지에서 자신의 목록을 편집하거나 삭제할 수 있습니다.

7. 팔로잉 사용자:
다른 사용자의 프로필 페이지에서는 '팔로우' 버튼을 사용할 수 있습니다.
"팔로우"를 클릭하면 해당 사용자가 팔로우 목록에 추가됩니다. 팔로우 수가 증가합니다.

8. 로그아웃:
프로필 페이지에서 사용자는 로그아웃하고 랜딩 페이지로 돌아갈 수 있습니다.


## 3. 핵심 기능
1. 사용자 계정 기능
- 가입: 이메일, 사용자 이름, 비밀번호 필수
- 로그인/로그아웃: 표준 Django 인증
- 프로필 페이지:
  * 사용자 이름과 등록 날짜
  * 판매/찜한 상품 목록
  * 팔로워/팔로잉 수
  * 프로필 이미지(선택)
  * 채팅 목록 및 알림

2. 상품 관리 기능
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

3. 소셜 기능
- 찜하기: 관심 상품 저장
- 팔로우: 판매자 팔로우/언팔로우
- 채팅: 상품별 1:1 채팅
- 리뷰: 판매자 리뷰 작성

4. 알림 기능
- 새로운 메시지 알림
- 읽지 않은 메시지 카운트
- 상품별 메시지 관리
  
5. 권한 관리
- 비로그인 사용자:
  * 랜딩 페이지만 접근 가능
  * 로그인 필요 안내
- 로그인 사용자:
  * 전체 기능 사용 가능
  * 자신의 상품만 수정/삭제 가능


## 4. 기술 스택
필수의:
- 백엔드 프레임워크: 
  - Django: 강력하고 빠른 서버 측 개발
  - 기본 Django 인증 시스템
  - Pillow: 이미지 처리
  - SQLite(개발) / PostgreSQL(배포)

- 프런트엔드:
  - Django 템플릿: 서버 사이드 렌더링
  - TailwindCSS: 유틸리티 중심의 CSS 프레임워크
  - 최소한의 JavaScript: 필요한 경우에만 사용

이론적 해석:
- Django: 사용자 인증, 데이터베이스 마이그레이션 및 CRUD 작업을 신속하게 처리
- Django 템플릿 + TailwindCSS: 깔끔하고 반응형 UI를 빠르게 구현


## 5. MVP 이후 추가 개선 사항
MVP가 안정적이고 핵심 기능이 검증되면 다음 개선 사항을 고려하세요.
1. 고급 검색 및 필터:
가격, 규모, 브랜드 또는 학교별로 정렬하는 카테고리 기반 필터링을 추가하세요.
2. 사용자 간 메시지:
구매 전 확인을 위한 직접 메시지 또는 Q&A 섹션(나중에 구매 기능을 추가하는 경우)
3. 알림 시스템:
새로운 팔로어, 항목 좋아요 또는 저장된 항목 업데이트에 대한 인앱 또는 이메일 알림입니다.
4. 향상된 사용자 프로필:
- 프로필 맞춤 옵션(프로필 사진, 소개 등)을 추가하세요.
- 최근 활동이나 권장 사항을 표시합니다.
5. 검증 및 신뢰 기능:
신뢰도를 높이기 위한 사용자 확인, 검토 또는 평가 시스템.
6. 현지화 및 국제화:
단일 지역 이상으로 확장하는 경우 여러 언어 및 통화 형식을 지원합니다.
7. 응답성 향상:
모바일 및 태블릿 보기를 더욱 개선하여 여러 장치에서 유연한 경험을 보장합니다.


요약
이 PRD는 중고 교복 거래 플랫폼의 핵심 시스템을 간략하게 설명합니다. MVP는 Django, ShadCN 및 TailwindCSS를 통해 구현된 간단한 UI 내에서 사용자 인증, 프로필 보기, 항목 CRUD 작업, 기본 검색, "좋아요" 및 팔로우 기능 등 최소한의 기능 세트에 중점을 둡니다. 향후 개선으로 복잡성이 추가되고 사용자 경험이 향상될 수 있지만, 초기 목표는 원활하게 작동하고 사용하기 쉬운 안정적이고 핵심적인 제품을 구축하는 것입니다.