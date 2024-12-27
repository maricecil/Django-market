from django.urls import path  # URL 패턴을 정의하는데 필요한 path 함수
from . import views  # 현재 앱의 views.py 파일에서 뷰 함수들을 가져옴

# URL namespace 설정 - 다른 앱과의 URL 이름 충돌을 방지
# 사용할 때는 'accounts:login' 같은 형식으로 사용
app_name = 'accounts'

# URL 패턴 목록
urlpatterns = [ 
    path('signup/', views.SignUpView.as_view(), name='signup'), # 회원가입 페이지
    path('login/', views.CustomLoginView.as_view(), name='login'),  # 로그인 페이지
    path('logout/', views.logout_view, name='logout'), # 로그아웃
    path('mypage/', views.mypage_redirect, name='mypage'),  # 마이페이지 (프로필 관리)
    path('follow/<int:user_id>/', views.follow_toggle, name='follow_toggle'), # 팔로우/언팔로우 기능
    path('profile/<int:pk>/', views.profile_view, name='profile'),  # 통합된 프로필 뷰
    path('profile/update/', views.profile_update, name='profile_update'),  # 추가
    path('privacy/', views.toggle_privacy, name='toggle_privacy'),
    path('<int:user_id>/follow/', views.toggle_follow, name='toggle_follow'),
    path('follow-list/<str:type>/<int:user_id>/', views.follow_list, name='follow_list'),
] 