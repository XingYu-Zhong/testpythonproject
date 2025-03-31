import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class BookView(BaseHTTPRequestHandler):
    def __init__(self, book_controller, *args, **kwargs):
        self.book_controller = book_controller
        # 必须在最后调用父类的__init__
        # 但由于BaseHTTPRequestHandler不是设计为这样使用的，我们需要通过另一种方式传递controller
        # 所以这个__init__实际上不会被直接调用
        pass
    
    @classmethod
    def create_handler_class(cls, book_controller):
        """创建一个绑定了book_controller的处理器类"""
        def __init__(self, *args, **kwargs):
            self.book_controller = book_controller
            BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        
        # 创建一个新的类
        return type('BoundBookView', (BaseHTTPRequestHandler,), {
            'book_controller': book_controller,
            'do_GET': cls.do_GET,
            'do_POST': cls.do_POST,
            'do_PUT': cls.do_PUT,
            'do_DELETE': cls.do_DELETE,
            '_send_response': cls._send_response,
            '_get_book_id_from_path': cls._get_book_id_from_path,
            '_parse_request_body': cls._parse_request_body
        })
    
    def _send_response(self, status_code, data=None, message=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {}
        if data is not None:
            response['data'] = data
        if message is not None:
            response['message'] = message
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def _get_book_id_from_path(self):
        path = urlparse(self.path).path
        parts = path.strip('/').split('/')
        if len(parts) >= 2 and parts[0] == 'books' and parts[1]:
            return parts[1]
        return None
    
    def _parse_request_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            request_body = self.rfile.read(content_length).decode('utf-8')
            return json.loads(request_body)
        return {}
    
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/books':
            # 获取所有书籍
            books = self.book_controller.get_all_books()
            self._send_response(200, books)
        elif path.startswith('/books/'):
            # 获取单本书籍
            book_id = self._get_book_id_from_path()
            if book_id:
                book, error = self.book_controller.get_book(book_id)
                if book:
                    self._send_response(200, book)
                else:
                    self._send_response(404, message=error)
            else:
                self._send_response(400, message="无效的请求路径")
        else:
            self._send_response(404, message="未找到资源")
    
    def do_POST(self):
        if self.path == '/books':
            try:
                book_data = self._parse_request_body()
                book, error = self.book_controller.create_book(book_data)
                if book:
                    self._send_response(201, book)
                else:
                    self._send_response(400, message=error)
            except json.JSONDecodeError:
                self._send_response(400, message="无效的JSON数据")
        else:
            self._send_response(404, message="未找到资源")
    
    def do_PUT(self):
        if self.path.startswith('/books/'):
            book_id = self._get_book_id_from_path()
            if book_id:
                try:
                    book_data = self._parse_request_body()
                    book, error = self.book_controller.update_book(book_id, book_data)
                    if book:
                        self._send_response(200, book)
                    else:
                        self._send_response(404, message=error)
                except json.JSONDecodeError:
                    self._send_response(400, message="无效的JSON数据")
            else:
                self._send_response(400, message="无效的请求路径")
        else:
            self._send_response(404, message="未找到资源")
    
    def do_DELETE(self):
        if self.path.startswith('/books/'):
            book_id = self._get_book_id_from_path()
            if book_id:
                success, error = self.book_controller.delete_book(book_id)
                if success:
                    self._send_response(204)
                else:
                    self._send_response(404, message=error)
            else:
                self._send_response(400, message="无效的请求路径")
        else:
            self._send_response(404, message="未找到资源") 