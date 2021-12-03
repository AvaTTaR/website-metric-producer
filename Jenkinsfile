pipeline {
    agent {
        kubernetes {
        defaultContainer 'kaniko'
        yaml '''
        kind: Pod
        spec:
          containers:
          - name: kubectl
            image: joshendriks/alpine-k8s
            command:
            - sleep
            args:
            - 99d
            volumeMounts:
            - name: kube-conf-map
              mountPath: /root/.kube/config
              subPath: config
          - name: kaniko
            image: gcr.io/kaniko-project/executor:v1.6.0-debug
            imagePullPolicy: Always
            command:
            - sleep
            args:
            - 99d
            volumeMounts:
              - name: jenkins-docker-cfg
                mountPath: /kaniko/.docker
          volumes:
          - name: kube-conf-map
            configMap:
              name: kube-conf-map
          - name: jenkins-docker-cfg
            projected:
              sources:
              - secret:
                  name: docker-credentials
                  items:
                    - key: .dockerconfigjson
                      path: config.json
            '''
        }
    }
    triggers {
        pollSCM('* * * * *')
        githubPush()
    }
    stages {
        stage('Build image'){
            steps {
                checkout scm
                //git url: 'https://github.com/AvaTTaR/website-metric-producer.git', branch: 'main'
                sh '/kaniko/executor --context "`pwd`" --destination avattar/fp-app-met:${BUILD_NUMBER}'
            }
        }
        stage('Deploy') {
            steps {
                container('kubectl') {
                checkout scm
                //git url: 'https://github.com/AvaTTaR/website-metric-producer.git', branch: 'main'
                    sh '''
                    if [[ "$(kubectl -n application-met get deploy)" ]]
                    then
                        if [[ "$(cat redeploy.txt)" == "1" ]]
                        then
                            echo "Redeploy is set to 1. clean kafka topic and deploy with --force-init-db"
                            kubectl -n kafka exec -it kafka-0 -- /opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka.kafka.svc.cluster.local:9092 --delete --topic app-met-topic
                            sed -i "s/<APP_COMMAND>/--force-init-db run/" deployment.yaml
                            sed -i "s/<TAG>/${BUILD_NUMBER}/" deployment.yaml
                            kubectl apply -f deployment.yaml
                            kubectl wait --for=condition=available --timeout=180s deployment/app-met -n application-met
                            echo Deploy started, changing env.
                            kubectl set env deployment app-met APP_COMAND=run -n application-met
                        else
                            echo "Redeploy is not enabled"
                            sed -i "s/<APP_COMMAND>/run/" deployment.yaml
                            sed -i "s/<TAG>/${BUILD_NUMBER}/" deployment.yaml
                            kubectl apply -f deployment.yaml
                        fi
                    else
                        echo "There is no active application instances, deploing"
                        sed -i "s/<APP_COMMAND>/--force-init-db run/" deployment.yaml
                        sed -i "s/<TAG>/${BUILD_NUMBER}/" deployment.yaml
                        kubectl apply -f deployment.yaml
                        kubectl wait --for=condition=available --timeout=180s deployment/app-met -n application-met
                        echo "Deploy started, changing env."
                        kubectl set env deployment app-met APP_COMAND=run -n application-met
                      
                   fi
                  '''
                }
            }
        }
    }
}