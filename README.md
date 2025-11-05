# 832301306_contacts_backend
# 联系人管理系统 - 后端

这是联系人管理系统的后端部分，使用Flask构建。它提供了一个RESTful API用于用户认证和联系人管理，并使用SQLite进行数据持久化。

网站：http://47.97.121.247/
## 功能特点

- 用户认证（注册、登录）
- 联系人管理（CRUD操作）
- 支持跨域请求的CORS
- 使用SQLite数据库进行数据持久化
- 密码哈希加密保障安全

## 使用的技术

- Python 3.7+
- Flask
- Flask-CORS
- SQLite3
- hashlib（用于密码哈希）

## 项目结构

```
backend/
├── README.md          # 后端文档
├── app.py             # Flask应用
└── db.sqlite          # SQLite数据库（首次运行时自动创建）
```

## 开始使用

### 先决条件

- Python 3.7+
- pip（Python包管理器）

### 安装

1. 克隆仓库：
   ```bash
   git clone <仓库URL>
   cd contact-manager/backend
   ```

2. 安装依赖：
   ```bash
   pip install flask flask-cors
   ```

### 运行服务器

```bash
python app.py
```

服务器将在 http://localhost:5500 启动，并启用调试模式。

## 数据库

应用使用SQLite进行数据存储。数据库文件（`db.sqlite`）在首次运行时会自动在父目录中创建。

### 数据库 schema

**用户表（Users）**:
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- username (TEXT UNIQUE NOT NULL)
- password (TEXT NOT NULL) - 使用SHA-256哈希

**联系人表（Contacts）**:
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- user_id (INTEGER NOT NULL) - 外键关联到users.id
- name (TEXT NOT NULL)
- phone (TEXT NOT NULL)
- email (TEXT)

## API端点

### 认证

#### 注册新用户
- **URL**: `/register`
- **方法**: `POST`
- **请求体**:
  ```json
  {
    "username": "example_user",
    "password": "example_password"
  }
  ```
- **成功响应**:
  - **状态码**: 201 CREATED
  - **内容**: `{"msg": "Registration successful"}`
- **错误响应**:
  - **状态码**: 400 BAD REQUEST
  - **内容**: `{"error": "Username already exists"}` 或 `{"error": "Username and password are required"}`

#### 登录
- **URL**: `/login`
- **方法**: `POST`
- **请求体**:
  ```json
  {
    "username": "example_user",
    "password": "example_password"
  }
  ```
- **成功响应**:
  - **状态码**: 200 OK
  - **内容**: `{"user_id": 1}`
- **错误响应**:
  - **状态码**: 401 UNAUTHORIZED
  - **内容**: `{"error": "Invalid username or password"}`

### 联系人

#### 添加新联系人
- **URL**: `/contacts`
- **方法**: `POST`
- **请求体**:
  ```json
  {
    "user_id": 1,
    "name": "John Doe",
    "phone": "1234567890",
    "email": "john@example.com"
  }
  ```
- **成功响应**:
  - **状态码**: 201 CREATED
  - **内容**: `{"msg": "Contact added successfully"}`

#### 获取用户的所有联系人
- **URL**: `/contacts/<user_id>`
- **方法**: `GET`
- **成功响应**:
  - **状态码**: 200 OK
  - **内容**: 
    ```json
    [
      {"id": 1, "name": "John Doe", "phone": "1234567890", "email": "john@example.com"},
      {"id": 2, "name": "Jane Smith", "phone": "0987654321", "email": "jane@example.com"}
    ]
    ```

#### 更新联系人
- **URL**: `/contacts/<contact_id>`
- **方法**: `PUT`
- **请求体**:
  ```json
  {
    "name": "John Updated",
    "phone": "1234567890",
    "email": "john.updated@example.com"
  }
  ```
- **成功响应**:
  - **状态码**: 200 OK
  - **内容**: `{"msg": "Contact updated successfully"}`

#### 删除联系人
- **URL**: `/contacts/<contact_id>`
- **方法**: `DELETE`
- **成功响应**:
  - **状态码**: 200 OK
  - **内容**: `{"msg": "Contact deleted successfully"}`

#### 获取用户的联系人数量
- **URL**: `/contacts/count/<user_id>`
- **方法**: `GET`
- **成功响应**:
  - **状态码**: 200 OK
  - **内容**: `{"total": 5}`

## 安全性

- 密码使用SHA-256哈希加密
- 配置了CORS以允许跨域请求
- 对所有API端点进行输入验证


本项目采用MIT许可证授权 - 详见LICENSE文件。
