from http.server import BaseHTTPRequestHandler
from jinja2 import Template


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        self.respond()

    def do_POST(self):
        return

    def handle_http(self):
        status = 200
        content_type = 'text/html'
        response_content = ""

        route_content = 'index.html'

        # response_content = open(route_content)
        # response_content = response_content.read()

        html_file = open(route_content)
        template = Template(html_file.read())
        response_content = template.render(url=self.headers['HOST'])

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes(response_content, 'UTF-8')

    def respond(self):
        content = self.handle_http()
        self.wfile.write(content)