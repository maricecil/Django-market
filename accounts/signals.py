# Django의 signal과 receiver 기능을 가져옵니다
from django.db.models.signals import post_save  # 데이터가 저장된 후 실행되는 신호
from django.dispatch import receiver  # signal을 받아서 처리하는 데코레이터
from django.apps import apps  # Django 앱 관련 기능
from .models import User, Profile  # 우리가 만든 사용자와 프로필 모델

# 사용자가 생성될 때 자동으로 프로필을 생성하는 함수
@receiver(post_save, sender=User)  # User 모델이 저장될 때 이 함수를 실행하라는 의미
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # 새로운 사용자가 생성된 경우에만
        Profile.objects.create(user=instance)  # 해당 사용자의 프로필을 생성

# 사용자 정보가 저장될 때마다 프로필도 함께 저장하는 함수
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):  # 프로필이 없는 경우
        Profile.objects.create(user=instance)  # 새로 생성
    instance.profile.save()  # 프로필 정보 저장