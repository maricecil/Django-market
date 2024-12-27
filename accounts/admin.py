# Django의 관리자 페이지 관련 모듈들을 임포트합니다
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Django의 기본 User 관리 클래스
from .models import User, Profile, Follow  # 우리가 만든 커스텀 모델들

# Profile 모델을 User admin 페이지 내에 함께 표시하기 위한 인라인 클래스
class ProfileInline(admin.StackedInline):
    model = Profile  # Profile 모델을 인라인으로 표시
    can_delete = False  # Profile 삭제 비활성화 (User와 1:1 관계이므로 삭제하면 안됨)
    verbose_name = '프로필'  # 관리자 페이지에서 표시될 단수 이름
    verbose_name_plural = '프로필'  # 관리자 페이지에서 표시될 복수 이름

# User 모델을 관리하기 위한 커스텀 관리자 클래스
@admin.register(User)  # User 모델에 이 관리자 클래스를 등록하는 데코레이터
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)  # User 편집 페이지에 Profile 정보도 함께 표시
    list_display = ['username', 'email', 'created_at']  # 목록 페이지에서 보여줄 필드들
    list_filter = ['created_at']  # 우측에 필터 옵션으로 사용할 필드
    search_fields = ['username', 'email']  # 검색창에서 검색 가능한 필드들
    ordering = ['-created_at']  # 생성일 기준 내림차순 정렬 (최신순)

# Follow 모델을 관리하기 위한 관리자 클래스
@admin.register(Follow)  # Follow 모델에 이 관리자 클래스를 등록하는 데코레이터
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']  # 목록에서 보여줄 필드들
    list_filter = ['created_at']  # 필터 옵션
    search_fields = ['follower__username', 'following__username']  # 사용자명으로 검색 가능
    date_hierarchy = 'created_at'  # 날짜 기반 계층적 탐색 기능 활성화
    ordering = ['-created_at']  # 생성일 기준 내림차순 정렬

# Profile 모델을 기본 관리자 인터페이스로 등록
admin.site.register(Profile)  # Profile 모델에 대한 기본 관리자 인터페이스 사용