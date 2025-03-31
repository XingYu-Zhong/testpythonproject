import socket
from http.server import HTTPServer
import threading
import json
import logging

from server.models import Database
from server.controllers import BookController
from server.views import BookView

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BookServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.database = Database()
        self.controller = BookController(self.database)
        self.server = None
        self.server_thread = None
        self._add_sample_data()
    
    def _add_sample_data(self):
        """添加一些示例数据"""
        sample_books = [
            {
                "title": "Python编程", 
                "author": "张三", 
                "publication_year": 2020, 
                "isbn": "9787111612727"
            },
            {
                "title": "深入理解计算机系统", 
                "author": "李四", 
                "publication_year": 2018, 
                "isbn": "9787111544937"
            },
            {
                "title": "算法导论", 
                "author": "王五", 
                "publication_year": 2019, 
                "isbn": "9787111407010"
            }
        ]
        
        for book_data in sample_books:
            self.controller.create_book(book_data)
    
    def start(self):
        """启动HTTP服务器"""
        try:
            handler = BookView.create_handler_class(self.controller)
            self.server = HTTPServer((self.host, self.port), handler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            logger.info(f"服务器已启动在 http://{self.host}:{self.port}")
            logger.info("按 Ctrl+C 停止服务器")
            
            return True
        except socket.error as e:
            logger.error(f"启动服务器时出错: {e}")
            return False
    
    def stop(self):
        """停止HTTP服务器"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            logger.info("服务器已停止")

def main():
    server = BookServer()
    try:
        if server.start():
            # 让主线程等待，直到用户按Ctrl+C
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                pass
    finally:
        server.stop()

if __name__ == '__main__':
    main() 