import http.server, socketserver, os
os.chdir('/Users/karen/Library/CloudStorage/Dropbox/_DevPlus/_Clients/_Self')
with socketserver.TCPServer(('', 8080), http.server.SimpleHTTPRequestHandler) as s:
    s.serve_forever()
