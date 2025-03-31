import argparse
import json
import sys
import logging
from tabulate import tabulate

from client.book_client import BookClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_books(books):
    """以表格形式打印书籍列表"""
    if not books:
        print("没有找到书籍")
        return
    
    headers = ["ID", "标题", "作者", "出版年份", "ISBN"]
    table_data = []
    
    for book in books:
        table_data.append([
            book.get("id", ""),
            book.get("title", ""),
            book.get("author", ""),
            book.get("publication_year", ""),
            book.get("isbn", "")
        ])
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def print_book(book):
    """打印单本书籍的详细信息"""
    if not book:
        print("没有找到书籍")
        return
    
    print("\n书籍详情:")
    print(f"ID: {book.get('id', '')}")
    print(f"标题: {book.get('title', '')}")
    print(f"作者: {book.get('author', '')}")
    print(f"出版年份: {book.get('publication_year', '')}")
    print(f"ISBN: {book.get('isbn', '')}")
    print()

def get_book_input():
    """从用户获取书籍信息"""
    book = {}
    book["title"] = input("标题: ")
    book["author"] = input("作者: ")
    
    while True:
        try:
            year = input("出版年份 (例如: 2020): ")
            book["publication_year"] = int(year)
            break
        except ValueError:
            print("请输入有效的年份（数字）")
    
    book["isbn"] = input("ISBN: ")
    return book

def main():
    parser = argparse.ArgumentParser(description="书籍管理客户端")
    parser.add_argument("--host", default="localhost", help="服务器主机")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口")
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 列出所有书籍
    subparsers.add_parser("list", help="列出所有书籍")
    
    # 获取单本书籍
    get_parser = subparsers.add_parser("get", help="获取单本书籍")
    get_parser.add_argument("id", help="书籍ID")
    
    # 创建书籍
    create_parser = subparsers.add_parser("create", help="创建新书籍")
    create_parser.add_argument("--title", help="书籍标题")
    create_parser.add_argument("--author", help="作者")
    create_parser.add_argument("--year", type=int, help="出版年份")
    create_parser.add_argument("--isbn", help="ISBN")
    
    # 更新书籍
    update_parser = subparsers.add_parser("update", help="更新书籍")
    update_parser.add_argument("id", help="书籍ID")
    update_parser.add_argument("--title", help="书籍标题")
    update_parser.add_argument("--author", help="作者")
    update_parser.add_argument("--year", type=int, help="出版年份")
    update_parser.add_argument("--isbn", help="ISBN")
    
    # 删除书籍
    delete_parser = subparsers.add_parser("delete", help="删除书籍")
    delete_parser.add_argument("id", help="书籍ID")
    
    # 交互模式
    subparsers.add_parser("interactive", help="进入交互模式")
    
    args = parser.parse_args()
    
    # 创建客户端
    base_url = f"http://{args.host}:{args.port}"
    client = BookClient(base_url)
    
    if args.command == "list":
        books, error = client.get_all_books()
        if books:
            print_books(books)
        else:
            print(f"错误: {error}")
    
    elif args.command == "get":
        book, error = client.get_book(args.id)
        if book:
            print_book(book)
        else:
            print(f"错误: {error}")
    
    elif args.command == "create":
        if all([args.title, args.author, args.year, args.isbn]):
            book_data = {
                "title": args.title,
                "author": args.author,
                "publication_year": args.year,
                "isbn": args.isbn
            }
        else:
            print("请输入书籍信息:")
            book_data = get_book_input()
        
        book, error = client.create_book(book_data)
        if book:
            print("书籍创建成功:")
            print_book(book)
        else:
            print(f"错误: {error}")
    
    elif args.command == "update":
        book_data = {}
        if args.title:
            book_data["title"] = args.title
        if args.author:
            book_data["author"] = args.author
        if args.year:
            book_data["publication_year"] = args.year
        if args.isbn:
            book_data["isbn"] = args.isbn
        
        if not book_data:
            print("请输入要更新的书籍信息:")
            book, error = client.get_book(args.id)
            if book:
                print(f"正在更新书籍 ID={args.id}")
                print("(保留空白将保持原值不变)")
                title = input(f"标题 [{book.get('title', '')}]: ")
                author = input(f"作者 [{book.get('author', '')}]: ")
                year = input(f"出版年份 [{book.get('publication_year', '')}]: ")
                isbn = input(f"ISBN [{book.get('isbn', '')}]: ")
                
                book_data = {
                    "title": title or book.get("title", ""),
                    "author": author or book.get("author", ""),
                    "publication_year": int(year) if year else book.get("publication_year", 0),
                    "isbn": isbn or book.get("isbn", "")
                }
            else:
                print(f"错误: {error}")
                return
        
        book, error = client.update_book(args.id, book_data)
        if book:
            print("书籍更新成功:")
            print_book(book)
        else:
            print(f"错误: {error}")
    
    elif args.command == "delete":
        success, error = client.delete_book(args.id)
        if success:
            print(f"书籍 ID={args.id} 已成功删除")
        else:
            print(f"错误: {error}")
    
    elif args.command == "interactive":
        interactive_mode(client)
    
    else:
        parser.print_help()

