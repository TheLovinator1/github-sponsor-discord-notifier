# github-sponsor-discord-notifier

Send a webhook to Discord when someone sponsors you.

<p align="center">
    <img alt="cute spider programming" src="https://github.com/TheLovinator1/github-sponsor-discord-notifier/blob/master/.github/example.png?raw=true" loading="lazy" width="50%" height="50%" />
</p>

## Installation

This is supposed to be run as a Docker container.

### Docker

- Rename `.env.example` to `.env` and fill in the values.
  - Or set your environment variables manually.
- Run `docker-compose up -d` to start the container.
- Add the `github-sponsor-discord-notifier` server behind your reverse proxy.
- Go to `https://github.com/sponsors/<username>/dashboard/webhooks` and add your subdomain as the webhook URL.
  - Example: `https://sponsor.example.com/webhook`
  - Content type: `application/json`
  - No secret required.

### Nginx

```nginx
## Version 2023/11/21
server {
    listen 443 ssl http2;

    server_name sponsor.example.com; # Change this to your subdomain

    include /config/nginx/ssl.conf;

    client_max_body_size 0;

    location / {
        include /config/nginx/proxy.conf;
        include /config/nginx/resolver.conf;
        set $upstream_app github-sponsor-discord-notifier; # Change this to your container name
        set $upstream_port 5000;
        set $upstream_proto http;
        proxy_pass $upstream_proto://$upstream_app:$upstream_port;
    }
}
```
