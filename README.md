# Quince

Virtual TableTop (VTT) combined with a world building tool. Start with a demo collaborative paint as a prove of concept.

Python back, react front (made with Node). Contains host file for nginx.

`python` refers to python3.8 or newer. Older python may work but I haven't tested with one.

Backend install:
1. Install python
2. To install dependencies, run `python -m pip install -r requirements.txt`
3. Make systemd service. Usually done with `ln -s /path/to/this/repo/quince.service /etc/systemd/system`
4. Reload systemd units `systemctl daemon-reload`
5. Turn on the unit `systemctl start quince`

Frontend install:
1. Install nginx
2. Link `quince.conf` to nginx config location. Usually done with `ln -s /path/to/this/repo/quince.conf /etc/nginx/sites-enabled`
3. Change `server_name` in `quince.conf`
4. Reload nginx with `systemctl reload nginx`

When both front and back are operational, site should respond to whatever `server_name` you gave it.
