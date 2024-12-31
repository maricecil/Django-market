# 스쿨마켓 REST API 문서

## Base URL
- Development: `http://localhost:8000/api/v1/`
- Production: `https://schoolmarket.com/api/v1/` 

## 공통 사항
### 인증
- 인증이 필요한 요청에는 Authorization 헤더 필요
- Format: `Authorization: Token {token}`

### 응답 형식
- 성공: HTTP 200/201 + 데이터
- 실패: HTTP 4XX/5XX + 에러메시지

## API 목록

### 1. 사용자(Accounts)

| Method | Endpoint | 설명 | 인증필요 |
|--------|----------|------|-----------|
| POST | /accounts/signup/ | 회원가입 | X |
| POST | /accounts/login/ | 로그인 | X |
| GET | /accounts/profile/<username>/ | 프로필 조회 | O |
| PUT | /accounts/profile/ | 프로필 수정 | O |
| POST | /accounts/<username>/follow/ | 팔로우/언팔로우 | O |

### 2. 상품(Products) 

| Method | Endpoint | 설명 | 인증필요 |
|--------|----------|------|-----------|
| GET | /products/ | 상품 목록 조회 | X |
| GET | /products/<id>/ | 상품 상세 조회 | X |
| POST | /products/ | 상품 등록 | O |
| PUT | /products/<id>/ | 상품 수정 | O |
| DELETE | /products/<id>/ | 상품 삭제 | O |
| POST | /products/<id>/like/ | 찜하기/취소 | O |

### 3. 메시지(Messages)

| Method | Endpoint | 설명 | 인증필요 |
|--------|----------|------|-----------|
| GET | /messages/<product_id>/ | 메시지 목록 조회 | O |
| POST | /messages/<product_id>/ | 메시지 전송 | O |

### 4. 소셜(Social)

#### 찜하기/취소
POST /api/products/<id>/like/
Response (200):
{
    "is_liked": true,
    "likes_count": 6
}

#### 팔로우/언팔로우
POST /api/accounts/<username>/follow/
Response (200):
{
    "is_following": true,
    "followers_count": 42
}

## API 상세

### 1. 사용자(Accounts)

#### 회원가입

http
POST /api/accounts/signup/

Request:
json
{
"username": "string",
"email": "string",
"password": "string",
"profile_image": "file (optional)"
}

Response (201):
json
{
"id": 1,
"username": "user1",
"email": "user1@example.com",
"created_at": "2024-01-01T00:00:00Z"
}

#### 로그인
http
POST /api/accounts/login/
Request:
json
{
"username": "string",
"password": "string"
}

Response (200):
json
{
"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
"user": {
"id": 1,
"username": "user1"
}
}

#### 프로필 조회
GET /api/accounts/profile/<username>/
Response (200):
{
    "username": "user1",
    "email": "user1@example.com",
    "profile_image": "url",
    "created_at": "2024-01-01T00:00:00Z",
    "products": [
        {
            "id": 1,
            "name": "교복 상의",
            "price": 30000,
            "image": "url"
        }
    ],
    "followers_count": 42,
    "following_count": 38
}

#### 프로필 수정
PUT /api/accounts/profile/
Request:
{
    "email": "string",
    "profile_image": "file",
    "password": "string (optional)"
}
Response (200):
{
    "username": "user1",
    "email": "new@example.com",
    "profile_image": "url"
}

### 2. 상품(Products)

#### 상품 목록 조회
GET /api/products/

Query Parameters:
- category: string (교복/교재/학용품)
- subcategory: string (동복/하복/체육복 등)
- condition: string (new/used)
- min_price: integer
- max_price: integer
- sort: string (latest/price_asc/price_desc)
- search: string (검색어)
- page: integer (기본값: 1)
- size: integer (기본값: 10)

Response (200):
json
{
"count": 100,
"next": "/api/products/?page=2",
"previous": null,
"results": [
{
"id": 1,
"name": "교복 상의",
"price": 30000,
"category": "uniform",
"image": "url",
"likes_count": 5,
"seller": {
"username": "user1"
}
}
]
}

#### 상품 상세 조회
GET /api/products/<id>/
Response (200):
{
    "id": 1,
    "name": "교복 상의",
    "description": "2023년 구매한 동복입니다",
    "price": 30000,
    "category": "uniform",
    "condition": "used",
    "image": "url",
    "additional_images": ["url1", "url2"],
    "seller": {
        "username": "user1",
        "profile_image": "url"
    },
    "likes_count": 5,
    "is_liked": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}

#### 상품 등록
http
POST /api/products/

Request:
json
{
"name": "string",
"description": "string",
"price": 0,
"category": "uniform",
"condition": "new",
"image": "file"
}

Response (201):
json
{
"id": 1,
"name": "교복 상의",
"price": 30000,
"created_at": "2024-01-01T00:00:00Z"
}

#### 상품 수정
PUT /api/products/<id>/
Request:
{
    "name": "string",
    "description": "string",
    "price": 0,
    "category": "uniform",
    "condition": "new",
    "image": "file (optional)"
}
Response (200):
{
    "id": 1,
    "name": "교복 상의",
    "price": 30000,
    "updated_at": "2024-01-01T00:00:00Z"
}


### 3. 메시지(Messages)

#### 메시지 전송
http
POST /api/messages/1/

http
POST /api/messages/1/
Request:

json
{
"content": "string"
}

Response (201):
json
{
"id": 1,
"content": "안녕하세요",
"created_at": "2024-01-01T00:00:00Z",
"is_read": false
}

#### 메시지 목록 조회
GET /api/messages/<product_id>/
Response (200):
{
    "product": {
        "id": 1,
        "name": "교복 상의"
    },
    "messages": [
        {
            "id": 1,
            "sender": "user1",
            "content": "안녕하세요",
            "created_at": "2024-01-01T00:00:00Z",
            "is_read": true
        }
    ]
}

## 상태 코드

| 코드 | 설명 |
|------|------|
| 200 | 성공 |
| 201 | 생성 성공 |
| 400 | 잘못된 요청 |
| 401 | 인증 필요 |
| 403 | 권한 없음 |
| 404 | 리소스 없음 |
| 500 | 서버 에러 |

### 에러 응답
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "에러 메시지",
        "details": {} // 추가 정보
    }
}
```

주요 에러 코드:
- INVALID_INPUT: 잘못된 입력값
- NOT_FOUND: 리소스를 찾을 수 없음
- UNAUTHORIZED: 인증 필요
- FORBIDDEN: 권한 없음
- SERVER_ERROR: 서버 오류

## API 테스트
### Swagger UI
- URL: `http://localhost:8000/swagger/`
- 브라우저에서 직접 API 테스트 가능
- 모든 엔드포인트의 실시간 문서화 제공

### 설치 방법
```bash
pip install drf-yasg
```

### 사용 방법
1. 브라우저에서 `/swagger/` 접속
2. 우측 상단의 'Authorize' 버튼 클릭
3. 로그인 후 받은 토큰 입력
4. 각 API의 'Try it out' 버튼으로 테스트