/**
 * This pipeline will run a Docker image build
 */

def label = "worker-${UUID.randomUUID().toString()}"
def imageBase = "quay.io/kubernetes-for-developers/flask"
podTemplate(label: label, containers: [
    containerTemplate(name: 'kubectl', image: 'lachlanevenson/k8s-kubectl:v1.8.8', command: 'cat', ttyEnabled: true),
    containerTemplate(name: 'docker', image: 'docker:1.11', ttyEnabled: true, command: 'cat')
  ],
  volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]
  ) {

  node(label) {
    def repository = checkout scm
    def gitCommit = repository.GIT_COMMIT
    def gitBranch = repository.GIT_BRANCH
    def shortCommit = "${gitCommit[0..10]}"
    def previousGitCommit = sh(script: "git rev-parse ${gitCommit}~", returnStdout: true)

    stage('create container image') {
      container('docker') {
        sh """
          docker build -t ${imageBase}:${gitBranch}-${gitCommit} .
        """
      }
    }
    stage('deploy') {
      container('kubectl') {
        sh("kubectl get pods")
      }
    }
  }
}
