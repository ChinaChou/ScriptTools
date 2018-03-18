#coding:utf-8
import docker
import logging
import sys
import urllib3
import json

data = {
    "prod":{
        "fxd-register": [
            ("10.10.10.167","10.10.10.167",5555,"register1.prod.fxds"),
            ("10.10.10.168","10.10.10.168",5555,"register2.prod.fxds"),
            ("10.10.10.169","10.10.10.169",5555,"register3.prod.fxds"),
        ],
        "fxd-config": [
            ("10.10.10.167","10.10.10.167",5557,"config1.prod.fxds"),
            ("10.10.10.168","10.10.10.168",5557,"config2.prod.fxds"),
            ("10.10.10.169","10.10.10.169",5557,"config3.prod.fxds"),
        ],
        "fxd-sleuth": [
            ("10.10.10.167","10.10.10.167",5556,"sleuth1.prod.fxds"),
            ("10.10.10.168","10.10.10.168",5556,"sleuth2.prod.fxds"),
            ("10.10.10.169","10.10.10.169",5556,"sleuth3.prod.fxds"),
        ],
        "fxd-apigateway": [
            ("10.10.10.167","10.10.10.184",8005,"apigateway1.prod.fxds"),
            ("10.10.10.168","10.10.10.188",8005,"apigateway2.prod.fxds"),
            ("10.10.10.169","10.10.10.192",8005,"apigateway3.prod.fxds"),
        ],
        "fxd-membership": [
            ("10.10.10.167","10.10.10.184",8000,"membership1.prod.fxds"),
            ("10.10.10.168","10.10.10.188",8000,"membership2.prod.fxds"),
            ("10.10.10.169","10.10.10.192",8000,"membership3.prod.fxds"),
        ],
        "fxd-secenter": [
            ("10.10.10.167","10.10.10.184",8001,"secenter1.prod.fxds"),
            ("10.10.10.168","10.10.10.188",8001,"secenter2.prod.fxds"),
            ("10.10.10.169","10.10.10.192",8001,"secenter3.prod.fxds"),
        ],
        "fxd-application": [
            ("10.10.10.167","10.10.10.185",8011,"application1.prod.fxds"),
            ("10.10.10.168","10.10.10.189",8011,"application2.prod.fxds"),
            ("10.10.10.169","10.10.10.193",8011,"application3.prod.fxds"),
        ],
        "fxd-order": [
            ("10.10.10.167","10.10.10.185",8010,"order1.prod.fxds"),
            ("10.10.10.168","10.10.10.189",8010,"order2.prod.fxds"),
            ("10.10.10.169","10.10.10.193",8010,"order3.prod.fxds"),
        ],
        "fxd-toolbox": [
            ("10.10.10.167","10.10.10.185",8002,"toolbox1.prod.fxds"),
            ("10.10.10.168","10.10.10.189",8002,"toolbox2.prod.fxds"),
            ("10.10.10.169","10.10.10.193",8002,"toolbox3.prod.fxds"),
        ],
        "fxd-core": [
            ("10.10.10.167","10.10.10.186",8004,"core1.prod.fxds"),
            ("10.10.10.168","10.10.10.190",8004,"core2.prod.fxds"),
            ("10.10.10.169","10.10.10.194",8004,"core3.prod.fxds"),
        ],
        "fxd-product": [
            ("10.10.10.167","10.10.10.186",8008,"product1.prod.fxds"),
            ("10.10.10.168","10.10.10.190",8008,"product2.prod.fxds"),
            ("10.10.10.169","10.10.10.194",8008,"product3.prod.fxds"),
        ],
        "fxd-datacenter": [
            ("10.10.10.167","10.10.10.186",8003,"datacenter1.prod.fxds"),
            ("10.10.10.168","10.10.10.190",8003,"datacenter2.prod.fxds"),
            ("10.10.10.169","10.10.10.194",8003,"datacenter3.prod.fxds"),
        ],
        "fxd-excenter": [
            ("10.10.10.167","10.10.10.187",8012,"excenter1.prod.fxds"),
            ("10.10.10.168","10.10.10.191",8012,"excenter2.prod.fxds"),
            ("10.10.10.169","10.10.10.195",8012,"excenter3.prod.fxds"),
        ],
        "fxd-rcenter": [
            ("10.10.10.167","10.10.10.187",8009,"rcenter1.prod.fxds"),
            ("10.10.10.168","10.10.10.191",8009,"rcenter2.prod.fxds"),
            ("10.10.10.169","10.10.10.195",8009,"rcenter3.prod.fxds"),
        ],
        "fxd-robot": [
            ("10.10.10.167","10.10.10.187",8013,"robot1.prod.fxds"),
            ("10.10.10.168","10.10.10.191",8013,"robot2.prod.fxds"),
            ("10.10.10.169","10.10.10.195",8013,"robot3.prod.fxds"),
        ],
        "fxd-operation": [
            ("10.10.10.167","10.10.10.167",8014,"operation1.prod.fxds"),
            ("10.10.10.168","10.10.10.168",8014,"operation2.prod.fxds"),
            ("10.10.10.169","10.10.10.169",8014,"operation3.prod.fxds"),
        ],
        "fxd-repaycenter": [
            ("10.10.10.167","10.10.10.184",8111,"repaycenter1.prod.fxds"),
            ("10.10.10.168","10.10.10.188",8111,"repaycenter2.prod.fxds"),
            ("10.10.10.169","10.10.10.192",8111,"repaycenter3.prod.fxds"),
        ],
        "fxd-paidcenter": [
            ("10.10.10.167","10.10.10.185",8006,"paidcenter1.prod.fxds"),
            ("10.10.10.168","10.10.10.189",8006,"paidcenter2.prod.fxds"),
            ("10.10.10.169","10.10.10.193",8006,"paidcenter3.prod.fxds"),
        ],
    },
    "uat": {
        "fxd-register": [("10.10.10.163","10.10.10.163",5555,"register.uat.fxds"),],
        "fxd-config": [("10.10.10.164","10.10.10.164",5557,"config.uat.fxds"),],
        "fxd-sleuth": [("10.10.10.165","10.10.10.165",5556,"sleuth.uat.fxds"),],
        "fxd-apigateway": [("192.168.7.75","192.168.7.75",8005,"apigateway.uat.fxds"),],
        "fxd-membership": [("10.10.10.163","10.10.10.163",8000,"membership.uat.fxds"),],
        "fxd-secenter": [("10.10.10.164","10.10.10.164",8001,"secenter.uat.fxds"),],
        "fxd-application":[("10.10.10.165","10.10.10.165",8011,"application.uat.fxds"),],
        "fxd-order": [("192.168.7.75","192.168.7.75",8010,"order.uat.fxds"),],
        "fxd-toolbox": [("10.10.10.163","10.10.10.163",8002,"toolbox.uat.fxds"),],
        "fxd-core": [("10.10.10.164","10.10.10.164",8004,"core.uat.fxds"),],
        "fxd-product": [("10.10.10.165","10.10.10.165",8008,"product.uat.fxds"),],
        "fxd-datacenter": [("192.168.7.75","192.168.7.75",8003,"datacenter.uat.fxds"),],
        "fxd-excenter": [("10.10.10.163","10.10.10.163",8012,"excenter.uat.fxds"),],
        "fxd-rcenter": [("10.10.10.164","10.10.10.164",8009,"rcenter.uat.fxds"),],
        "fxd-robot": [("10.10.10.165","10.10.10.165",8013,"robot.uat.fxds"),],
        "fxd-operation": [("192.168.7.75","192.168.7.75",8014,"operation.uat.fxds"),],
        "fxd-repaycenter": [("192.168.7.75","192.168.7.75",8111,"repaycenter.uat.fxds"),],
        "fxd-paidcenter": [("192.168.7.75","192.168.7.75",8006,"paidcenter.uat.fxds"),],
        "jyd-operation": [("10.10.10.163","10.10.10.163",8015,"jydoperation.uat.fxds"),],
        "fxd-esb": [("10.10.10.61","10.10.10.61",9090,"esb.uat.fxds"),],
        "fxd-omp": [("10.10.10.61","10.10.10.61",9020,"service-omp.uat.fxds"),],
    },
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DockerMgt():
    docker_registry = "dockerhub.prod.fxds"
    docker_username = "pull_user"
    docker_password = "FXD123"
    log_base_dir = "/opt/logs"

    def __init__(self,project_env,project_name):
        self.project_env = project_env
        self.project_name = project_name
        self.logger = self._log_tool()
        self.docker_conn = {}
    
    def _log_tool(self):
        logger = logging.Logger('fxd')
        formatter = logging.Formatter(fmt='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger

    def _gen_docker_conn(self,ip):
        if ip in self.docker_conn:
            return self.docker_conn[ip]
        else:
            try:
                tls_cfg = docker.tls.TLSConfig(ca_cert="/root/.docker/{0}/ca.pem".format(self.project_env),client_cert=("/root/.docker/{0}/cert.pem".format(self.project_env),"/root/.docker/{0}/key.pem".format(self.project_env)))
                client = docker.DockerClient(base_url="tcp://{0}:2376".format(ip),version="auto",tls=tls_cfg)
            except Exception,e:
                self.logger.error(str(e))
                return None
            else:
                self.docker_conn[ip] = client
                return client

    def stop_container(self,client,container_name,container_host):
        try:
            container = client.containers.get(container_name)
        except docker.errors.NotFound,e:
            self.logger.info("容器{0}之前并没有运行过，可能这是您第一次在{1}上发布此服务".format(container_name,container_host))
            return True
        else:
            if container.status in ["running","restarting"]:
                self.logger.warning("container {0} on {1} is in {2} status,so use contianer.stop() to stop it".format(container_name,container_host,container.status))
                container.stop()
                container.reload()
                if container.status != "exited":
                    self.logger.error("Failed to use container.stop() to stop container {0} on {1},so I will use container.kill() to kill it".format(container_name,container_host))
                    container.kill()
                    container.reload()
                    if container.status != "exit":
                        self.logger.error("Failed to use container.kill() to stop container {0} on {1}".format(container_name,container_host))
                        return None
                    else:
                        self.logger.info("Use container.kill() to kill container {0} on {1} success".format(container_name,container_host))
                        return container
                else:
                    self.logger.info("Use container.stop() to stop container {0} on {1} success".format(container_name,container_host))
                    return container
            elif container.status == "paused":
                self.logger.warning("container {0} on {1} is paused,so use contianer.unpause() and container.stop() to stop it".format(container_name,container_host))
                container.unpause()
                container.stop()
                container.reload()
                if container.status != "exited":
                    self.logger.error("Failed to use container.stop() to stop container {0} on {1},so I will use container.kill() to kill it".format(container_name,container_host))
                    container.kill()
                    container.reload()
                    if container.status != "exit":
                        self.logger.error("Failed to use container.kill() to stop container{0} on {1}".format(container_name,container_host))
                        return None
                    else:
                        self.logger.info("Use container.kill() to kill container {0} on {1} success".format(container_name,container_host))
                        return container
                else:
                    self.logger.info("Use container.stop() to stop container {0} on {1} success".format(container_name,container_host))
                    return container
            else:
                self.logger.warning("container {0} on {1} is in {2} status before this deployment".format(container_name,container_host,container.status))
                return container
                
    def remove_container(self,stopped_container,container_host):
        stopped_container.remove()
        try:
            stopped_container.reload()
        except docker.errors.NotFound,e:
            self.logger.info("Delete container {0} on {1} success".format(stopped_container.name,container_host))
            return True
        else:
            return False

    def delete_old_image(self,client,image,container_host):
        try:
            client.images.remove(image)
        except docker.errors.APIError,e:
            self.logger.warning(str(e))
            return True
        except Exception,e:
            self.logger.error("Failed to remove image {0} on {1}".format(image,container_host))
            return False
        else:
            return True

    def Deploy(self):
        if self.project_env not in data:
            self.logger.error("{0} is a invalided env name".format(self.project_env))
            return None
        if self.project_name not in data[self.project_env]:
            self.logger.error("{0} is a invalided project name".format(self.project_name))
            return None
        services = data[self.project_env][self.project_name]
        for s in services:
            self.logger.info("#"*80)
            container_host,service_ip,container_port,container_hostname = s
            container_name = self.project_name + "_" + service_ip + "_" + str(container_port)
            client = self._gen_docker_conn(container_host)
            if client:
                #check if the container_name running
                self.logger.info("Start to stop container {0} on {1}".format(container_name,container_host))
                stopped_container = self.stop_container(client,container_name,container_host)
                if stopped_container is None:
                    self.logger.error("Failed to stop container {0} on {1}, Please check the server,I will abort this deployment".format(container_name,container_host))
                    return None
                
                #remove the old container
                if stopped_container is True:
                    self.logger.info("由于是第一次在服务器{0}上发布{1}服务，所以直接拉取镜像".format(container_host,container_name))
                else:
                    self.logger.info("Start to delete the old container for {0} on {1}".format(container_name,container_host))
                    old_image = stopped_container.image
                    old_image_tags = old_image.tags[0]
                    remove_container_status = self.remove_container(stopped_container,container_host)
                    if not remove_container_status:
                        self.logger.warning("Failed to delete the old container for {0} on {1}".format(container_name,container_host))
                
                    #delete the old image
                    delete_image_status = self.delete_old_image(client,old_image_tags,container_host)
                    if delete_image_status:
                        self.logger.info("Delete old image {0} on {1} success".format(old_image_tags,container_host))

                #pull the new image
                self.logger.info("Start to login docker registry {0}".format(self.docker_registry))
                client.login(username=self.docker_username,password=self.docker_password,registry=self.docker_registry)
                
                #if self.project_name in ["fxd-esb133","fxd-esb134","fxd-omp133","fxd-omp134"]:
                #    self.logger.info("Start to pull {0}/fxd-old-system/{1}_{2}:{3} on {4}".format(self.docker_registry,self.project_env,self.project_name,self.project_tag,container_host))
                #    new_image = client.images.pull(name="{0}/fxd-old-system/{1}_{2}".format(self.docker_registry,self.project_env,self.project_name),tag=self.project_tag)
                #else:
                #    self.logger.info("Start to pull {0}/{1}-fxd-service/{1}_{2}:{3} on {4}".format(self.docker_registry,self.project_env,self.project_name,self.project_tag,container_host))
                #    new_image = client.images.pull(name="{0}/{1}-fxd-service/{1}_{2}".format(self.docker_registry,self.project_env,self.project_name),tag=self.project_tag)

                self.logger.info("Start to pull {0}/prod-fxd-service/prod_{1} on {2}".format(self.docker_registry,self.project_name,container_host))
                new_image = client.images.pull(name="{0}/prod-fxd-service/prod_{1}".format(self.docker_registry,self.project_name),tag="latest")

                #run new container
                self.logger.info("Run new container with {0} on {1}".format(new_image.tags[0],container_host))
                new_container = client.containers.run(
                    image = "{0}".format(new_image.tags[0]),
                    detach = True,
                    hostname = container_hostname,
                    name = container_name,
                    environment = [
                        "project_env={0}".format(self.project_env),
                        "service_port={0}".format(container_port),
                        "project_name={0}".format(self.project_name),
                    ],
                    ports = {
                        "{0}/tcp".format(container_port):(service_ip,container_port)
                    },
                    restart_policy = {
                        "Name":"always",
                        "MaximumRetryCount":5
                    },
                    volumes = {
                        "{0}/{1}".format(self.log_base_dir,container_name): {
                            "bind": "/opt/logs",
                            "mode": "rw"
                        }
                    },
                    extra_hosts = {"public.baofoo.com":"222.73.110.156"}
                )
                new_container.reload()
                if new_container.status != "running":
                    self.logger.error("Failed to run container {0} on {1},the container's status is {2}".format(container_name,container_host,new_container.status))
                    return None
                self.logger.info("Run container {0} on {1} success".format(container_name,container_host))
            else:
                self.logger.error("Connect to {0} via docker api failed".format(container_host))
        
        if self.project_env == 'prod':    
            http = urllib3.PoolManager()
            message_template = {"app_id":1000003,"group_id":4,"message":"{0} 环境中 {1} 已经发布成功".format(self.project_env,self.project_name)}
            jmsg = json.dumps(message_template,ensure_ascii=False)
            rsp = http.request("POST","http://192.168.7.191:3000/sendWx",body=jmsg,headers={"Content-Type":"application/json"})
            if rsp.status == 200:
                self.logger.info("Success to send weixin notice msg")
            else:
                self.logger.warning("Failed to send weixin notice msg")


if __name__ == "__main__":
    try:
        project_env = sys.argv[1]
        project_name = sys.argv[2]
    except Exception,e:
        print(e)
        print("Usage {0} PROJECT_ENV PROJECT_NAME PROJECT_TAG".format(__file__))
        sys.exit(200)
    else:
        deploy = DockerMgt(project_env,project_name)
        deploy.Deploy()
