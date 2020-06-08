pipeline {
    agent {
        kubernetes {
            label 'all-python'
	    defaultContainer 'all-python'
        }
    }
    
    environment {
	GIT_LATEST_COMMIT_AUTHOR= sh(
	        returnStdout:true,
        	script: 'git show -s --pretty=%an '
        ).trim()
	GIT_LATEST_COMMIT_MESSAGE= sh(
		returnStdout:true,
		script: 'git log -1 --pretty=%B'
	).trim()
	GIT_STAT= sh(
		returnStdout: true,
		script: "git diff --stat ${get_previous_commit_id().trim()}"
).trim()
	GIT_SHORT_STAT= sh(
		returnStdout: true,
		script: "git diff --shortstat ${get_previous_commit_id().trim()}"
).trim()

	GIT_COMPARE_URL= "${return_github_url().trim()}/compare/${env.GIT_COMMIT.trim()}..${get_previous_commit_id().trim()}" 
	
	}

    parameters {
        string(name: 'SLACK_CHANNEL', defaultValue:'U011V1A6ACE', description: 'slack channel to notify')
           }
    

    stages {

	stage ('Debug') {
		steps {
		sh 'env'
		}
	}
    	
        stage ('Install venv') {
            steps {
                sh 'apt update && apt install -y python3-venv'
            }
        }
        stage ('activate virtual environment') {
            steps {
                sh 'python 3.8 -m venv venv'
		sh 'source venv/bin/activate'
            }
        }
	
        stage ('install requirements') {
            steps {
                sh 'pip install wheel'
		sh 'pip install -r requirements.txt'
		sh 'pip install tox pytest pytest-cov flake8'
            }
        }

	stage ('run tests') {
		steps {
			sh 'flake8'
			sh 'pytest'
			sh 'tox'
		}
	}
    }
    
    post {
        success {
            slackSend color: 'good',
                          message: """
Build ${env.BUILD_NUMBER} completed successfully for ${env.JOB_NAME}.
changes: <${env.RUN_CHANGES_DISPLAY_URL}|here>
Latest Commit: <${return_github_url().trim()}/commit/${env.GIT_COMMIT.trim()}|${env.GIT_LATEST_COMMIT_MESSAGE}>
with id: ${env.GIT_COMMIT}
${env.GIT_SHORT_STAT}
written by ${env.GIT_LATEST_COMMIT_AUTHOR}
<${env.GIT_COMPARE_URL}|Compare against previous build>
More Details <${env.BUILD_URL}|here>
			      """,
			      channel: "${params.SLACK_CHANNEL}"

        }
      failure {
         slackSend color: 'danger',
	    	              message: """
	Build ${env.BUILD_NUMBER} Failed for ${env.JOB_NAME}. 
	changes: <${env.RUN_CHANGES_DISPLAY_URL}|here>
	Latest commit: <${return_github_url().trim()}/commit/${env.GIT_COMMIT.trim()}|${env.GIT_LATEST_COMMIT_MESSAGE}>
	${env.GIT_SHORT_STAT}
	written by ${env.GIT_LATEST_COMMIT_AUTHOR}
	<${env.GIT_COMPARE_URL}|Compare against previous build>
	More Details<${env.BUILD_URL}|here>
			       """,
			       channel:"${params.SLACK_CHANNEL}"

      }
}

}

def return_github_url() {
	def url
	url = sh(script: 'echo "$GIT_URL" | sed -e "s/\\.git[^.]*$//"', returnStdout: true)
	return url.trim()
}

def get_previous_commit_id() {
    if(env.GIT_PREVIOUS_SUCCESSFUL_COMMIT) {
        return env.GIT_PREVIOUS_SUCCESSFUL_COMMIT;
    } else if (env.GIT_PREVIOUS_COMMIT) {
        return env.GIT_PREVIOUS_COMMIT;
    } else {
        return '4b825dc642cb6eb9a060e54bf8d69288fbee4904'; //git magic number for empty tree
    }
}
