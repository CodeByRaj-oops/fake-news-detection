import http.server 
import socketserver 
import threading 
import time 
import requests 
import sys 
import os 
import subprocess 
 
# Configuration 
PORT = int(os.environ.get('PORT', 5000)) 
CHECK_INTERVAL = 60  # seconds 
MAX_RETRIES = 3 
 
def check_backend_health(): 
    """Check if the backend is healthy""" 
    try: 
        response = requests.get(f'http://localhost:{PORT}/health', timeout=5) 
        return response.status_code == 200 
    except Exception as e: 
        print(f"Health check failed: {e}") 
        return False 
 
def restart_backend(): 
    """Restart the backend server""" 
    try: 
        # First try using PM2 
        subprocess.run(['pm2', 'restart', 'fake-news-backend'], check=True) 
        print("Backend restarted with PM2") 
        return True 
    except Exception as e: 
        print(f"Failed to restart with PM2: {e}") 
        # Fall back to direct start 
        try: 
            subprocess.Popen(['python', 'app_new.py'], cwd=os.path.dirname(os.path.abspath(__file__))) 
            print("Backend restarted directly") 
            return True 
        except Exception as e2: 
            print(f"Failed to restart directly: {e2}") 
            return False 
 
def health_checker_thread(): 
    """Thread to periodically check backend health""" 
    failed_checks = 0 
    while True: 
        if check_backend_health(): 
            failed_checks = 0 
            print("Backend health check passed") 
        else: 
            failed_checks += 1 
            print(f"Failed health checks: {failed_checks}/{MAX_RETRIES}") 
            if failed_checks 
                print("Too many failed health checks. Restarting backend...") 
                restart_backend() 
                failed_checks = 0 
        time.sleep(CHECK_INTERVAL) 
 
# Start health checker thread 
health_thread = threading.Thread(target=health_checker_thread, daemon=True) 
health_thread.start() 
 
# Status server to show that the health checker is running 
class HealthHandler(http.server.SimpleHTTPRequestHandler): 
    def do_GET(self): 
        self.send_response(200) 
        self.send_header('Content-type', 'text/html') 
        self.end_headers() 
        self.wfile.write(bytes("<html><body><h1>Health Checker Running</h1>" 
                             "<p>Backend status: " + ("OK" if check_backend_health() else "Not responding") + "</p>" 
                             "</body></html>", "utf-8")) 
 
PORT = 8080 
Handler = HealthHandler 
 
with socketserver.TCPServer(("", PORT), Handler) as httpd: 
    print(f"Health checker monitoring backend on port {PORT}") 
    print(f"View status at http://localhost:{PORT}") 
    try: 
        httpd.serve_forever() 
    except KeyboardInterrupt: 
        pass 
    httpd.server_close() 
