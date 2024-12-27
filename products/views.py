from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg
from .models import Product, Review, ProductImage, CartItem, Inquiry, Message
from accounts.models import Follow
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
import json

class HomeView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = {
            '교복': ['동복', '하복', '체육복', '생활복', '넥타이'],
            '교재': ['교과서', '참고서', '문제집'],
            '학용품': ['필기구', '문구류', '체육용품', '미술용품', '음악용품', '기타학습도구']
        }
        
        if self.request.user.is_authenticated:
            # 읽지 않은 메시지 수 계산
            unread_count = Message.objects.filter(
                receiver=self.request.user,
                is_read=False
            ).count()
            
            # 읽지 않은 메시지가 있는 상품들 조회 (SQLite 호환 버전)
            unread_messages = Message.objects.filter(
                receiver=self.request.user,
                is_read=False
            ).select_related('product').order_by('product_id', '-created_at')
            
            # 상품별로 첫 번째 메시지만 선택
            unique_product_messages = {}
            for message in unread_messages:
                if message.product_id not in unique_product_messages:
                    unique_product_messages[message.product_id] = message
            
            context['unread_message_count'] = unread_count
            context['unread_messages'] = unique_product_messages.values()
            
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')

def home(request):
    view = HomeView.as_view()
    return view(request)

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # 자신의 상품이 아닐 경우에만 조회수 증가
        if request.user != self.object.seller:
            self.object.view_count += 1
            self.object.save(update_fields=['view_count'])
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 현매자의 모든 상품에 대한 리뷰를 가져옴
        context['reviews'] = Review.objects.filter(
            product__seller=self.object.seller  # 현재 상품의 판매자가 판매한 모든 상품의 리뷰
        ).select_related('user', 'product').order_by('-created_at')
        
        context['review_count'] = context['reviews'].count()
        
        # 판매자의 다른 상품들 (현재 상품 제외, 최신순)
        product = self.get_object()
        context['seller_products'] = Product.objects.filter(
            seller=product.seller
        ).exclude(
            id=product.id
        ).order_by('-created_at')[:4] # 4개만 표시
        
        # 판매자 정보
        context['seller'] = product.seller
        context['seller_product_count'] = Product.objects.filter(
            seller=product.seller
        ).count()
        
        # 팔로우 상태
        context['is_following'] = Follow.objects.filter(
            follower=self.request.user, 
            following=self.object.seller
        ).exists() if self.request.user.is_authenticated else False
        
        # 장바구니 상태 확인 로직 추가
        context['is_in_cart'] = CartItem.objects.filter(
            user=self.request.user,
            product=self.object
        ).exists() if self.request.user.is_authenticated else False
        
        # 문의 목록 추가
        context['inquiries'] = self.object.inquiries.all().select_related('user')
        context['inquiry_count'] = context['inquiries'].count()
        
        # 채팅 관련 컨텍스트 추가
        if self.request.user.is_authenticated:
            # 이전 대화 내역이 있는지 확인
            context['has_chat_history'] = Message.objects.filter(
                product=self.object
            ).filter(
                Q(sender=self.request.user) | Q(receiver=self.request.user)
            ).exists()
            
            # 읽지 않은 메시지 수
            context['unread_count'] = Message.objects.filter(
                product=self.object,
                receiver=self.request.user,
                is_read=False
            ).count()
        
        return context

def seller_profile_view(request, seller_id):
    User = get_user_model()
    seller = get_object_or_404(User.objects.select_related('profile'), id=seller_id)
    
    context = {
        'seller': seller,
        'profile': seller.profile,
        'seller_product_count': Product.objects.filter(seller=seller).count(),
        'is_following': (
            request.user.is_authenticated and 
            Follow.objects.filter(follower=request.user, following=seller).exists()
        )
    }
    
    return render(request, 'products/components/seller_profile.html', context)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:home')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        response = super().form_valid(form)
        
        # 추가 이미지 처리
        files = self.request.FILES.getlist('additional_images')
        for f in files:
            ProductImage.objects.create(product=self.object, image=f)
            
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 내가 등록한 상품 목록 (최신순)
        context['my_products'] = Product.objects.filter(
            seller=self.request.user
        ).order_by('-created_at')[:4]  # 최근 4개만 표시
        context['my_product_count'] = Product.objects.filter(
            seller=self.request.user
        ).count()
        return context

