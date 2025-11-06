# 后端代码风格指南

本文档概述了联系人管理器后端项目的编码风格和约定。

## 一般原则

- 遵循Python的PEP 8风格指南
- 编写可读、可维护的代码
- 使用有意义的变量和函数名称
- 为所有函数、类和模块添加文档字符串
- 保持函数简短并专注于单一任务

## 格式规范

### 缩进
- 使用4个空格进行缩进
- 永远不要使用制表符

### 行长度
- 最大行长度：79个字符
- 适当换行以保持可读性

### 空白
- 使用空行分隔逻辑部分
- 逗号后添加一个空格
- 运算符周围添加空格
- 函数和类之间使用一个空行

### 命名约定
- **变量/函数**：snake_case
- **类**：PascalCase
- **常量**：UPPER_SNAKE_CASE
- **私有变量/函数**：_leading_underscore

## 代码结构

### 导入
- 按以下顺序分组导入：
  1. 标准库导入
  2. 第三方库导入
  3. 本地应用导入
- 所有导入使用绝对导入
- 每组内按字母顺序排序导入

### 函数
- 限制函数只负责单一职责
- 函数长度保持在50行以内
- 为函数参数和返回值使用类型提示
- 为所有函数添加文档字符串

### 错误处理
- 使用特定异常而不是裸`except`
- 包含有意义的错误消息
- 适当记录异常

## 数据库交互
- 使用参数化查询防止SQL注入
- 保持数据库连接生命周期短暂
- 使用上下文管理器（`with`语句）处理数据库连接
- 正确关闭数据库连接

## API设计
- 遵循RESTful原则
- 使用适当的HTTP方法：
  - GET：检索资源
  - POST：创建资源
  - PUT：更新资源
  - DELETE：删除资源
- 返回适当的HTTP状态码
- 使用JSON作为请求/响应体
- 在响应中包含有意义的错误消息

## 安全
- 存储密码前进行哈希处理
- 验证所有用户输入
- 实现适当的认证和授权
- 在生产环境中使用HTTPS

## 示例代码

```python
import sqlite3
import hashlib
from typing import Tuple, List, Dict, Optional

def hash_password(password: str) -> str:
    """
    使用SHA-256哈希密码。
    
    Args:
        password: 要哈希的明文密码
        
    Returns:
        哈希后的密码
    """
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(username: str) -> Optional[Tuple[int, str, str]]:
    """
    通过用户名从数据库检索用户。
    
    Args:
        username: 要搜索的用户名
        
    Returns:
        如果找到，返回包含user_id、username和密码哈希的元组，
        否则返回None
    """
    try:
        with sqlite3.connect(DB) as conn:
            user = conn.execute(
                'SELECT id, username, password FROM users WHERE username=?',
                (username,)
            ).fetchone()
        return user
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        return None
```

## 代码检查和格式化工具

- 使用`pylint`进行代码分析
- 使用`black`进行代码格式化
- 使用`isort`进行导入排序

## Git提交指南

- 编写清晰、简洁的提交消息
- 在提交消息中适当引用问题编号
- 保持提交专注于单一变更
