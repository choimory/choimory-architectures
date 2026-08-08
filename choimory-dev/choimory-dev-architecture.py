from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Kotlin, Nodejs, Java
from diagrams.programming.framework import Nextjs
from diagrams.onprem.database import Postgresql, MongoDB
from diagrams.onprem.vcs import Github
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.gitops import ArgoCD
from diagrams.k8s.compute import RS, Pod, Deploy
from diagrams.aws.compute import EC2
from diagrams.aws.storage import S3
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.onprem.inmemory import Redis
from diagrams.firebase.grow import FCM
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.logging import Fluentbit, Loki

graph_attr = {
    "splines": "ortho",
    "nodesep": "0.8",
    "ranksep": "1.1",
}

with Diagram("choimory-dev", direction="TB", graph_attr=graph_attr):
    user = Users("user")

    with Cluster("Front"):
        front = Nextjs("client")
        admin = Nextjs("admin")
        user >> [front, admin]

    with Cluster("API Gateway"):
        api_gateway = Nginx("api-gateway")
        [front, admin] >> Edge(weight="100") >> api_gateway

    with Cluster("Member"):
        member_api = Java("member-api") # front <-> api
        member_queue = Java("member-queue") # api <-> api (command)

        member_command = Postgresql("member-command")
        member_query = Elasticsearch("member-query")
        member_redis = Redis("member-redis")
        
        api_gateway >> member_api
    
    with Cluster("Article"):
        article_api = Kotlin("article-api")
        article_queue = Kotlin("article-queue")

        article_command = Postgresql("article-command")
        article_query = Elasticsearch("article-query")
        article_redis = Redis("article-redis")

        api_gateway >> article_api

    with Cluster("Memo"):
        memo_api = Nodejs("memo-api")
        memo_queue = Nodejs("memo-queue")

        memo_command = Postgresql("memo-command")
        memo_query = MongoDB("memo-query")
        memo_redis = Redis("memo-redis")

        api_gateway >> memo_api
    
    with Cluster("Sender"):
        sender_api = Java("sender-api")
        sender_queue = Java("sender-queue")

        sender_command = Postgresql("sender-command")
        sender_query = Elasticsearch("sender-query")

        api_gateway >> sender_api

    with Cluster("Notification"):
        noti_api = Nodejs("noti-api")
        noti_queue = Nodejs("noti-queue")
        noti_socket = Nodejs("noti-socket")

        noti_command = Postgresql("noti-command")
        noti_query = Elasticsearch("noti-query")
        noti_redis = Redis("noti-redis-pubsub")
        noti_fcm = FCM("noti-fcm")

        [front, admin] - noti_socket
        api_gateway >> noti_api
        noti_queue >> noti_redis >> noti_socket
        noti_queue >> noti_fcm

    with Cluster("Message broker"):
        broker = Kafka("broker")

        [member_queue, article_queue, memo_queue, sender_queue, noti_queue] - broker

    with Cluster("CI"):
        github = Github("github")
        github_actions = GithubActions("github-actions")
        dockerhub = Docker("dockerhub")
        gitops_repo = Github("k8s-gitops-repo")

        github >> github_actions
        github_actions >> dockerhub
        github_actions >> gitops_repo

    with Cluster("CD"):
        argo_cd = ArgoCD("argo-cd")
        deploy = Deploy("k8s deploy")
        gitops_repo >> argo_cd >> deploy

        replica = RS("k8s set")
        deploy >> replica

        pod = Pod("k8s pod")
        replica >> pod

    with Cluster("Infra"):
        ec2 = EC2("ec2")       
        s3 = S3("s3")

        pod >> ec2

    with Cluster("Observability"):
        fluent_bit = Fluentbit("fluent-bit")
        loki = Loki("loki")
        prometheus = Prometheus("prometheus")
        grafana = Grafana("grafana")

        pod >> fluent_bit >> loki >> grafana
        fluent_bit >> s3
        pod >> prometheus >> grafana
