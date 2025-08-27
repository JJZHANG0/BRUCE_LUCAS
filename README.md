# Blend Lumina - 艺术品交易网站

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-orange.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Blend Lumina 是一个基于 Django REST Framework 构建的现代化艺术品交易平台，为艺术家、收藏家和艺术爱好者提供完整的艺术品交易、展示和管理服务。

## 🌟 项目特色

- **完整的艺术品交易系统** - 支持购买、销售、拍卖等交易方式
- **多角色用户管理** - 买家、艺术家、商家三种用户角色
- **丰富的分类系统** - 绘画、雕塑、潮玩、周边、手工艺、非遗艺术等
- **定制服务支持** - 个人定制和商业定制服务
- **内容管理系统** - 新闻、文章、轮播图等内容管理
- **现代化API设计** - RESTful API，支持Token认证
- **响应式设计** - 支持多设备访问

## 🚀 技术栈

### 后端技术
- **Python 3.12** - 主要编程语言
- **Django 5.2.5** - Web框架
- **Django REST Framework 3.16.1** - API框架
- **MySQL** - 数据库
- **PyMySQL** - MySQL驱动

### 核心功能
- **用户认证系统** - Session + Token双重认证
- **文件上传** - 支持图片、文档等文件上传
- **搜索过滤** - 强大的搜索和过滤功能
- **分页系统** - 高效的数据分页
- **权限管理** - 细粒度的权限控制

## 📋 功能模块

### 1. 用户管理
- 用户注册、登录、退出
- 多角色用户系统（买家、艺术家、商家）
- 用户档案管理
- 艺术家入驻审核

### 2. 商品管理
- 商品分类管理
- 商品信息管理
- 商品图片管理
- 商品标签系统

### 3. 订单系统
- 购物车管理
- 订单创建和管理
- 支付系统集成
- 订单状态跟踪

### 4. 艺术家服务
- 艺术家店铺管理
- 作品展示
- 客户服务
- 交易管理

### 5. 内容管理
- 新闻管理
- 文章发布
- 轮播图管理
- 活动管理

### 6. 定制服务
- 个人定制请求
- 商业合作申请
- 定制进度跟踪
- 报价管理

## 🛠️ 安装说明

### 环境要求
- Python 3.12+
- MySQL 8.0+
- pip 23.0+

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/blendlumina.git
cd blendlumina
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置数据库
```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE BRUCE_LUCAS CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 环境配置
```bash
# 复制环境配置文件
cp .env.example .env

# 编辑配置文件，设置数据库连接信息
vim .env
```

### 6. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. 初始化数据
```bash
# 创建超级用户
python manage.py createsuperuser

# 初始化分类数据
python manage.py init_categories
```

### 8. 启动服务
```bash
python manage.py runserver
```

访问 http://localhost:8000 查看项目

## 🔧 配置说明

### 数据库配置
在 `settings.py` 中配置数据库连接：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'BRUCE_LUCAS',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### 环境变量
创建 `.env` 文件：

```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=mysql://user:password@localhost:3306/BRUCE_LUCAS
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 📚 API 文档

详细的 API 接口文档请查看 [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### 主要接口
- **用户管理**: `/api/users/`
- **商品分类**: `/api/categories/`
- **商品管理**: `/api/products/`
- **订单管理**: `/api/orders/`
- **购物车**: `/api/cart/`
- **内容管理**: `/api/news/`, `/api/articles/`

### 认证方式
- **Token认证**: 在请求头中添加 `Authorization: Token <your_token>`
- **Session认证**: 适用于Web界面

## 🧪 测试

### 运行测试
```bash
python manage.py test
```

### API测试
```bash
# 使用curl测试
curl -X GET "http://localhost:8000/api/categories/"

# 使用Python requests测试
python test_api.py
```

## 🚀 部署

### 生产环境配置
1. 修改 `settings.py` 中的 `DEBUG = False`
2. 配置生产数据库
3. 设置 `SECRET_KEY`
4. 配置静态文件和媒体文件服务
5. 设置 CORS 策略

### 使用Gunicorn部署
```bash
pip install gunicorn
gunicorn blendlumina.wsgi:application --bind 0.0.0.0:8000
```

## 📁 项目结构

```
blendlumina/
├── blendlumina/          # 项目配置
│   ├── settings.py      # 项目设置
│   ├── urls.py          # 主URL配置
│   └── wsgi.py          # WSGI配置
├── users/               # 用户管理应用
├── products/            # 商品管理应用
├── orders/              # 订单管理应用
├── artists/             # 艺术家服务应用
├── content/             # 内容管理应用
├── customization/       # 定制服务应用
├── static/              # 静态文件
├── media/               # 媒体文件
├── templates/           # 模板文件
├── requirements.txt     # 项目依赖
├── API_DOCUMENTATION.md # API文档
└── README.md           # 项目说明
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- 项目链接: [https://github.com/yourusername/blendlumina]

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

---

**注意**: 这是一个开发中的项目，生产环境使用前请仔细测试和配置。 