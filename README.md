# Prerequistes

To run this python script, please do install 
1. python 2.7.15+ 
2. pip install -r requirements.txt

# All Available options:

```
$ python navvis-demo.py --help
usage: navvis-demo.py [-h] {run,build,deploy,update} ...

positional arguments:
  {run,build,deploy,update}
                        Available Navvis Demo Docker Container Options
    run                 Run Navvis Web Demo Continers with port and unique
                        name
    build               Build Navvis Demo web application image
    deploy              Deploy Navvis nginx as Load Balancer
    update              Update all the navvis demo container config to nginx

optional arguments:
  -h, --help            show this help message and exit

```
# Deploy nginx Container with basic configuration:

```
$ python navvis-demo.py deploy --help
usage: navvis-demo.py deploy [-h] [--nginx-name NGINX_NAME]
                             [--nginx-label NGINX_LABEL] [--network NETWORK]
                             [--nginx-port NGINX_PORT]

optional arguments:
  -h, --help            show this help message and exit
  --nginx-name NGINX_NAME
  --nginx-label NGINX_LABEL
  --network NETWORK
  --nginx-port NGINX_PORT

```

# Build Navvis Demo application container image

```
$ python navvis-demo.py build --help
usage: navvis-demo.py build [-h] [--web-image-label WEB_IMAGE_LABEL]
                            [--docker-file-path DOCKER_FILE_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --web-image-label WEB_IMAGE_LABEL
  --docker-file-path DOCKER_FILE_PATH
```

# Run Navvis Demo application 
```
$ python navvis-demo.py run --help
usage: navvis-demo.py run [-h] --web-name WEB_NAME [--web-label WEB_LABEL]
                          [--network NETWORK] [--web-image WEB_IMAGE]
                          --web-port WEB_PORT

optional arguments:
  -h, --help            show this help message and exit
  --web-name WEB_NAME
  --web-label WEB_LABEL
  --network NETWORK
  --web-image WEB_IMAGE
  --web-port WEB_PORT
```
# Update nginx Configuration and reload nginx

```
$ python navvis-demo.py update --help
usage: navvis-demo.py update [-h] [--web-label WEB_LABEL]
                             [--nginx-label NGINX_LABEL] [--network NETWORK]
                             [--template-path TEMPLATE_PATH]
                             [--destination-path DESTINATION_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --web-label WEB_LABEL
  --nginx-label NGINX_LABEL
  --network NETWORK
  --template-path TEMPLATE_PATH
  --destination-path DESTINATION_PATH
```

# TO-DO:
1. Error handling in each and every scenario with proper messages.
2. Build Customised nginx configuration files with enhanced templates.
