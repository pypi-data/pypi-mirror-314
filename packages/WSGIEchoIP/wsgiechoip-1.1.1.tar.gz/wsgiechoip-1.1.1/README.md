# WSGIEchoIP

```
$ curl -L ip.jb2170.com
12.34.56.78
```

A simple WSGI app that returns the value of the `X-Forwarded-For` header, so one can get their public IP address.

No more need for `$ curl -L -D - ipconfig.org` and its unnecessary cookies!

This is a useful 'just-werks' app, and demonstrates using WSGI without a framework such as Flask. The only thing to really be aware of in raw WSGI is that strings are bytes decoded as Latin-1, as per [PEP-3333](https://peps.python.org/pep-3333/), when in reality there's a 99% chance the bytes should've been decoded as UTF-8. Therefore if one is concerned about Unicode headers etc the WSGI environment strings should be corrected with `.encode("latin1").decode("utf8")`. This is one of the many reasons to use a framework like Flask in a production app.

## Installing

I run this as a reverse proxy via Apache. Example systemd unit files and friends are in `daemon-files` of this repo

- create a venv, say in `~/.local/var/lib/WSGIEchoIP`, and source it
- `$ pip install WSGIEchoIP gunicorn`
- place the systemd unit file and shell script into the correct folders, for example I use `~/.local/var/lib/systemd/{etc/user,usr/bin}`
- place the `.htaccess` file in the public http folder corresponding to the domain you want to serve the app from
- adjust the unix socket path in the `.htaccess` file and `.service` unit

Make sure you have the `headers`, `proxy`, and `proxy_http` modules enabled for Apache!

You can probably figure out the rest, enabling / starting the systemd service...

## Customizing

Setting the environment variable `FORWARDED_IP_HEADER_NAME=X-Sneed-Chuck` makes the app return the `X-Sneed-Chuck` header value instead. (perhaps nginx uses something different than `X-Forwarded-For`.)

## See also

- [FlaskEchoIP](https://github.com/jb2170/FlaskEchoIP/), a Flask version of this app that I also made, which is why this one is now archived
