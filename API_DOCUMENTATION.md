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

### 1.5 艺术家档案管理

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

## 2. 商品管理 API

### 2.1 商品分类

**接口**: `GET /api/categories/`

**描述**: 获取所有商品分类

**响应格式**: 数组格式，包含所有分类及其子分类

**响应示例**:
```json
[
    {
        "id": 1,
        "name": "绘画",
        "parent": null,
        "description": "各种绘画作品",
        "image": null,
        "sort_order": 1,
        "is_active": true,
        "children": [
            {
                "id": 2,
                "name": "油画",
                "parent": 1,
                "description": "油画作品",
                "image": null,
                "sort_order": 1,
                "is_active": true,
                "children": []
            },
            {
                "id": 3,
                "name": "水彩",
                "parent": 1,
                "description": "水彩画作品",
                "image": null,
                "sort_order": 2,
                "is_active": true,
                "children": []
            }
        ]
    },
    {
        "id": 10,
        "name": "立体艺术/雕刻",
        "parent": null,
        "description": "立体艺术作品和雕刻品",
        "image": null,
        "sort_order": 2,
        "is_active": true,
        "children": [
            {
                "id": 11,
                "name": "木雕",
                "parent": 10,
                "description": "木雕作品",
                "image": null,
                "sort_order": 1,
                "is_active": true,
                "children": []
            }
        ]
    }
]
```

**分类结构说明**:
- **绘画**: 油画、水彩、素描、丙烯、版画、插画、漫画、数字绘画
- **立体艺术/雕刻**: 木雕、石雕、泥塑、陶瓷、艺术装置、3D打印
- **潮玩**: 盲盒、手办、拼装模型、涂鸦、二次元
- **周边**: 动漫周边、影视周边、游戏周边、小说周边、明星周边、艺术周边、海报、贴纸/卡片、徽章、装饰画、模型、服饰、文具、玩具、数字艺术
- **手工艺**: 刺绣、印染、布艺、首饰、挂件、编织
- **非遗艺术**: 民族工艺

**接口**: `GET /api/categories/root_categories/`

**描述**: 获取根分类（无父分类的主分类）

**响应格式**: 数组格式，只包含主分类及其子分类

**响应示例**:
```json
[
    {
        "id": 1,
        "name": "绘画",
        "parent": null,
        "description": "各种绘画作品",
        "image": null,
        "sort_order": 1,
        "is_active": true,
        "children": [
            {
                "id": 2,
                "name": "油画",
                "parent": 1,
                "description": "油画作品",
                "image": null,
                "sort_order": 1,
                "is_active": true,
                "children": []
            }
        ]
    }
]
```

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

#### 获取商品列表
```bash
curl -X GET "http://localhost:8000/api/products/?search=山水&ordering=-created_at"
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

## 13. Token 认证使用指南

### 13.1 完整认证流程

1. **用户登录获取 Token**
   ```bash
   curl -X POST "http://localhost:8000/api/users/login/" \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin"}'
   ```

2. **使用 Token 调用需要认证的接口**
   ```bash
   curl -X GET "http://localhost:8000/api/users/profile/" \
     -H "Authorization: Token YOUR_TOKEN_HERE"
   ```

3. **用户退出登录**
   ```bash
   curl -X POST "http://localhost:8000/api/users/logout/" \
     -H "Authorization: Token YOUR_TOKEN_HERE"
   ```

### 13.2 Token 安全建议

- **存储安全**: 不要在客户端代码中硬编码 token
- **传输安全**: 始终使用 HTTPS 传输 token
- **过期管理**: 定期更换 token，特别是在生产环境中
- **权限控制**: 不同用户角色的 token 具有不同的权限

### 13.3 常见问题

**Q: Token 过期了怎么办？**
A: 重新调用登录接口获取新的 token

**Q: 可以同时使用多个 token 吗？**
A: 可以，每个 token 都是独立的认证凭证

**Q: Token 被盗用了怎么办？**
A: 立即联系管理员重置 token，或重新登录获取新 token

## 14. 更新日志

- **v1.0.0** (2024-01-01): 初始版本，包含基础功能
- **v1.1.0** (计划): 添加支付集成
- **v1.2.0** (计划): 添加消息系统

---

**联系方式**: admin@blendlumina.com
**技术支持**: 如有问题请联系技术支持团队 