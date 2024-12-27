# Django의 앱 설정을 위한 AppConfig를 가져옴
from django.apps import AppConfig

# accounts 앱의 설정을 담당하는 클래스
class AccountsConfig(AppConfig):
    # 데이터베이스 필드의 기본 타입 설정
    default_auto_field = 'django.db.models.BigAutoField'
    # 앱의 이름 설정
    name = 'accounts'
    
    # 앱이 준비되었을 때 실행되는 메서드
    def ready(self):
        import accounts.signals  # 시그널 파일을 불러와서 등록함
        # 시그널은 특정 이벤트(예: 사용자 생성)가 발생했을 때 
        # 자동으로 다른 작업(예: 프로필 생성)을 실행하게 해주는 기능임