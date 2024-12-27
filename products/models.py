from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('uniform', '교복'),
        ('book', '교재'),
        ('supply', '학용품'),
    ]

    UNIFORM_TYPE_CHOICES = [
        ('winter', '동복'),
        ('summer', '하복'),
        ('pe', '체육복'),
        ('casual', '생활복'),
        ('accessory', '액세서리'),
    ]

    CONDITION_CHOICES = [
        ('excellent', '아주 좋아요'),  # 거의 새것과 같은 상태
        ('great', '훌륭해요'),         # 사용감이 적은 상태
        ('vert-good', '좋아요'),            # 사용감이 있으나 깨끗한 상태
        ('good', '나쁘지 않아요'),     # 사용감이 있는 상태
    ]

    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('FREE', 'FREE'),
    ]
    
    TRADE_TYPE_CHOICES = [
        ('direct', '직거래'),
        ('delivery', '택배거래'),
        ('both', '협의'),
    ]

    name = models.CharField(max_length=100, verbose_name='상품명')
    description = models.TextField(verbose_name='설명')
    price = models.IntegerField(verbose_name='가격')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='카테고리')
    uniform_type = models.CharField(
        max_length=10, 
        choices=UNIFORM_TYPE_CHOICES, 
        blank=True,  # 교복이 아닌 경우 선택 안해도 됨
        verbose_name='교복 종류'
    )
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, verbose_name='상태')
    image = models.ImageField(upload_to='products/', verbose_name='대표이미지')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='판매자')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    view_count = models.IntegerField(default=0, verbose_name='조회수')
    size = models.CharField(
        max_length=4, 
        choices=SIZE_CHOICES, 
        default='FREE',
        blank=True,  # 폼에서 선택 안해도 됨
        verbose_name='사이즈'
    )
    trade_type = models.CharField(
        max_length=10, 
        choices=TRADE_TYPE_CHOICES, 
        default='both',
        blank=True,  # 폼에서 선택 안해도 됨
        verbose_name='거래방법'
    )
    is_sold = models.BooleanField(default=False, verbose_name='판매완료')
    sold_at = models.DateTimeField(null=True, blank=True, verbose_name='판매완료일')
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchased_products'
    )
    cart = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CartItem',
        related_name='cart',
        blank=True
    )

    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품들'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def like_count(self):
        return self.cartitem_set.count()

class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='내용')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='평점')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    def __str__(self):
        return f"{self.user.username}의 {self.product.name} 리뷰"

    class Meta:
        ordering = ['-created_at']
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰들'
        unique_together = ['user', 'product']

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='products/additional/', verbose_name='추가이미지')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '상품 추가 이미지'
        verbose_name_plural = '상품 추가 이미지들'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.product.name}의 추가 이미지"

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

class Inquiry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='문의내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    is_answered = models.BooleanField(default=False, verbose_name='답변여부')
    answer = models.TextField(null=True, blank=True, verbose_name='답변내용')
    answered_at = models.DateTimeField(null=True, blank=True, verbose_name='답변일')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '문의'
        verbose_name_plural = '문의들'

class Message(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
