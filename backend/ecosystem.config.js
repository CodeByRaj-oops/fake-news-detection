module.exports = { 
  apps: [{ 
    name: "fake-news-backend", 
    script: "app_new.py", 
    interpreter: "python", 
    env: { 
      PORT: 5000 
    }, 
    watch: true, 
    ignore_watch: ["__pycache__", "*.pyc", "reports", "history"], 
    max_memory_restart: "500M", 
    autorestart: true, 
    restart_delay: 3000, 
    max_restarts: 10, 
    error_file: "../logs/backend-error.log", 
    out_file: "../logs/backend-output.log", 
  }] 
} 
