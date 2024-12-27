# 필요한 Django 기능들을 가져옵니다
from django.shortcuts import render, redirect, get_object_or_404  # 페이지 표시, 이동, 객체 조회
from django.contrib.auth import login as auth_login  # 로그인 처리
from django.contrib.auth import logout as auth_logout  # 로그아웃 처리
from django.contrib.auth.decorators import login_required  # 로그인 필요 표시
from django.http import JsonResponse  # AJAX 응답용
from django.views.decorators.http import require_POST  # POST 요청만 허용
from django.contrib.auth import get_user_model  # 현재 사용중인 User 모델 가져오기
from .models import Follow, Profile  # Profile 모델 추가
from products.models import Product  # 상품 모델
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm, CustomAuthenticationForm, ProfileForm  # ProfileForm import 추가
from django.contrib.auth import login
from django.db import transaction
import json  # 상단에 추가

# 함수형 뷰 대신 클래스형 뷰로 변경
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return reverse_lazy('products:home')  # 로그인 후 메인 페이지로 이동

# 로그아웃 처리
def logout_view(request):
    auth_logout(request)  # Django의 로그아웃 기능 사용
    return redirect('products:home')  # 홈페이지로 이동

# 팔로우/언팔로우 토글 (POST 요청만 허용)
@require_POST  # GET 요청 등은 거부
def follow_toggle(request, user_id):
    try:
        target_user = get_user_model().objects.get(id=user_id)
        
        if request.user == target_user:
            return JsonResponse({'error': '자신을 팔로우할 수 없습니다.'}, status=400)
        
        # 팔로우 관계 확인 및 토글
        follow_relation = Follow.objects.filter(
            follower=request.user,
            following=target_user
        )
        
        if follow_relation.exists():
            follow_relation.delete()
            is_following = False
        else:
            Follow.objects.create(
                follower=request.user,
                following=target_user
            )
            is_following = True
            
        return JsonResponse({
            'status': 'success',
            'is_following': is_following,
            'follower_count': target_user.follower_relations.count()
        })
        
    except get_user_model().DoesNotExist:
        return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

# 프로필 상세 페이지 (로그인 필요)
@login_required
def profile_detail(request, user_id):
    User = get_user_model()
    seller = get_object_or_404(User.objects.select_related('profile'), id=user_id)
    
    # POST 요청 처리 (프로필 수정)
    if request.method == 'POST' and request.user == seller:
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile_detail', user_id=user_id)
    else:
        form = ProfileForm(instance=seller.profile) if request.user == seller else None
    
    # privacy 설정 확인
    is_school_info_visible = seller.profile.is_school_info_public or request.user == seller
    is_personal_info_visible = seller.profile.is_personal_info_public or request.user == seller
    
    context = {
        'seller': seller,
        'is_following': Follow.objects.filter(
            follower=request.user, 
            following=seller
        ).exists() if request.user.is_authenticated else False,
        'form': form,
        'is_school_info_visible': is_school_info_visible,
        'is_personal_info_visible': is_personal_info_visible,
    }
    return render(request, 'accounts/profile_detail.html', context)

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:profile', pk=user.id)

@login_required
@require_POST
def toggle_privacy(request):
    data = json.loads(request.body)
    field = data.get('field')
    value = data.get('value')
    
    if field not in ['school_info', 'personal_info']:
        return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)
    
    profile = request.user.profile
    field_name = f'is_{field}_public'
    setattr(profile, field_name, value)
    profile.save()
    
    return JsonResponse({
        'success': True,
        'is_public': value
    })

User = get_user_model()

