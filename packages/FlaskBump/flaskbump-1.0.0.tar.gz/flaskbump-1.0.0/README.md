# FlaskBump

```
$ curl -L bump.area51.jb2170.com
1989
$ curl -L bump.area51.jb2170.com
1990
$ curl -L bump.area51.jb2170.com
1991
```

A simple Flask app that counts the number of requests to it, a visitor count perchance

## Installing

I run this as a reverse proxy via Apache. Example systemd unit files and friends are in `daemon-files` of this repo

- create a venv, say in `~/.local/var/lib/FlaskBump`, and source it
- `$ pip install FlaskBump gunicorn`
- place the systemd unit file and shell script into the correct folders, for example I use `~/.local/var/lib/systemd/{etc/user,usr/bin}`
- place the `.htaccess` file in the public http folder corresponding to the domain you want to serve the app from
- adjust the unix socket path in the `.htaccess` file and `.service` unit
- copy the default `state.json` file from `daemon-files` into the app's working directory (as specified as `WorkingDirectory` in the `.service` file)

Make sure you have the `headers`, `proxy`, and `proxy_http` modules enabled for Apache!

You can probably figure out the rest, enabling / starting the systemd service...
