from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Kotlin, Nodejs, Java
from diagrams.programming.framework import Nextjs
from diagrams.onprem.database import Postgresql, MongoDB
from diagrams.onprem.vcs import Github
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import GithubActions
from diagrams.k8s.compute import RS, Pod, Deploy
from diagrams.aws.compute import EC2
from diagrams.aws.storage import S3
from diagrams.elastic.elasticsearch import Elasticsearch, LogStash, Kibana
from diagrams.onprem.inmemory import Redis
from diagrams.firebase.grow import FCM
from diagrams.onprem.monitoring import Prometheus, Grafana

with Diagram("choimory-dev", direction="TB"):
    user = Users("user")

    with Cluster("Front"):
        front = Nextjs("client")
        user >> front

    with Cluster("Member"):
        member_api = Kotlin("member-api") # front <-> api
        member_queue = Kotlin("member-queue") # api <-> api (command)

        member_command = Postgresql("member-command")
        member_query = Elasticsearch("member-query")
        member_redis = Redis("member-redis")
        
        front >> member_api
    
    with Cluster("Article"):
        article_api = Kotlin("article-api")
        article_queue = Kotlin("article-queue")

        article_command = Postgresql("article-command")
        article_query = Elasticsearch("article-query")
        article_redis = Redis("article-redis")

        front >> article_api

    with Cluster("Memo"):
        memo_api = Nodejs("memo-api")
        memo_queue = Nodejs("memo-queue")

        memo_command = Postgresql("memo-command")
        memo_query = MongoDB("memo-query")
        memo_redis = Redis("memo-redis")

        front >> memo_api
    
    with Cluster("Sender"):
        sender_queue = Kotlin("sender-queue")

        sender_command = Postgresql("sender-command")
        sender_query = MongoDB("sender-query")
        sender_redis = Redis("sender-redis")

        [member_api, article_api, memo_api] >> sender_queue

    with Cluster("Notification"):
        noti_api = Nodejs("noti-api")
        noti_queue = Nodejs("noti-queue")
        noti_socket = Nodejs("noti-socket")

        noti_command = Postgresql("noti-command")
        noti_query = Elasticsearch("noti-query")
        noti_redis = Redis("noti-redis-pubsub")
        noti_fcm = FCM("noti-fcm")

        front - noti_socket
        front >> noti_api
        noti_queue >> noti_redis >> noti_socket
        noti_queue >> noti_fcm

    with Cluster("Message broker"):
        broker = Kafka("broker")

        [member_queue, article_queue, memo_queue, sender_queue, noti_queue] - broker

    with Cluster("Logging"):
        logstash = LogStash("logstash")
        elasticsearch = Elasticsearch("elasticsearch")
        kibana = Kibana("kibana")

        logstash >> elasticsearch
        elasticsearch >> kibana        

    with Cluster("Monitoring"):
        prometheus = Prometheus("prometheus")
        grafana = Grafana("grafana")

        prometheus >> grafana

    with Cluster("CI"):
        github = Github("github")

        github_actions = GithubActions("github-actions")
        github >> github_actions

    with Cluster("CD"):
        docker = Docker("docker")
        github_actions >> docker

        deploy = Deploy("k8s deploy")
        docker >> deploy

        replica = RS("k8s set")
        deploy >> replica

        pod = Pod("k8s pod")
        replica >> pod

    with Cluster("Infra"):
        ec2 = EC2("ec2")       
        s3 = S3("s3")

        pod >> ec2