class CartView(LoginRequiredMixin, ListView):
    template_name = 'products/cart.html'
    context_object_name = 'cart_items'
    
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 사용자의 채팅 메시지를 최신순으로 정렬하고 중복 제거
        messages = Message.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).select_related('product', 'sender', 'receiver').order_by('-created_at')
        
        # 상품별로 최신 메시지만 그룹화
        unique_messages = {}
        for message in messages:
            if message.product_id not in unique_messages:
                unique_messages[message.product_id] = message
        
        context['messages'] = unique_messages.values()
        return context

@login_required
def toggle_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product in request.user.cart.all():
        request.user.cart.remove(product)
        in_cart = False
    else:
        request.user.cart.add(product)
        in_cart = True
    
    cart_count = product.cart.count()  # 전체 찜하기 수
    
    return JsonResponse({
        'status': 'success',
        'in_cart': in_cart,
        'like_count': cart_count  # 찜하기 수를 반환
    })

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    
    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        product = self.get_object()
        return product.seller == self.request.user
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products:home')
    
    def test_func(self):
        product = self.get_object()
        return product.seller == self.request.user

@login_required
def get_inquiries(request, pk):
    product = get_object_or_404(Product, id=pk)
    inquiries = Inquiry.objects.filter(
        product=product
    ).select_related('user').order_by('-created_at')
    
    data = {
        'inquiries': [{
            'id': inquiry.id,
            'content': inquiry.content,
            'created_at': inquiry.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_answered': inquiry.is_answered,
            'answer': inquiry.answer,
            'answered_at': inquiry.answered_at.strftime('%Y-%m-%d %H:%M:%S') if inquiry.answered_at else None,
            'user': inquiry.user.username
        } for inquiry in inquiries]
    }
    
    return JsonResponse(data)

