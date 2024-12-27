# 필요한 Django 기능들을 가져옵니다
from django.db import models  # 데이터베이스 모델 관련 기능
from django.contrib.auth.models import AbstractUser  # Django의 기본 사용자 모델
from django.conf import settings  # Django 프로젝트의 설정값들
from django.db.models.signals import post_save  # 데이터 저장 후 자동으로 실행될 기능
from django.dispatch import receiver  # signal 수신용 데코레이터
from PIL import Image  # 프로필 이미지 처리용 라이브러리

# 기본 User 모델을 확장한 커스텀 사용자 모델
class User(AbstractUser):
    # 사용자가 가입한 시간을 자동으로 저장
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Django의 기본 그룹 시스템과의 충돌을 피하기 위해 related_name 변경
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # 기존 'user_set'과 구분하기 위한 이름
        blank=True,  # 필수 입력 아님
        help_text='사용자가 속한 그룹들',
        verbose_name='그룹',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # 기존 'user_set'과 구분하기 위한 이름
        blank=True,  # 필수 입력 아님
        help_text='사용자의 권한들',
        verbose_name='사용자 권한',
    )
    
    following = models.ManyToManyField(
        'self',
        through='Follow',
        related_name='followers',
        symmetrical=False
    )
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username  # 사용자 객체를 문자열로 표현할 때는 사용자명 반환

# 사용자의 추가 정보를 저장하는 프로필 모델
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]
    
    # User 모델과 1:1 연결 (한 사용자당 하나의 프로필)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True  # user 필드를 primary key로 유지
    )
    
    # 프로필에 필요한 추가 정보들
    location = models.CharField(max_length=100, blank=True, verbose_name='지역')  # 거주 지역
    school = models.CharField(max_length=100, blank=True, verbose_name='학교')    # 학교 이름
    department = models.CharField(max_length=100, blank=True, verbose_name='학과')  # major를 department로 변경
    height = models.IntegerField(null=True, blank=True, verbose_name='키')       # 키 (cm)
    weight = models.IntegerField(null=True, blank=True, verbose_name='몸무게')    # 몸무게 (kg)
    usual_size = models.CharField(
        max_length=2, 
        choices=SIZE_CHOICES, 
        blank=True,   # 폼에서 빈 값 허용
        null=True     # 데이터베이스에서 NULL 허용
    )
    bio = models.TextField(blank=True, verbose_name='인사말')  # 자기소개
    
    # 프로필 이미지 필드
    profile_image = models.ImageField(
        upload_to='profiles/',  # 이미지는 media/profiles/ 폴더에 저장
        blank=True,  # 필수 아님
        null=True,   # 데이터베이스에서 NULL 허용
        help_text='권장 크기: 300x300px, 최대 2MB'  # 관리자 페이지에서 보이는 도움말
    )
    
    # 학년 선택 필드 (1~3학년)
    grade = models.CharField('학년', max_length=10, blank=True, null=True)
    
    # 판매자 평가 관련 필드들
    rating = models.DecimalField(
        max_digits=3,      # 최대 3자리 숫자
        decimal_places=1,  # 소수점 1자리
        default=0.0,       # 기본값 0.0
        verbose_name='평점'
    )
    review_count = models.IntegerField(
        default=0,
        verbose_name='리뷰 수'
    )
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)  # 성별 필드 추가
    
    # 개별 공개 설정을 섹션별 공개 설정으로 변경
    is_school_info_public = models.BooleanField('학교 정보 공개', default=True)
    is_personal_info_public = models.BooleanField('개인 정보 공개', default=True)
    
    # 기존 개별 공개 설정 필드들 제거
    # is_location_public, is_school_public, is_grade_public, is_major_public,
    # is_gender_public, is_size_public, is_height_public, is_weight_public

    def __str__(self):
        return f"{self.user.username}의 프로필"  # 프로필 객체를 문자열로 표현할 때

    class Meta:
        db_table = 'user_profile'  # 실제 데이터베이스 테이블 이름 지정

    # 프로필 이미지 저장 시 자동으로 실행되는 메서드
    def save(self, *args, **kwargs):
        if self.profile_image:
            # 이미지 크기 제한 (2MB)
            if self.profile_image.size > 2*1024*1024:  # 바이트 단위로 2MB 계산
                raise ValueError("이미지 크기는 2MB를 초과할 수 없습니다.")
            
            # 큰 이미지 자동 리사이징
            img = Image.open(self.profile_image)
            if img.height > 300 or img.width > 300:  # 300px 초과 시
                output_size = (300, 300)
                img.thumbnail(output_size)  # 비율 유지하며 크기 조정
                img.save(self.profile_image.path)  # 원본 파일 덮어쓰기
        
        super().save(*args, **kwargs)  # 원래의 저장 동작 실행

# 팔로우 관계를 저장하는 모델
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_relations')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_relations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and not Profile.objects.filter(user=instance).exists():
#         Profile.objects.create(user=instance)
