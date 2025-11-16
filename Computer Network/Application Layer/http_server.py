import http.server
import socketserver
PORT = 12340 # 定义服务器的端口号
Handler = http.server.SimpleHTTPRequestHandler #创建处理器
with socketserver.TCPServer(("172.24.219.249", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

# 运行py文件后，打开浏览器访问http://ip:port/index.html与http://ip:port/abc.html
