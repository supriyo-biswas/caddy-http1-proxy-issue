## Usage:

Clone the repository:

```
git clone https://github.com/supriyo-biswas/caddy-http1-proxy-issue.git
cd caddy-http1-proxy-issue
```

Build and run the app, which will start a server on port 2000:

```
./build-app.sh && ./data/app
```

In another terminal, download the `caddy` binary:

```
docker pull caddy:2.6.4
container_id=$(docker create caddy:2.6.4)
docker cp $container_id:/usr/bin/caddy ./data/caddy
docker rm $container_id
```

Run the `caddy` binary, where `my.web.site` is the domain name of the server running `app.py`.

```
sudo setcap cap_net_bind_service=+ep ./data/caddy
sed 's!__hostname__!my.web.site!' Caddyfile.sample > ./data/Caddyfile
./data/caddy run --config ./data/Caddyfile
```

In a third terminal, run the make-request script to test the reverse_proxy bug:

```
./make-requests.sh my.web.site
```
