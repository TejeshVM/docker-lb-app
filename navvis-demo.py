import argparse
import os
import sys
import docker
from itertools import chain

def parse_args(args):
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(dest='command', help='Available Navvis Demo Docker Container Options')
    run_parser = sub_parser.add_parser('run', help='Run Navvis Web Demo Continers with port and unique name')
    run_parser.add_argument('--web-name', type=str, required=True)
    run_parser.add_argument('--web-label', default='navvis-demo-web')
    run_parser.add_argument('--network', default='navvis_demo_web_nw')
    run_parser.add_argument('--web-image', default='navvis-demo')
    run_parser.add_argument('--web-port', type=int, required=True)
    build_parser = sub_parser.add_parser('build', help='Build Navvis Demo web application image')
    build_parser.add_argument('--web-image-label', default='navvis-demo')
    build_parser.add_argument('--docker-file-path', default='navvis-demo')
    deploy_parser = sub_parser.add_parser('deploy', help='Deploy Navvis nginx as Load Balancer')
    deploy_parser.add_argument('--nginx-name', default='navvis-nginx')
    deploy_parser.add_argument('--nginx-label', default='navvis-demo-nginx')
    deploy_parser.add_argument('--network', default='navvis_demo_web_nw')
    deploy_parser.add_argument('--nginx-port', type=int, default=80)
    update_parser = sub_parser.add_parser('update', help='Update all the navvis demo container config to nginx')
    update_parser.add_argument('--web-label', default='type=navvis-demo-web')
    update_parser.add_argument('--nginx-label', default='type=navvis-demo-nginx')
    update_parser.add_argument('--network', default='navvis_demo_web_nw')
    update_parser.add_argument('--template-path', default='navvis-conf.d/navvis-app.conf.tmpl')
    update_parser.add_argument('--destination-path', default='navvis-conf.d/navvis-app.conf')
    return parser.parse_args(args)

def reload_nginx(client, web_servers, args):
    web_server_ips = [container.attrs['NetworkSettings']['Networks'][args.network]['IPAddress']
     for container in web_servers.values()]
    web_server_ports_list = [container.attrs['NetworkSettings']['Ports']
     for container in web_servers.values()]
    web_server_ports_stripped = [elem.strip().split('/tcp') for i in range(len(web_server_ports_list)) for elem in web_server_ports_list[i]]
    web_server_ports_chained = list(chain.from_iterable(web_server_ports_stripped))
    web_server_ports_filtered = filter(None, web_server_ports_chained)
    render_template(web_server_ips, web_server_ports_filtered, args)
    nginx_containers = client.containers.list(filters={'label' : args.nginx_label, 'status': 'running'})
    for container in nginx_containers:
        container.kill(signal='SIGHUP')

def render_template(ips, ports, args):
    upstreams = '\n'.join(['server {}:{};'.format(ips[i], ports[i]) for i in range(len(ips))])
    with open(args.template_path, 'r') as f:
        contents = f.read()
        new_contents = contents.replace('__SERVERS__', upstreams)
        tmp_path = args.destination_path + '.tmp'
        with open(tmp_path, 'w') as tmp_file:
            tmp_file.write(new_contents)
            os.rename(tmp_path, args.destination_path)

def get_currently_running_web_servers(client, args):
    web_containers = client.containers.list(filters={'label': args.web_label, 'status': 'running'})
    return dict([(c.id, c) for c in web_containers])

def get_currently_existing_networks(client, args):
    print args.network
    existing_network = client.networks.list(filters={'name': args.network})
    return existing_network

def update_already_running_containers(client, args):
    web_servers = get_currently_running_web_servers(client, args)
    if web_servers:
        reload_nginx(client, web_servers, args)
    else:
        sys.exit("No Servers Are running still")
    return web_servers

def build_navvis_image(client, args):
    image = client.images.build(path=args.docker_file_path, tag=args.web_image_label)
    print "this is the image details: %s" % (image,)

def deploy_nginx(client, args):
    pwd = os.getcwd()
    path = pwd + "/navvis-conf.d"
    volume_bindings = {path: {'bind': '/etc/nginx/conf.d', 'mode': 'rw'}}
    nginx = client.containers.run('nginx:latest', detach=True, volumes=volume_bindings, ports={args.nginx_port:8080}, name=args.nginx_name, network=args.network, restart_policy={"Name": "always"}, labels={'type': args.nginx_label})
    print nginx

def run_web(client, args):
    cmd = "java -jar -Dserver.port=%s demo-0.0.1-SNAPSHOT.jar" % (args.web_port)
    web = client.containers.run(args.web_image, command=cmd, detach=True, ports={args.web_port:None}, name=args.web_name, network=args.network, restart_policy={"Name": "always"}, labels={'type': args.web_label})


def main(args):
    args = parse_args(args)
    client = docker.from_env()
    if args.command == 'run':
        print "Im in run"
        existing_network = get_currently_existing_networks(client, args)
        if not existing_network:
            client.networks.create(args.network, driver="bridge")
        run_web(client, args)
    elif args.command == 'build':
        print "Im in build"
        build_navvis_image(client, args)
    elif args.command == 'deploy':
        print "Im in deploy"
        existing_network = get_currently_existing_networks(client, args)
        if not existing_network:
            client.networks.create(args.network, driver="bridge")
        deploy_nginx(client, args)
    elif args.command == "update":
        web_servers = update_already_running_containers(client, args)
    else:
        print "Unknown options"

if __name__ == '__main__':
    main(sys.argv[1:])
