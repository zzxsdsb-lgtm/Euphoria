#!/usr/bin/env python3
"""本地开发服务器：静态文件 + 接收页面 __snap() POST 的画布截图。
用法：python3 tools/server.py  [端口默认 8818]
截图保存到 /tmp/spilled_<name>.png
"""
import http.server
import socketserver
import urllib.parse
import base64
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8818


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 开发服务器：禁用缓存，保证刷新即拿到最新代码
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_POST(self):
        if self.path.startswith("/__snap"):
            q = urllib.parse.urlparse(self.path).query
            name = urllib.parse.parse_qs(q).get("name", ["shot"])[0]
            safe = "".join(ch for ch in name if ch.isalnum() or ch in "_-") or "shot"
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length)
            if data.startswith(b"data:image/png;base64,"):
                data = base64.b64decode(data.split(b",", 1)[1])
            path = f"/tmp/spilled_{safe}.png"
            with open(path, "wb") as f:
                f.write(data)
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"ok")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"serving on http://localhost:{PORT} (snaps -> /tmp/spilled_*.png)")
        httpd.serve_forever()
