# Book Info 管理系统

实现一个简单的 C-S 架构，实现一个 HTTP Server，以及一个 HTTP Client，实现一个bookinfo 资源对象的 CRUD 功能（要求MVC分离，符合该语言基本代码风格规范）

## 项目结构

```
testpythonproject/
├── server/                # 服务器端代码
│   ├── models/            # 数据模型
│   ├── controllers/       # 控制器
│   ├── views/             # 视图
│   └── server.py          # 服务器入口
├── client/                # 客户端代码
│   ├── book_client.py     # 客户端API
│   └── cli.py             # 命令行界面
├── requirements.txt       # 依赖管理
└── README.md              # 项目说明
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务器

```bash
python -m server.server
```

服务器将在 http://localhost:8000 上启动。

## 使用客户端

### 命令行模式

```bash
python -m client.cli [命令]
```

可用命令：

- `list`: 列出所有书籍
- `get <id>`: 获取指定ID的书籍
- `create`: 创建新书籍
- `update <id>`: 更新指定ID的书籍
- `delete <id>`:
 删除指定ID的书籍

示例：

```bash
# 列出所有书籍
python -m client.cli list

# 获取ID为1的书籍
python -m client.cli get 1

# 创建新书籍
python -m client.cli create

# 更新ID为1的书籍
python -m client.cli update 1

# 删除ID为1的书籍
python -m client.cli delete 1
```

### 交互模式

```bash
python -m client.cli interactive
```

在交互模式下，你可以输入命令来操作书籍资源。输入 `help` 查看可用命令。

## API 端点

- `GET /books`: 获取所有书籍
- `GET /books/{id}`: 获取指定ID的书籍
- `POST /books`: 创建新书籍
- `PUT /books/{id}`: 更新指定ID的书籍
- `DELETE /books/{id}`: 删除指定ID的书籍
