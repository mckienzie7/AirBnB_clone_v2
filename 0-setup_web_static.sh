#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static
# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
	apt-get update
	apt-get install -y nginx
fi

# Create necessary folders if not exist
web_static_dir="/data/web_static"
test_dir="/data/web_static/releases/test"
html_file="/data/web_static/releases/test/index.html"

mkdir -p "$web_static_dir/releases" "$web_static_dir/shared" "$test_dir"
touch "$html_file"
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > "$html_file"

# Create symbolic link and set ownership
if [ -L "/data/web_static/current" ]; then
	rm -f "/data/web_static/current"
fi

ln -sf "$test_dir" "/data/web_static/current"
chown -R ubuntu:ubuntu /data/

# Update Nginx configration
nginx_config="/etc/nginx/sites-available/default"
sed -i '/server_name _;/a \\n\tlocation /hbnb_static/ \
	{\n\t\talias /data/web_static/current/;\n\t}\n' "$nginx_config"

# Restart nginx
service nginx restart
