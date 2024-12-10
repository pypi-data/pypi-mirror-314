
#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

class NginxConfigManager:
    def __init__(self):
        self.sites_available = "/etc/nginx/sites-available"
        self.sites_enabled = "/etc/nginx/sites-enabled"
    def create_config(self):
        print("\n=== Nginx Site Configuration ===")
        
        # Basic Settings
        domain = input("Enter domain name (e.g., example.com): ")
        http_port = input("Enter HTTP port (default 80): ") or "80"
        
        # SSL Settings
        use_ssl = input("Enable SSL? (y/n): ").lower() == 'y'
        ssl_port = "443"
        if use_ssl:
            ssl_port = input("Enter HTTPS port (default 443): ") or "443"
            ssl_cert = input("Enter path to SSL certificate (default: /etc/nginx/ssl/domain.crt): ") or f"/etc/nginx/ssl/{domain}.crt"
            ssl_key = input("Enter path to SSL key (default: /etc/nginx/ssl/domain.key): ") or f"/etc/nginx/ssl/{domain}.key"
            redirect_ssl = input("Redirect HTTP to HTTPS? (y/n): ").lower() == 'y'
        
        # Root Directory Settings
        root_dir = input("Enter root directory (default: /var/www/html): ") or "/var/www/html"
        
        # PHP Support
        php_support = input("Enable PHP support? (y/n): ").lower() == 'y'
        
        # Custom Index Files
        default_index = "index.html index.htm index.nginx-debian.html"
        custom_index = input(f"Enter index files (default: {default_index}): ") or default_index
        
        # Custom Locations
        locations = []
        while input("\nAdd custom location block? (y/n): ").lower() == 'y':
            path = input("Enter location path (e.g., /api): ")
            proxy_pass = input("Enter proxy_pass URL (if any, e.g., http://localhost:3000): ")
            locations.append((path, proxy_pass))
        
        config_content = self._generate_enhanced_config(
            domain=domain,
            http_port=http_port,
            ssl_port=ssl_port,
            use_ssl=use_ssl,
            ssl_cert=ssl_cert if use_ssl else None,
            ssl_key=ssl_key if use_ssl else None,
            redirect_ssl=redirect_ssl if use_ssl else False,
            root_dir=root_dir,
            php_support=php_support,
            custom_index=custom_index,
            locations=locations
        )
        
        config_path = f"{self.sites_available}/{domain}"
        try:
            with open(config_path, 'w') as f:
                f.write(config_content)
            print(f"\nConfiguration created at {config_path}")
        except Exception as e:
            print(f"Error creating config: {e}")

    def _generate_enhanced_config(self, **kwargs):
        config = f"""server {{
        listen {kwargs['http_port']};
        listen [::]:{kwargs['http_port']};
        server_name {kwargs['domain']};
    """

        if kwargs['redirect_ssl']:
            config += f"""
        return 301 https://$server_name:{kwargs['ssl_port']}$request_uri;
    }}

    server {{"""

        if kwargs['use_ssl']:
            config += f"""
        listen {kwargs['ssl_port']} ssl;
        listen [::]:{kwargs['ssl_port']} ssl;
        server_name {kwargs['domain']};
        
        ssl_certificate {kwargs['ssl_cert']};
        ssl_certificate_key {kwargs['ssl_key']};
        
        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        
        # SSL session settings
        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:50m;
        ssl_session_tickets off;
    """

        config += f"""
        root {kwargs['root_dir']};
        index {kwargs['custom_index']};
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN";
        add_header X-Content-Type-Options "nosniff";
        add_header X-XSS-Protection "1; mode=block";
        
        # Logging
        access_log /var/log/nginx/{kwargs['domain']}-access.log;
        error_log /var/log/nginx/{kwargs['domain']}-error.log;
    """

        if kwargs['php_support']:
            config += """
        # PHP-FPM Configuration
        location ~ \.php$ {
            include snippets/fastcgi-php.conf;
            fastcgi_pass unix:/var/run/php/php-fpm.sock;
        }
    """

        # Add custom locations
        for path, proxy_pass in kwargs['locations']:
            config += f"""
        location {path} {{"""
            if proxy_pass:
                config += f"""
            proxy_pass {proxy_pass};
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;"""
            else:
                config += """
            try_files $uri $uri/ =404;"""
            config += """
        }"""

        config += """
        
        location / {
            try_files $uri $uri/ =404;
        }
    }"""
        return config
    def enable_site(self):
        print("\nAvailable sites:")
        sites = os.listdir(self.sites_available)
        for i, site in enumerate(sites, 1):
            print(f"{i}. {site}")
        
        try:
            choice = int(input("\nSelect site number to enable: ")) - 1
            if 0 <= choice < len(sites):
                site = sites[choice]
                target = Path(f"{self.sites_available}/{site}")
                link = Path(f"{self.sites_enabled}/{site}")
                
                if not link.exists():
                    os.symlink(target, link)
                    print(f"Site {site} enabled successfully")
                else:
                    print("Site already enabled")
            else:
                print("Invalid selection")
        except Exception as e:
            print(f"Error enabling site: {e}")

    def install_nginx(self):
        try:
            # Check system package manager
            if os.path.exists("/usr/bin/apt"):
                subprocess.run(["apt", "update"], check=True)
                subprocess.run(["apt", "install", "-y", "nginx"], check=True)
            elif os.path.exists("/usr/bin/dnf"):
                subprocess.run(["dnf", "install", "-y", "nginx"], check=True)
            elif os.path.exists("/usr/bin/yum"):
                subprocess.run(["yum", "install", "-y", "nginx"], check=True)
            print("Nginx installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error installing nginx: {e}")

    def manage_service(self):
        while True:
            print("\nNginx Service Management")
            print("1. Start Nginx")
            print("2. Stop Nginx")
            print("3. Restart Nginx")
            print("4. Check Status")
            print("5. Enable Nginx (start on boot)")
            print("6. Disable Nginx (don't start on boot)")
            print("7. Back to main menu")
            
            choice = input("\nEnter your choice (1-7): ")
            
            try:
                if choice == "1":
                    subprocess.run(["systemctl", "start", "nginx"], check=True)
                    print("Nginx started")
                elif choice == "2":
                    subprocess.run(["systemctl", "stop", "nginx"], check=True)
                    print("Nginx stopped")
                elif choice == "3":
                    subprocess.run(["systemctl", "restart", "nginx"], check=True)
                    print("Nginx restarted")
                elif choice == "4":
                    subprocess.run(["systemctl", "status", "nginx"])
                elif choice == "5":
                    subprocess.run(["systemctl", "enable", "nginx"], check=True)
                    print("Nginx enabled - will start on boot")
                elif choice == "6":
                    subprocess.run(["systemctl", "disable", "nginx"], check=True)
                    print("Nginx disabled - won't start on boot")
                elif choice == "7":
                    break
            except subprocess.CalledProcessError as e:
                print(f"Error managing service: {e}")

    def disable_site(self):
        print("\nEnabled sites:")
        enabled_sites = os.listdir(self.sites_enabled)
        if not enabled_sites:
            print("No enabled sites found")
            return
            
        for i, site in enumerate(enabled_sites, 1):
            print(f"{i}. {site}")
        
        try:
            choice = int(input("\nSelect site number to disable: ")) - 1
            if 0 <= choice < len(enabled_sites):
                site = enabled_sites[choice]
                link_path = Path(f"{self.sites_enabled}/{site}")
                
                if link_path.exists():
                    os.remove(link_path)
                    print(f"Site {site} disabled successfully")
                else:
                    print("Site link not found")
            else:
                print("Invalid selection")
        except Exception as e:
            print(f"Error disabling site: {e}")

    def remove_site(self):
        print("\nAvailable sites:")
        available_sites = os.listdir(self.sites_available)
        if not available_sites:
            print("No sites found")
            return
            
        for i, site in enumerate(available_sites, 1):
            print(f"{i}. {site}")
        
        try:
            choice = int(input("\nSelect site number to remove: ")) - 1
            if 0 <= choice < len(available_sites):
                site = available_sites[choice]
                config_path = Path(f"{self.sites_available}/{site}")
                link_path = Path(f"{self.sites_enabled}/{site}")
                
                # Remove symlink if exists
                if link_path.exists():
                    os.remove(link_path)
                
                # Remove config file
                if config_path.exists():
                    os.remove(config_path)
                    print(f"Site {site} removed successfully")
                else:
                    print("Site config not found")
            else:
                print("Invalid selection")
        except Exception as e:
            print(f"Error removing site: {e}")
    def create_load_balancer(self):
        print("\n=== Load Balancer Configuration ===")
        
        # Basic Settings
        domain = input("Enter load balancer domain (e.g., lb.example.com): ")
        http_port = input("Enter HTTP port (default 80): ") or "80"
        
        # SSL Settings
        use_ssl = input("Enable SSL? (y/n): ").lower() == 'y'
        ssl_port = "443"
        if use_ssl:
            ssl_port = input("Enter HTTPS port (default 443): ") or "443"
            ssl_cert = input("Enter path to SSL certificate: ") or f"/etc/nginx/ssl/{domain}.crt"
            ssl_key = input("Enter path to SSL key: ") or f"/etc/nginx/ssl/{domain}.key"
            redirect_ssl = input("Redirect HTTP to HTTPS? (y/n): ").lower() == 'y'
        
        # Backend Servers
        backends = []
        print("\nAdd backend servers (minimum 2):")
        while len(backends) < 2 or input("\nAdd another backend? (y/n): ").lower() == 'y':
            server = input("Enter backend server (e.g., http://10.0.0.1:8080): ")
            weight = input("Enter server weight (default 1): ") or "1"
            max_fails = input("Enter max fails (default 3): ") or "3"
            fail_timeout = input("Enter fail timeout in seconds (default 30): ") or "30"
            backends.append((server, weight, max_fails, fail_timeout))
        
        # Load Balancing Method
        print("\nSelect load balancing method:")
        print("1. Round Robin (default)")
        print("2. Least Connections")
        print("3. IP Hash")
        print("4. Least Time")
        lb_method = input("Choose method (1-4): ") or "1"
        
        # Session Persistence
        sticky_sessions = input("Enable sticky sessions? (y/n): ").lower() == 'y'
        
        # Health Check Settings
        health_check = input("Configure health checks? (y/n): ").lower() == 'y'
        if health_check:
            health_path = input("Health check path (default /health): ") or "/health"
            check_interval = input("Check interval in seconds (default 5): ") or "5"
            timeout = input("Timeout in seconds (default 3): ") or "3"
        
        config_content = self._generate_lb_config(
            domain=domain,
            http_port=http_port,
            ssl_port=ssl_port if use_ssl else None,
            use_ssl=use_ssl,
            ssl_cert=ssl_cert if use_ssl else None,
            ssl_key=ssl_key if use_ssl else None,
            redirect_ssl=redirect_ssl if use_ssl else False,
            backends=backends,
            lb_method=lb_method,
            sticky_sessions=sticky_sessions,
            health_check=health_check,
            health_settings={
                'path': health_path,
                'interval': check_interval,
                'timeout': timeout
            } if health_check else None
        )
        
        config_path = f"{self.sites_available}/{domain}"
        try:
            with open(config_path, 'w') as f:
                f.write(config_content)
            print(f"\nLoad balancer configuration created at {config_path}")
        except Exception as e:
            print(f"Error creating config: {e}")

    def _generate_lb_config(self, **kwargs):
        # Upstream configuration
        config = "upstream backend_servers {\n"
        
        # Load balancing method
        if kwargs['lb_method'] == "2":
            config += "    least_conn;\n"
        elif kwargs['lb_method'] == "3":
            config += "    ip_hash;\n"
        elif kwargs['lb_method'] == "4":
            config += "    least_time header;\n"
        
        if kwargs['sticky_sessions']:
            config += "    sticky cookie SERVERID expires=1h;\n"
        
        # Backend servers
        for server, weight, max_fails, fail_timeout in kwargs['backends']:
            config += f"    server {server} weight={weight} max_fails={max_fails} fail_timeout={fail_timeout}s;\n"
        
        config += "    keepalive 32;\n"
        config += "}\n\n"
        
        # HTTP Server
        config += f"""server {{
        listen {kwargs['http_port']};
        server_name {kwargs['domain']};
    """

        if kwargs['redirect_ssl']:
            config += f"""
        return 301 https://$server_name:{kwargs['ssl_port']}$request_uri;
    }}

    server {{"""

        # HTTPS Server
        if kwargs['use_ssl']:
            config += f"""
        listen {kwargs['ssl_port']} ssl http2;
        server_name {kwargs['domain']};
        
        ssl_certificate {kwargs['ssl_cert']};
        ssl_certificate_key {kwargs['ssl_key']};
        
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        
        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:50m;
        ssl_session_tickets off;
    """

        # Health Check Location
        if kwargs.get('health_check'):
            config += f"""
        location {kwargs['health_settings']['path']} {{
            access_log off;
            return 200;
            add_header Content-Type text/plain;
        }}"""

        # Main Proxy Configuration
        config += """
        location / {
            proxy_pass http://backend_servers;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
            proxy_connect_timeout 5s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
            proxy_buffering on;
            proxy_buffer_size 8k;
            proxy_buffers 8 8k;
            
            # Enable keepalive
            proxy_set_header Connection "";
        }
        
        # Error pages
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root /usr/share/nginx/html;
        }
    }"""
        
        return config
def main():
    manager = NginxConfigManager()
    
    while True:
        print("\nNginx Configuration Manager")
        print("1. Install Nginx")
        print("2. Manage Nginx Service")
        print("3. Create config")
        print("4. Create Load Balancer")
        print("5. Enable site")
        print("6. Disable site")
        print("7. Remove site")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ")
        
        if choice == "1":
            manager.install_nginx()
        elif choice == "2":
            manager.manage_service()
        elif choice == "3":
            manager.create_config()
        elif choice == "4":
            manager.create_load_balancer()
        elif choice == "5":
            manager.enable_site()
        elif choice == "6":
            manager.disable_site()
        elif choice == "7":
            manager.remove_site()
        elif choice == "8":
            sys.exit(0)
        else:
            print("Invalid choice")
if __name__ == "__main__":
    main()

