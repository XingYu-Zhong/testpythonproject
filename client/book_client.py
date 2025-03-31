import json
import requests
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BookClient:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.books_url = f"{base_url}/books"
    
    def get_all_books(self):
        """获取所有书籍"""
        try:
            response = requests.get(self.books_url)
            response.raise_for_status()
            return response.json().get('data', []), None
        except requests.exceptions.RequestException as e:
            logger.error(f"获取所有书籍时出错: {e}")
            return None, str(e)
        except json.JSONDecodeError:
            logger.error("解析服务器响应时出错")
            return None, "无效的服务器响应"
    
    def get_book(self, book_id):
        """获取单本书籍"""
        try:
            url = f"{self.books_url}/{book_id}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get('data', {}), None
        except requests.exceptions.RequestException as e:
            logger.error(f"获取书籍 ID={book_id} 时出错: {e}")
            return None, str(e)
        except json.JSONDecodeError:
            logger.error("解析服务器响应时出错")
            return None, "无效的服务器响应"
    
    def create_book(self, book_data):
        """创建新书籍"""
        try:
            response = requests.post(
                self.books_url,
                json=book_data,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json().get('data', {}), None
        except requests.exceptions.RequestException as e:
            logger.error(f"创建书籍时出错: {e}")
            return None, str(e)
        except json.JSONDecodeError:
            logger.error("解析服务器响应时出错")
            return None, "无效的服务器响应"
    
    def update_book(self, book_id, book_data):
        """更新书籍"""
        try:
            url = f"{self.books_url}/{book_id}"
            response = requests.put(
                url,
                json=book_data,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json().get('data', {}), None
        except requests.exceptions.RequestException as e:
            logger.error(f"更新书籍 ID={book_id} 时出错: {e}")
            return None, str(e)
        except json.JSONDecodeError:
            logger.error("解析服务器响应时出错")
            return None, "无效的服务器响应"
    
    def delete_book(self, book_id):
        """删除书籍"""
        try:
            url = f"{self.books_url}/{book_id}"
            response = requests.delete(url)
            response.raise_for_status()
            return True, None
        except requests.exceptions.RequestException as e:
            logger.error(f"删除书籍 ID={book_id} 时出错: {e}")
            return False, str(e) 