@login_required
def create_inquiry(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        content = request.POST.get('content')
        
        # 입력값 검증
        if not content:
            return JsonResponse({
                'status': 'error',
                'message': '문의 내용을 입력해주세요.'
            }, status=400)
            
        # 자신의 상품인지 확인
        if product.seller == request.user:
            return JsonResponse({
                'status': 'error',
                'message': '자신의 상품에는 문의할 수 없습니다.'
            }, status=400)
            
        # 문의 생성
        inquiry = Inquiry.objects.create(
            product=product,
            user=request.user,
            content=content
        )
        
        return JsonResponse({
            'status': 'success',
            'message': '문의가 등록되었습니다.',
            'inquiry': {
                'id': inquiry.id,
                'content': inquiry.content,
                'created_at': inquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    return JsonResponse({
        'status': 'error',
        'message': '잘못된 요청입니다.'
    }, status=400)

@login_required
def answer_inquiry(request, pk, inquiry_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        inquiry = get_object_or_404(Inquiry, id=inquiry_id, product=product)
        
        # 판매자 확인
        if request.user != product.seller:
            return JsonResponse({
                'status': 'error',
                'message': '판매자만 답변할 수 있습니다.'
            }, status=403)
            
        answer = request.POST.get('answer')
        if not answer:
            return JsonResponse({
                'status': 'error',
                'message': '답변 내용을 입력해주세요.'
            }, status=400)
            
        # 답변 저장
        inquiry.answer = answer
        inquiry.is_answered = True
        inquiry.answered_at = timezone.now()
        inquiry.save()
        
        return JsonResponse({
            'status': 'success',
            'message': '답변이 등록되었습니다.',
            'answer': {
                'content': inquiry.answer,
                'answered_at': inquiry.answered_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    return JsonResponse({
        'status': 'error',
        'message': '잘못된 요청입니다.'
    }, status=400)

@login_required
def create_review(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        
        # 판매자는 리뷰를 작성할 수 없음
        if request.user == product.seller:
            return JsonResponse({
                'status': 'error',
                'message': '판매자는 리뷰를 작성할 수 없습니다.'
            }, status=403)
            
        # 이미 리뷰를 작성했는지 확인
        if Review.objects.filter(product=product, user=request.user).exists():
            return JsonResponse({
                'status': 'error',
                'message': '이미 리뷰를 작성하셨습니다.'
            }, status=400)
        
        # 거래완료된 상품인지 확인
        if not product.is_sold:
            return JsonResponse({
                'status': 'error',
                'message': '거래완료된 상품에만 리뷰를 작성할 수 있습니다.'
            }, status=400)
            
        try:
            rating = int(request.POST.get('rating', 5))
            content = request.POST.get('content', '').strip()
            
            if not content:
                return JsonResponse({
                    'status': 'error',
                    'message': '리뷰 내용을 입력해주세요.'
                }, status=400)
                
            if not (1 <= rating <= 5):
                return JsonResponse({
                    'status': 'error',
                    'message': '별점은 1~5점 사이여야 합니다.'
                }, status=400)
            
            review = Review.objects.create(
                product=product,
                user=request.user,
                content=content,
                rating=rating
            )
            
            return JsonResponse({
                'status': 'success',
                'message': '리뷰가 등록되었습니다.'
            })
            
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': '잘못된 입력입니다.'
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': '잘못된 요청입니다.'
    }, status=400)

# 시간 차이를 문자열로 변환하는 헬퍼 함수
def timedelta_to_str(td):
    days = td.days
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    
    if days > 0:
        return f"{days}일 전"
    elif hours > 0:
        return f"{hours}시 전"
    elif minutes > 0:
        return f"{minutes}분 전"
    else:
        return "방금 전"

@login_required
def update_review(request, pk, review_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        review = get_object_or_404(Review, id=review_id, product=product)
        
        # 리뷰 작성 확인
        if request.user != review.user:
            return JsonResponse({
                'status': 'error',
                'message': '자신의 리뷰만 수정할 수 있습니다.'
            }, status=403)
            
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        
        # 입력값 검증
        if not content or not rating:
            return JsonResponse({
                'status': 'error',
                'message': '내용과 평점을 모두 입력해주세요.'
            }, status=400)
            
        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                raise ValueError
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': '평점은 1~5 사이의 숫자여야 합니다.'
            }, status=400)
            
        # 리뷰 수정
        review.content = content
        review.rating = rating
        review.save()
        
        return JsonResponse({
            'status': 'success',
            'message': '리뷰가 수정되었습니다.',
            'review': {
                'id': review.id,
                'content': review.content,
                'rating': review.rating,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    return JsonResponse({
        'status': 'error',
        'message': '잘못된 요청입니다.'
    }, status=400)

@login_required
def message_list_create(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            
            if not content:
                return JsonResponse({
                    'status': 'error',
                    'message': '메시지를 입력해주세요.'
                }, status=400)

            # 수신자 결정 로직
            if request.user == product.seller:
                # 판매자인 경우 마지막 대화 상대 찾기
                last_message = Message.objects.filter(
                    product=product,
                    receiver=request.user
                ).order_by('-created_at').first()
                
                receiver = last_message.sender if last_message else None
            else:
                # 구매자인 경우 판매자에게
                receiver = product.seller

            if not receiver:
                return JsonResponse({
                    'status': 'error',
                    'message': '메시지를 보낼 수 없습니다.'
                }, status=400)

            message = Message.objects.create(
                product=product,
                sender=request.user,
                receiver=receiver,
                content=content
            )

            return JsonResponse({
                'status': 'success',
                'message': {
                    'content': message.content,
                    'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'sender_name': message.sender.username,
                    'is_mine': True
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': '잘못된 요청입니다.'
            }, status=400)

    # GET 요청 처리
    messages = Message.objects.filter(
        product=product
    ).filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender').order_by('created_at')

    return JsonResponse({
        'status': 'success',
        'messages': [{
            'content': msg.content,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'sender_name': msg.sender.username,
            'is_mine': msg.sender == request.user
        } for msg in messages]
    })

@login_required
def mark_messages_read(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        
        # 해당 상품의 받은 메시지만 읽음 처리
        Message.objects.filter(
            product=product,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_unread_count(request):
    unread_count = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()
    return JsonResponse({'unread_count': unread_count})

@login_required
def mark_as_sold(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        
        if request.user != product.seller:
            return JsonResponse({
                'status': 'error',
                'message': '상품 등록자만 거래완료 처리할 수 있습니다.'
            }, status=403)
        
        # 마지막 메시지를 보낸 사용자를 구매자로 설정
        last_message = Message.objects.filter(
            product=product
        ).exclude(sender=request.user).order_by('-created_at').first()
        
        product.is_sold = True
        product.sold_at = timezone.now()
        if last_message:
            product.buyer = last_message.sender
        product.save()
        
        return JsonResponse({
            'status': 'success',
            'message': '거래가 완료되었습니다.'
        })
    
    return JsonResponse({
        'status': 'error',
        'message': '잘못된 요청입니다.'
    }, status=400)

@login_required
def message_list(request):
    # 사용자의 모든 메시지 대화를 가져옴
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('product', 'product__seller', 'sender', 'receiver').order_by('-created_at')
    
    # 상품별로 최신 메시지만 그룹화
    conversations = {}
    for msg in messages:
        if msg.product_id not in conversations:
            conversations[msg.product_id] = {
                'product': msg.product,
                'last_message': msg,
                'unread_count': 0,
                'other_user': msg.sender if msg.receiver == request.user else msg.receiver
            }
        
        if msg.receiver == request.user and not msg.is_read:
            conversations[msg.product_id]['unread_count'] += 1
    
    context = {
        'conversations': sorted(
            conversations.values(), 
            key=lambda x: x['last_message'].created_at,
            reverse=True
        )
    }
    
    return render(request, 'products/message_list.html', context)

@login_required
def send_message(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        content = request.POST.get('content', '').strip()
        
        if not content:
            return JsonResponse({
                'status': 'error',
                'message': '메시지 내용을 입력해주세요.'
            }, status=400)
            
        # 판매자는 마지막으로 메시지를 보낸 사용자에게, 구매자는 판매자에게 메시지 전송
        if request.user == product.seller:
            # 판매자가 보내는 경우, 가장 최근에 메시지를 보낸 사용자에게 전송
            last_message = Message.objects.filter(
                product=product
            ).exclude(
                sender=request.user
            ).order_by('-created_at').first()
            
            if not last_message:
                return JsonResponse({
                    'status': 'error',
                    'message': '메시지를 보낼 수 없습니다.'
                }, status=400)
                
            receiver = last_message.sender
        else:
            # 구매자가 보내는 경우, 판매자에게 전송
            receiver = product.seller
            
        message = Message.objects.create(
            product=product,
            sender=request.user,
            receiver=receiver,
            content=content
        )
        
        return JsonResponse({
            'status': 'success',
            'message': {
                'content': message.content,
                'sender_name': message.sender.username,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M'),
                'is_mine': True
            }
        })
        
    return JsonResponse({
        'status': 'error',
        'message': '잘못된 요청입니다.'
    }, status=400)

@login_required
def toggle_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product in request.user.cart.all():
        request.user.cart.remove(product)
        in_cart = False
    else:
        request.user.cart.add(product)
        in_cart = True
    
    return JsonResponse({
        'status': 'success',
        'in_cart': in_cart,
        'like_count': product.like_count
    })

