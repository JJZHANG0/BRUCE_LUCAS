# Blend Lumina 艺术品交易网站 API 接口文档

## 概述

本文档描述了 Blend Lumina 艺术品交易网站的所有 API 接口。API 基于 Django REST Framework 构建，提供完整的艺术品交易、用户管理、内容管理等功能。

**基础URL**: `http://localhost:8000/api/`

## 认证方式

本 API 支持两种认证方式：

### Token 认证（推荐）
- **适用场景**: 移动端应用、前端应用、第三方集成
- **认证方式**: 在请求头中添加 `Authorization: Token <your_token>`
- **获取方式**: 通过登录接口获取
- **优势**: 无状态、易于测试、适合 API 调用

### Session 认证
- **适用场景**: Web 界面、浏览器应用
- **认证方式**: 通过 cookie 中的 sessionid 自动认证
- **获取方式**: 登录后自动设置

**注意**: 大多数 API 接口推荐使用 Token 认证，更符合 RESTful API 设计原则。

## 1. 用户管理 API

### 1.1 用户注册

**接口**: `POST /api/users/register/`

**描述**: 用户注册

**请求体**:
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "first_name": "张",
    "last_name": "三",
    "user_type": "buyer",
    "phone": "13800138000"
}
```

**响应**:
```json
{
    "message": "用户注册成功",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "张",
        "last_name": "三",
        "user_type": "buyer",
        "phone": "13800138000",
        "is_verified": false,
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

### 1.2 用户登录

**接口**: `POST /api/users/login/`

**描述**: 用户登录，支持用户名/密码认证，返回用户信息和认证 token

**请求体**:
```json
{
    "username": "testuser",
    "password": "password123"
}
```

**响应**:
```json
{
    "message": "登录成功",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "张",
        "last_name": "三",
        "user_type": "buyer",
        "phone": "13800138000",
        "wechat": "",
        "avatar": null,
        "is_verified": false,
        "created_at": "2024-01-01T00:00:00Z"
    },
    "token": "289bb0861ccbcc3565ca404222461d27e3f65fe4",
    "token_type": "Token"
}
```

**重要说明**:
- 登录成功后，服务器会返回一个唯一的 `token`
- 此 token 用于后续所有需要认证的 API 调用
- Token 格式：在请求头中添加 `Authorization: Token <your_token>`
- 示例：`Authorization: Token 289bb0861ccbcc3565ca404222461d27e3f65fe4`

### 1.3 用户退出

**接口**: `POST /api/users/logout/`

**描述**: 用户退出登录，需要提供有效的认证 token

**认证**: 需要在请求头中提供有效的 token
```
Authorization: Token <your_token>
```

**响应**:
```json
{
    "message": "退出登录成功"
}
```

**重要说明**:
- 此接口需要认证，请确保在请求头中提供有效的 token
- 退出登录后，当前 token 仍然有效（如需立即失效，请联系管理员）
- 建议客户端在退出登录后删除本地存储的 token

### 1.4 获取用户信息

**接口**: `GET /api/users/profile/`

**描述**: 获取当前登录用户信息

**响应**:
```json
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "张",
    "last_name": "三",
    "user_type": "buyer",
    "phone": "13800138000",
    "avatar": null,
    "is_verified": false,
    "created_at": "2024-01-01T00:00:00Z"
}
```

### 1.5 修改用户信息

**接口**: `PUT /api/users/update_profile/`

**描述**: 修改当前登录用户信息

**认证**: 需要在请求头中提供有效的 token
```
Authorization: Token <your_token>
```

**请求体**:
```json
{
    "first_name": "张",
    "last_name": "三",
    "phone": "13800138000",
    "wechat": "zhangsan123",
    "avatar": "头像文件"
}
```

**响应**:
```json
{
    "message": "用户信息更新成功",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "张",
        "last_name": "三",
        "user_type": "buyer",
        "phone": "13800138000",
        "wechat": "zhangsan123",
        "avatar": "/media/avatars/avatar.jpg",
        "is_verified": false,
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

### 1.6 艺术家注册（需要资质审核）

**接口**: `POST /api/users/register_artist/`

**描述**: 艺术家注册，需要提交资质材料进行后台审核

**请求体** (multipart/form-data):
```
username: artist1
email: artist1@example.com
password: password123
first_name: 李
last_name: 四
phone: 13900139000
artist_name: 李四艺术家
bio: 专业油画艺术家，擅长风景画
tags: ["油画", "风景", "写实"]

# 资质材料（必填）
education_background: 中央美术学院油画系本科毕业
professional_experience: 从事油画创作10年，曾在多家画廊举办个展
awards_honors: 2019年获得全国油画大赛金奖
exhibition_history: 2020年北京798艺术区个展，2021年上海美术馆联展

# 文件上传（必填）
identity_document: 身份证扫描件
art_qualification: 艺术资质证明文件
portfolio_document: 作品集PDF文档
portfolio_images: [作品图片1, 作品图片2, 作品图片3, ...]
other_documents: [其他证明材料1, 其他证明材料2, ...]
```

**响应**:
```json
{
    "message": "艺术家注册申请已提交，等待审核",
    "user": {
        "id": 2,
        "username": "artist1",
        "email": "artist1@example.com",
        "first_name": "李",
        "last_name": "四",
        "user_type": "artist",
        "phone": "13900139000",
        "is_verified": false,
        "created_at": "2024-01-01T00:00:00Z"
    },
    "artist_profile": {
        "id": 1,
        "artist_name": "李四艺术家",
        "bio": "专业油画艺术家，擅长风景画",
        "tags": ["油画", "风景", "写实"],
        "education_background": "中央美术学院油画系本科毕业",
        "professional_experience": "从事油画创作10年，曾在多家画廊举办个展",
        "awards_honors": "2019年获得全国油画大赛金奖",
        "exhibition_history": "2020年北京798艺术区个展，2021年上海美术馆联展",
        "portfolio_images": ["/media/artist_documents/portfolio/work1.jpg"],
        "other_documents": ["/media/artist_documents/other/cert1.pdf"],
        "is_approved": false,
        "followers_count": 0,
        "works_count": 0,
        "submitted_at": "2024-01-01T00:00:00Z"
    },
    "review_status": "pending"
}
```

**重要说明**:
- 艺术家注册需要提交完整的资质材料
- 注册后状态为 `pending`，需要后台管理员审核
- 只有通过审核的艺术家才能上传作品和享受艺术家功能
- 审核通过后，`is_approved` 字段会变为 `true`

### 1.7 艺术家档案管理

**接口**: `GET /api/artist-profiles/`

**描述**: 获取所有艺术家档案

**查询参数**:
- `search`: 搜索艺术家名称或简介
- `is_approved`: 是否已审核通过

**响应**:
```json
[
    {
        "id": 1,
        "user": {
            "id": 2,
            "username": "artist1",
            "email": "artist1@example.com"
        },
        "artist_name": "张三艺术家",
        "bio": "专业油画艺术家",
        "tags": ["油画", "风景"],
        "is_approved": true,
        "followers_count": 100,
        "works_count": 50
    }
]
```

**接口**: `GET /api/artist-profiles/approved/`

**描述**: 获取已审核通过的艺术家

**接口**: `POST /api/artist-profiles/create_profile/`

**描述**: 艺术家创建自己的信息

**认证**: 需要在请求头中提供有效的 token
```
Authorization: Token <your_token>
```

**请求体**:
```json
{
    "artist_name": "王五艺术家",
    "bio": "专业水彩画艺术家，擅长人物画",
    "tags": ["水彩", "人物", "写实"]
}
```

**响应**:
```json
{
    "message": "艺术家档案创建成功",
    "profile": {
        "id": 2,
        "artist_name": "王五艺术家",
        "bio": "专业水彩画艺术家，擅长人物画",
        "tags": ["水彩", "人物", "写实"],
        "is_approved": false,
        "followers_count": 0,
        "works_count": 0
    }
}
```

**接口**: `PUT /api/artist-profiles/update_profile/`

**描述**: 艺术家更新自己的信息

**认证**: 需要在请求头中提供有效的 token
```
Authorization: Token <your_token>
```

**请求体**:
```json
{
    "artist_name": "王五艺术家（更新）",
    "bio": "专业水彩画艺术家，擅长人物画和风景画",
    "tags": ["水彩", "人物", "风景", "写实"]
}
```

### 1.8 艺术家审核管理（管理员）

**接口**: `GET /api/artist-profiles/pending_artists/`

**描述**: 获取待审核的艺术家列表（仅管理员）

**认证**: 需要在请求头中提供有效的管理员 token
```
Authorization: Token <admin_token>
```

**响应**:
```json
[
    {
        "id": 1,
        "user": {
            "id": 2,
            "username": "artist1",
            "email": "artist1@example.com"
        },
        "artist_name": "李四艺术家",
        "bio": "专业油画艺术家，擅长风景画",
        "education_background": "中央美术学院油画系本科毕业",
        "professional_experience": "从事油画创作10年",
        "awards_honors": "2019年获得全国油画大赛金奖",
        "exhibition_history": "2020年北京798艺术区个展",
        "portfolio_images": ["/media/artist_documents/portfolio/work1.jpg"],
        "is_approved": false,
        "submitted_at": "2024-01-01T00:00:00Z"
    }
]
```

**接口**: `POST /api/artist-profiles/{id}/review_artist/`

**描述**: 审核艺术家申请（仅管理员）

**认证**: 需要在请求头中提供有效的管理员 token
```
Authorization: Token <admin_token>
```

**请求体** (通过审核):
```json
{
    "action": "approve",
    "review_notes": "资质材料齐全，作品质量优秀，同意通过审核"
}
```

**请求体** (拒绝申请):
```json
{
    "action": "reject",
    "rejection_reason": "作品集质量不符合要求，请重新提交",
    "review_notes": "建议提供更多高质量作品"
}
```

**响应** (通过审核):
```json
{
    "message": "艺术家申请已通过",
    "artist_profile": {
        "id": 1,
        "artist_name": "李四艺术家",
        "is_approved": true,
        "approval_date": "2024-01-01T12:00:00Z",
        "review_notes": "资质材料齐全，作品质量优秀，同意通过审核",
        "reviewed_at": "2024-01-01T12:00:00Z"
    }
}
```

**响应** (拒绝申请):
```json
{
    "message": "艺术家申请已拒绝",
    "artist_profile": {
        "id": 1,
        "artist_name": "李四艺术家",
        "is_approved": false,
        "rejection_reason": "作品集质量不符合要求，请重新提交",
        "review_notes": "建议提供更多高质量作品",
        "reviewed_at": "2024-01-01T12:00:00Z"
    }
}
```

## 2. 商品管理 API

### 2.1 商品分类

**接口**: `GET /api/categories/`

**描述**: 获取所有商品分类

**响应**:
```json
[
    {
        "id": 1,
        "name": "绘画",
        "parent": null,
        "description": "各种绘画作品",
        "image": null,
        "sort_order": 0,
        "is_active": true,
        "children": [
            {
                "id": 2,
                "name": "油画",
                "parent": 1,
                "description": "油画作品",
                "children": []
            }
        ]
    }
]
```

**接口**: `GET /api/categories/root_categories/`

**描述**: 获取根分类

### 2.2 商品列表

**接口**: `GET /api/products/`

**描述**: 获取商品列表

**查询参数**:
- `search`: 搜索商品标题或描述
- `category`: 按分类筛选
- `artist`: 按艺术家筛选
- `ordering`: 排序方式 (price, -price, created_at, -created_at, views_count, -views_count, likes_count, -likes_count)

**响应**:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "山水画",
            "price": "1000.00",
            "original_price": "1200.00",
            "category": {
                "id": 2,
                "name": "油画"
            },
            "primary_image": {
                "id": 1,
                "image": "/media/products/landscape.jpg",
                "alt_text": "山水画"
            },
            "views_count": 50,
            "likes_count": 10,
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### 2.3 商品详情

**接口**: `GET /api/products/{id}/`

**描述**: 获取商品详情

**响应**:
```json
{
    "id": 1,
    "title": "山水画",
    "description": "精美的山水画作品",
    "artist": {
        "id": 1,
        "artist_name": "张三艺术家"
    },
    "category": {
        "id": 2,
        "name": "油画"
    },
    "price": "1000.00",
    "original_price": "1200.00",
    "size": "60x80cm",
    "weight": "2.5",
    "materials": ["油画布", "油画颜料"],
    "techniques": ["写实"],
    "year_created": 2023,
    "is_original": true,
    "is_limited": false,
    "status": "published",
    "views_count": 50,
    "likes_count": 10,
    "images": [
        {
            "id": 1,
            "image": "/media/products/landscape.jpg",
            "alt_text": "山水画",
            "is_primary": true,
            "sort_order": 0
        }
    ],
    "tags": [
        {
            "id": 1,
            "name": "风景",
            "color": "#007bff"
        }
    ]
}
```

### 2.4 推荐商品

**接口**: `GET /api/products/featured/`

**描述**: 获取推荐商品

### 2.5 按分类获取商品

**接口**: `GET /api/products/by_category/?category_id=2`

**描述**: 按分类获取商品

### 2.6 增加商品浏览量

**接口**: `POST /api/products/{id}/increment_views/`

**描述**: 增加商品浏览量

### 2.7 商品点赞

**接口**: `POST /api/products/{id}/increment_likes/`

**描述**: 增加商品点赞数

### 2.8 作品上传

**接口**: `POST /api/products/upload_work/`

**描述**: 艺术家上传作品

**认证**: 需要在请求头中提供有效的 token
```
Authorization: Token <your_token>
```

**请求体** (multipart/form-data):
```
title: 山水画
description: 精美的山水画作品
category: 2
price: 1000.00
original_price: 1200.00
size: 60x80cm
weight: 2.5
materials: ["油画布", "油画颜料"]
techniques: ["写实"]
year_created: 2023
is_original: true
is_limited: false
images: [图片文件1, 图片文件2, ...]
image_alt_0: 主图描述
image_alt_1: 第二张图片描述
tags: ["风景", "山水", "油画"]
```

**响应**:
```json
{
    "message": "作品上传成功",
    "product": {
        "id": 1,
        "title": "山水画",
        "description": "精美的山水画作品",
        "artist": {
            "id": 1,
            "artist_name": "张三艺术家"
        },
        "category": {
            "id": 2,
            "name": "油画"
        },
        "price": "1000.00",
        "original_price": "1200.00",
        "size": "60x80cm",
        "weight": "2.5",
        "materials": ["油画布", "油画颜料"],
        "techniques": ["写实"],
        "year_created": 2023,
        "is_original": true,
        "is_limited": false,
        "status": "draft",
        "views_count": 0,
        "likes_count": 0,
        "images": [
            {
                "id": 1,
                "image": "/media/products/landscape.jpg",
                "alt_text": "主图描述",
                "is_primary": true,
                "sort_order": 0
            }
        ],
        "tags": [
            {
                "id": 1,
                "name": "风景",
                "color": "#007bff"
            }
        ]
    }
}
```

## 3. 购物车和订单 API

### 3.1 购物车管理

**接口**: `GET /api/cart/`

**描述**: 获取购物车商品

**响应**:
```json
[
    {
        "id": 1,
        "product": 1,
        "product_title": "山水画",
        "product_price": "1000.00",
        "product_image": "/media/products/landscape.jpg",
        "quantity": 1,
        "total_price": "1000.00",
        "added_at": "2024-01-01T00:00:00Z"
    }
]
```

**接口**: `POST /api/cart/add_to_cart/`

**描述**: 添加到购物车

**请求体**:
```json
{
    "product_id": 1,
    "quantity": 1
}
```

**接口**: `POST /api/cart/{id}/update_quantity/`

**描述**: 更新购物车商品数量

**请求体**:
```json
{
    "quantity": 2
}
```

**接口**: `GET /api/cart/total/`

**描述**: 获取购物车总金额

### 3.2 愿望清单

**接口**: `GET /api/wishlist/`

**描述**: 获取愿望清单

**接口**: `POST /api/wishlist/add_to_wishlist/`

**描述**: 添加到愿望清单

**请求体**:
```json
{
    "product_id": 1
}
```

### 3.3 订单管理

**接口**: `GET /api/orders/`

**描述**: 获取用户订单列表

**接口**: `POST /api/orders/`

**描述**: 创建订单

**请求体**:
```json
{
    "shipping_address": {
        "name": "张三",
        "phone": "13800138000",
        "address": "北京市朝阳区xxx街道xxx号"
    },
    "contact_phone": "13800138000",
    "contact_name": "张三",
    "notes": "请小心包装",
    "items": [
        {
            "product_id": 1,
            "quantity": 1
        }
    ]
}
```

**接口**: `GET /api/orders/by_status/?status=pending_payment`

**描述**: 按状态获取订单

### 3.4 订单支付

**接口**: `POST /api/payments/process_payment/`

**描述**: 订单支付接口

**认证**: 需要在请求头中提供有效的 token
```
Authorization: Token <your_token>
```

**请求体**:
```json
{
    "order_id": 1,
    "payment_method": "alipay"
}
```

**响应**:
```json
{
    "message": "支付成功",
    "payment": {
        "id": 1,
        "order": 1,
        "payment_method": "alipay",
        "amount": "1000.00",
        "transaction_id": "TXN00000001",
        "status": "success",
        "payment_time": "2024-01-01T12:00:00Z",
        "created_at": "2024-01-01T12:00:00Z"
    },
    "order": {
        "id": 1,
        "order_number": "BL12345678",
        "status": "paid",
        "total_amount": "1000.00",
        "final_amount": "1000.00",
        "payment_time": "2024-01-01T12:00:00Z",
        "payment_method": "alipay"
    }
}
```

**接口**: `POST /api/payments/{id}/refund/`

**描述**: 退款接口

**认证**: 需要在请求头中提供有效的 token
```
Authorization: Token <your_token>
```

**响应**:
```json
{
    "message": "退款成功",
    "refund_payment": {
        "id": 2,
        "order": 1,
        "payment_method": "alipay",
        "amount": "-1000.00",
        "transaction_id": "REF00000001",
        "status": "success",
        "payment_time": "2024-01-01T13:00:00Z",
        "created_at": "2024-01-01T13:00:00Z"
    }
}
```

## 4. 内容管理 API

### 4.1 轮播图

**接口**: `GET /api/banners/`

**描述**: 获取所有轮播图

**接口**: `GET /api/banners/active/`

**描述**: 获取当前活跃的轮播图

### 4.2 新闻资讯

**接口**: `GET /api/news/`

**描述**: 获取新闻列表

**查询参数**:
- `search`: 搜索新闻标题或内容
- `ordering`: 排序方式
- `type`: 新闻类型

**接口**: `GET /api/news/featured/`

**描述**: 获取推荐新闻

**接口**: `GET /api/news/by_type/?type=art_news`

**描述**: 按类型获取新闻

### 4.3 用户文章

**接口**: `GET /api/articles/`

**描述**: 获取文章列表

**接口**: `POST /api/articles/`

**描述**: 创建文章

**请求体**:
```json
{
    "title": "我的艺术感悟",
    "content": "这是一篇关于艺术的感悟文章...",
    "cover_image": null
}
```

**接口**: `GET /api/articles/featured/`

**描述**: 获取推荐文章

**接口**: `GET /api/articles/my_articles/`

**描述**: 获取我的文章

### 4.4 活动管理

**接口**: `GET /api/activities/`

**描述**: 获取活动列表

**接口**: `GET /api/activities/featured/`

**描述**: 获取推荐活动

**接口**: `GET /api/activities/upcoming/`

**描述**: 获取即将开始的活动

## 5. 艺术家服务 API

### 5.1 艺术家店铺

**接口**: `GET /api/artist-shops/`

**描述**: 获取艺术家店铺列表

### 5.2 艺术家作品集

**接口**: `GET /api/artist-portfolios/`

**描述**: 获取艺术家作品集

### 5.3 艺术家服务

**接口**: `GET /api/artist-services/`

**描述**: 获取艺术家服务列表

### 5.4 提现管理

**接口**: `GET /api/artist-withdrawals/`

**描述**: 获取提现申请列表

**接口**: `POST /api/artist-withdrawals/`

**描述**: 申请提现

**请求体**:
```json
{
    "amount": "1000.00",
    "bank_account": "6222021234567890123",
    "bank_name": "中国工商银行",
    "notes": "提现到工商银行"
}
```

## 6. 定制服务 API

### 6.1 定制请求

**接口**: `GET /api/customization-requests/`

**描述**: 获取定制请求列表

**接口**: `POST /api/customization-requests/`

**描述**: 创建定制请求

**请求体**:
```json
{
    "request_type": "personal",
    "customization_type": "painting",
    "title": "定制油画",
    "description": "想要一幅山水画",
    "reference_images": [],
    "budget_range": "1000-2000",
    "duration_type": "short",
    "expected_delivery": "2024-02-01"
}
```

### 6.2 商业合作

**接口**: `POST /api/commercial-cooperations/`

**描述**: 提交商业合作申请

**请求体**:
```json
{
    "company_name": "ABC公司",
    "contact_person": "李四",
    "contact_phone": "13900139000",
    "contact_email": "lisi@abc.com",
    "cooperation_type": "institutional",
    "project_description": "需要定制一批艺术品",
    "budget_range": "50000-100000",
    "expected_timeline": "3个月"
}
```

### 6.3 个性化定制提交

**接口**: `POST /api/customization-requests/submit_customization/`

**描述**: 提交个性化定制请求

**认证**: 需要在请求头中提供有效的 token
```
Authorization: Token <your_token>
```

**请求体** (multipart/form-data):
```
request_type: personal
customization_type: painting
title: 定制油画
description: 想要一幅山水画
budget_range: 1000-2000
duration_type: short
expected_delivery: 2024-02-01
reference_images: [参考图片1, 参考图片2, ...]
```

**响应**:
```json
{
    "message": "定制请求提交成功",
    "request": {
        "id": 1,
        "user": 1,
        "request_type": "personal",
        "customization_type": "painting",
        "title": "定制油画",
        "description": "想要一幅山水画",
        "reference_images": ["/media/customization/ref1.jpg"],
        "budget_range": "1000-2000",
        "duration_type": "short",
        "expected_delivery": "2024-02-01",
        "status": "pending",
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

**接口**: `POST /api/customization-requests/{id}/update_status/`

**描述**: 更新定制请求状态

**认证**: 需要在请求头中提供有效的 token
```
Authorization: Token <your_token>
```

**请求体**:
```json
{
    "status": "accepted"
}
```

**响应**:
```json
{
    "message": "状态更新成功",
    "request": {
        "id": 1,
        "status": "accepted",
        "updated_at": "2024-01-01T12:00:00Z"
    }
}
```

## 7. 测试示例

### 7.1 使用 curl 测试

#### 用户注册
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "first_name": "张",
    "last_name": "三",
    "user_type": "buyer",
    "phone": "13800138000"
  }'
```

#### 用户登录
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

**登录成功后，保存返回的 token 用于后续请求**

#### 使用 Token 获取用户信息
```bash
curl -X GET "http://localhost:8000/api/users/profile/" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

#### 修改用户信息
```bash
curl -X PUT "http://localhost:8000/api/users/update_profile/" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "张",
    "last_name": "三",
    "phone": "13800138000",
    "wechat": "zhangsan123"
  }'
```

#### 艺术家注册（带资质材料）
```bash
curl -X POST http://localhost:8000/api/users/register_artist/ \
  -F "username=artist1" \
  -F "email=artist1@example.com" \
  -F "password=password123" \
  -F "first_name=李" \
  -F "last_name=四" \
  -F "phone=13900139000" \
  -F "artist_name=李四艺术家" \
  -F "bio=专业油画艺术家，擅长风景画" \
  -F "tags=[\"油画\", \"风景\", \"写实\"]" \
  -F "education_background=中央美术学院油画系本科毕业" \
  -F "professional_experience=从事油画创作10年，曾在多家画廊举办个展" \
  -F "awards_honors=2019年获得全国油画大赛金奖" \
  -F "exhibition_history=2020年北京798艺术区个展，2021年上海美术馆联展" \
  -F "identity_document=@id_card.jpg" \
  -F "art_qualification=@qualification.pdf" \
  -F "portfolio_document=@portfolio.pdf" \
  -F "portfolio_images=@work1.jpg" \
  -F "portfolio_images=@work2.jpg" \
  -F "other_documents=@cert1.pdf"
```

#### 管理员审核艺术家申请
```bash
# 获取待审核的艺术家列表
curl -X GET "http://localhost:8000/api/artist-profiles/pending_artists/" \
  -H "Authorization: Token ADMIN_TOKEN_HERE"

# 通过审核
curl -X POST "http://localhost:8000/api/artist-profiles/1/review_artist/" \
  -H "Authorization: Token ADMIN_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "approve",
    "review_notes": "资质材料齐全，作品质量优秀，同意通过审核"
  }'

# 拒绝申请
curl -X POST "http://localhost:8000/api/artist-profiles/1/review_artist/" \
  -H "Authorization: Token ADMIN_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "reject",
    "rejection_reason": "作品集质量不符合要求，请重新提交",
    "review_notes": "建议提供更多高质量作品"
  }'
```

#### 获取商品列表
```bash
curl -X GET "http://localhost:8000/api/products/?search=山水&ordering=-created_at"
```

#### 作品上传
```bash
curl -X POST http://localhost:8000/api/products/upload_work/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "title=山水画" \
  -F "description=精美的山水画作品" \
  -F "category=2" \
  -F "price=1000.00" \
  -F "original_price=1200.00" \
  -F "size=60x80cm" \
  -F "materials=[\"油画布\", \"油画颜料\"]" \
  -F "techniques=[\"写实\"]" \
  -F "year_created=2023" \
  -F "is_original=true" \
  -F "images=@image1.jpg" \
  -F "images=@image2.jpg" \
  -F "tags=[\"风景\", \"山水\", \"油画\"]"
```

#### 添加到购物车
```bash
curl -X POST http://localhost:8000/api/cart/add_to_cart/ \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 1
  }'
```

#### 订单支付
```bash
curl -X POST http://localhost:8000/api/payments/process_payment/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "payment_method": "alipay"
  }'
```

#### 个性化定制提交
```bash
curl -X POST http://localhost:8000/api/customization-requests/submit_customization/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "request_type=personal" \
  -F "customization_type=painting" \
  -F "title=定制油画" \
  -F "description=想要一幅山水画" \
  -F "budget_range=1000-2000" \
  -F "duration_type=short" \
  -F "expected_delivery=2024-02-01" \
  -F "reference_images=@reference1.jpg"
```

### 7.2 使用 Python requests 测试

```python
import requests

# 基础URL
base_url = "http://localhost:8000/api"

# 用户注册
register_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "first_name": "张",
    "last_name": "三",
    "user_type": "buyer",
    "phone": "13800138000"
}

response = requests.post(f"{base_url}/users/register/", json=register_data)
print("注册响应:", response.json())

# 用户登录
login_data = {
    "username": "testuser",
    "password": "password123"
}

response = requests.post(f"{base_url}/users/login/", json=login_data)
print("登录响应:", response.json())

# 保存 token 用于后续请求
if response.status_code == 200:
    token = response.json().get('token')
    print(f"获取到 token: {token}")
    
    # 设置认证头
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 使用 token 获取用户信息
    response = requests.get(f"{base_url}/users/profile/", headers=headers)
    print("用户信息:", response.json())
    
    # 使用 token 添加到购物车
    cart_data = {
        "product_id": 1,
        "quantity": 1
    }
    response = requests.post(f"{base_url}/cart/add_to_cart/", 
                           json=cart_data, headers=headers)
    print("购物车添加:", response.json())
    
    # 用户退出登录
    response = requests.post(f"{base_url}/users/logout/", headers=headers)
    print("退出登录:", response.json())
else:
    print("登录失败")

# 获取商品列表（无需认证）
response = requests.get(f"{base_url}/products/")
print("商品列表:", response.json())
```

### 7.3 使用 Postman 测试

1. 导入以下集合到 Postman
2. 设置环境变量 `base_url` 为 `http://localhost:8000`
3. 按顺序执行请求

## 8. 错误处理

### 8.1 常见错误码

- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未认证
- `403 Forbidden`: 权限不足
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器内部错误

### 8.2 错误响应格式

```json
{
    "error": "错误描述",
    "detail": "详细错误信息"
}
```

## 9. 分页

所有列表接口都支持分页，响应格式：

```json
{
    "count": 总数量,
    "next": "下一页URL",
    "previous": "上一页URL",
    "results": [数据列表]
}
```

## 10. 过滤和搜索

支持以下过滤方式：
- `search`: 文本搜索
- `ordering`: 排序
- 模型字段过滤
- 自定义过滤器

## 11. 权限说明

- `AllowAny`: 无需认证
- `IsAuthenticated`: 需要登录
- `IsAdminUser`: 需要管理员权限

## 12. 部署说明

### 12.1 生产环境配置

1. 修改 `settings.py` 中的 `DEBUG = False`
2. 配置生产数据库
3. 设置 `SECRET_KEY`
4. 配置静态文件和媒体文件服务
5. 设置 CORS 策略

### 12.2 性能优化

1. 使用 Redis 缓存
2. 数据库查询优化
3. 图片压缩和CDN
4. API 限流

## 13. 更新日志

- **v1.0.0** (2024-01-01): 初始版本，包含基础功能
- **v1.1.0** (计划): 添加   集成
- **v1.2.0** (计划): 添加消息系统

---

**联系方式**: admin@blendlumina.com
**技术支持**: 如有问题请联系技术支持团队 