@login_required
def profile_view(request, pk):
    seller = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST' and request.user == seller:  # 본인만 수정 가능
        try:
            profile = seller.profile
            
            # 디버깅용 출력
            print("POST 데이터:", request.POST)
            print("FILES 데이터:", request.FILES)
            
            # 프로필 이미지 처리
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            
            # 기본 정보 업데이트
            fields_to_update = ['bio', 'location', 'school', 'department', 'gender', 'usual_size']
            for field in fields_to_update:
                if field in request.POST:  # POST에 필드가 있는 경우만 업데이트
                    setattr(profile, field, request.POST.get(field))
            
            # 숫자 필드 처리
            for field in ['grade', 'height', 'weight']:
                value = request.POST.get(field, '').strip()
                setattr(profile, field, int(value) if value else None)
            
            profile.save()
            
            return JsonResponse({
                'status': 'success',
                'profile_data': {
                    'bio': profile.bio,
                    'location': profile.location,
                    'school': profile.school,
                    'grade': profile.grade,
                    'department': profile.department,
                    'gender': profile.gender,
                    'usual_size': profile.usual_size,
                    'height': profile.height,
                    'weight': profile.weight,
                }
            })
            
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    # GET 요청 처리
    context = {
        'seller': seller,
        'sizes': Profile.SIZE_CHOICES,
        'is_following': Follow.objects.filter(
            follower=request.user, 
            following=seller
        ).exists() if request.user.is_authenticated else False,
    }
    return render(request, 'accounts/profile.html', context)

def mypage_redirect(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return redirect('accounts:profile', pk=request.user.id)

@login_required
@require_POST
def profile_update(request):
    try:
        profile = request.user.profile
        
        # 디버깅용 출력 추가
        print("전체 POST 데이터:", request.POST)
        print("사이즈 값:", request.POST.get('usual_size'))
        print("현재 프로필 사이즈:", profile.usual_size)
        
        # 기본 정보 업데이트
        fields_to_update = ['bio', 'location', 'school', 'department', 'gender', 'usual_size']
        for field in fields_to_update:
            value = request.POST.get(field)
            print(f"{field} 업데이트: {value}")  # 각 필드 값 출력
            if value is not None:  # None이 아닌 경우만 업데이트
                setattr(profile, field, value)
        
        # 숫자 필드 처리
        for field in ['grade', 'height', 'weight']:
            value = request.POST.get(field)
            if value and value.strip():  # 빈 문자열이 아닌 경우에만 처리
                setattr(profile, field, int(value))
        
        profile.save()
        
        # 저장 후 값 확인
        print("저장 후 사이즈:", profile.usual_size)
        
        response_data = {
            'status': 'success',
            'profile_data': {
                'bio': profile.bio,
                'location': profile.location,
                'school': profile.school,
                'grade': profile.grade,
                'department': profile.department,
                'gender': profile.gender,
                'usual_size': profile.usual_size,
                'height': profile.height,
                'weight': profile.weight,
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_POST
def toggle_follow(request, user_id):
    try:
        target_user = get_user_model().objects.get(id=user_id)
        
        if request.user == target_user:
            return JsonResponse({'error': '자신을 팔로우할 수 없습니다.'}, status=400)
        
        # 팔로우 관계 확인 및 토글
        follow_relation = Follow.objects.filter(
            follower=request.user,
            following=target_user
        )
        
        if follow_relation.exists():
            follow_relation.delete()
            is_following = False
        else:
            Follow.objects.create(
                follower=request.user,
                following=target_user
            )
            is_following = True
            
        return JsonResponse({
            'status': 'success',
            'is_following': is_following,
            'follower_count': target_user.follower_relations.count()
        })
        
    except get_user_model().DoesNotExist:
        return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

@login_required
def follow_list(request, type, user_id):
    try:
        user = get_user_model().objects.get(id=user_id)
        
        if type == 'followers':
            users = user.follower_relations.all().values_list('follower', flat=True)
            users = get_user_model().objects.filter(id__in=users)
        else:  # following
            users = user.following_relations.all().values_list('following', flat=True)
            users = get_user_model().objects.filter(id__in=users)
        
        users_data = [{
            'id': user.id,
            'username': user.username,
            'profile_image': user.profile.profile_image.url if user.profile.profile_image else None,
            'bio': getattr(user.profile, 'bio', ''),
            'is_following': request.user.following_relations.filter(following=user).exists(),
            'can_follow': request.user != user and request.user.is_authenticated
        } for user in users]
        
        return JsonResponse({'status': 'success', 'users': users_data})
        
    except get_user_model().DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '사용자를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