def interactive_mode(client):
    """交互模式"""
    print("欢迎使用图书管理系统")
    print("输入 'help' 查看可用命令，输入 'exit' 退出")
    
    while True:
        command = input("\n> ").strip().lower()
        
        if command == "exit":
            print("再见!")
            break
        
        elif command == "help":
            print("\n可用命令:")
            print("  list              - 列出所有书籍")
            print("  get <id>          - 获取指定ID的书籍")
            print("  create            - 创建新书籍")
            print("  update <id>       - 更新指定ID的书籍")
            print("  delete <id>       - 删除指定ID的书籍")
            print("  exit              - 退出程序")
            print("  help              - 显示此帮助")
        
        elif command == "list":
            books, error = client.get_all_books()
            if books:
                print_books(books)
            else:
                print(f"错误: {error}")
        
        elif command.startswith("get "):
            parts = command.split(" ", 1)
            if len(parts) == 2:
                book_id = parts[1]
                book, error = client.get_book(book_id)
                if book:
                    print_book(book)
                else:
                    print(f"错误: {error}")
            else:
                print("用法: get <id>")
        
        elif command == "create":
            book_data = get_book_input()
            book, error = client.create_book(book_data)
            if book:
                print("书籍创建成功:")
                print_book(book)
            else:
                print(f"错误: {error}")
        
        elif command.startswith("update "):
            parts = command.split(" ", 1)
            if len(parts) == 2:
                book_id = parts[1]
                book, error = client.get_book(book_id)
                if book:
                    print(f"正在更新书籍 ID={book_id}")
                    print("(保留空白将保持原值不变)")
                    title = input(f"标题 [{book.get('title', '')}]: ")
                    author = input(f"作者 [{book.get('author', '')}]: ")
                    year = input(f"出版年份 [{book.get('publication_year', '')}]: ")
                    isbn = input(f"ISBN [{book.get('isbn', '')}]: ")
                    
                    book_data = {
                        "title": title or book.get("title", ""),
                        "author": author or book.get("author", ""),
                        "publication_year": int(year) if year else book.get("publication_year", 0),
                        "isbn": isbn or book.get("isbn", "")
                    }
                    
                    updated_book, error = client.update_book(book_id, book_data)
                    if updated_book:
                        print("书籍更新成功:")
                        print_book(updated_book)
                    else:
                        print(f"错误: {error}")
                else:
                    print(f"错误: {error}")
            else:
                print("用法: update <id>")
        
        elif command.startswith("delete "):
            parts = command.split(" ", 1)
            if len(parts) == 2:
                book_id = parts[1]
                confirm = input(f"确定要删除书籍 ID={book_id} 吗? (y/n): ")
                if confirm.lower() == 'y':
                    success, error = client.delete_book(book_id)
                    if success:
                        print(f"书籍 ID={book_id} 已成功删除")
                    else:
                        print(f"错误: {error}")
            else:
                print("用法: delete <id>")
        
        else:
            print(f"未知命令: '{command}'")
            print("输入 'help' 查看可用命令")

if __name__ == "__main__":
    main() 