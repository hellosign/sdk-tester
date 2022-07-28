@Library('jenkins-lib') _

pipeline {
    agent { label 'sfdc && bionic' }
    //TODO change the parameter
    parameters {
        string(name: 'container', defaultValue: '', description: 'Build parameter to define the container to run the tests')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Specify a different python framework branch to use. Default is main.')
//         booleanParam(name: 'NO_SLACK_NOTIFY', defaultValue: false, description: 'Specify true to avoid sending Slack notifications.')
    }
    environment {
        FRAMEWORK_ROOT_DIR = 'openapi-integration-tests'
        BUILD_USER_EMAIL = 'sfdc+translationupdate@hellosign.com'

        SLACK_API_ID = 'C030GQLB41L'
        SLACK_STAGING_ID = 'CB40P96TX'
        SLACK_QA_ID = 'CB4TEM44F'
        EMAIL_MOBILE_ID = 'mobile-e2e-automation-aaaaeyyjz5tto6vmla35wnwn7y@dropbox.org.slack.com'
    }
    options {
        timeout(time: 10, unit: 'HOURS')
    }
    stages{
        stage('Check branch name') {
            when {
                not {
                    anyOf {
                        branch 'dependabot/**'
                        branch '**/dev/*'
                        branch '**/feature/*'
                        branch 'hs-regression-*'
                        branch 'DEV-*'
                        branch 'main'
                        branch 'release/*'
                    }
                }
            }
            steps {
                script {
                    currentBuild.result = 'ABORTED'
                    error('Not a valid branch')
                }
            }
        }
        stage('SDK Tests') {
           when {
                anyOf {
                    branch 'openapi-integration-tests'
                }
            }
            steps {
                //cancelPreviousBuilds()
                withCredentials([string(credentialsId: 'SFDC-HS-for-SFDC-SFDX-Priv-Key', variable: 'JWT_KEY')]) {
                    script {
                    // TODO fix this
                        if ( "${params.container}" == "" ) {
                            MODULES_TOUSE = "python3 data_python/tests/test_create_account.py"
                        } else {
                            MODULES_TOUSE = ""
                        }
//                         TESTRAIL = checkBranchRequiresTestrail("${params.BRANCH}")
                        sh "./clone_qa_repo.sh ${params.BRANCH}"
//                         decryptSecretFiles("python-e2e-framework/settings/")
//                         sh "sudo chmod -R 0777 python-e2e-framework/settings/"
//                         sh "ls -la python-e2e-framework/settings/"
                        sh script: "${FRAMEWORK_ROOT_DIR}/setup_python_jenkins.sh"
//                         RUN_STR = "${FRAMEWORK_ROOT_DIR}/run_qa_tests.sh ${BUILD_USER_EMAIL} ${params.BUILD_ENV} 0 hsapi '"
                        BUILD_STR = "./python-build"
                        RUN_STR = "${BUILD_USER_EMAIL} ${params.BUILD_ENV} '"
                        RUN_STR += "${MODULES_TOUSE}"
                        echo "${RUN_STR}"
                        echo "${BUILD_STR}"
                        sh script: "${BUILD_STR}", returnStatus: true
                        sh script: "${RUN_STR}", returnStatus: true
                    }
                }
            }
            post {
                always {
                    script {
                        NOTIFY_TOUSE = "${params.BUILD_ENV}-hsapi"
                        def summaryapi = junit allowEmptyResults: true, testResults: '**/hsapi*.xml', skipPublishingChecks: true
                        archiveArtifacts artifacts: 'artifacts/*', allowEmptyArchive: true
                        SEND_RESULT = checkBranchRequiresTestrail("${params.BRANCH}")
                        if ( "${SEND_RESULT}" == "1" ) {
                            echo "HSApi ${NOTIFY_TOUSE}"
                            notifyResult(summaryapi, "${NOTIFY_TOUSE}")
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            deleteDir()
        }
    }
}

@NonCPS
def cancelPreviousBuilds() {
    def jobName = env.JOB_NAME
    def branchName = env.BRANCH_NAME
    def buildNumber = env.BUILD_NUMBER.toInteger()
    /* Get job name */
    def currentJob = Jenkins.instance.getItemByFullName(jobName)

    /* Iterating over the builds for specific job */
    for (def build : currentJob.builds) {
        /* If there is a build that is currently running and it's older and on the same branch, stop it */
        if (build.isBuilding() && build.branch == branchName && build.number.toInteger() < buildNumber) {
            build.doStop()
        }
    }
}

def checkBranchRequiresTestrail(inBranchParam) {
    if (inBranchParam.contains('feature/')) {
        return 0
    } else {
        if (env.BRANCH_NAME.contains('feature/') && inBranchParam == "") {
            return 0
        }
    }
    return 1
}

def getBuildStatus(totalCount, failCount) {
    failMap = [
        "status": "failed",
        "emoji": "heavy_multiplication_x",
        "color": "#FF0000",
    ]
    passMap = [
        "status": "successful",
        "emoji": "heavy_check_mark",
        "color": "#00FF00",
    ]
    if (totalCount.toInteger() == 0) {
        return failMap
    } else if (failCount.toInteger() > 0) {
        return failMap
    } else {
        return passMap
    }
}

def buildMessage(resultsLabel, msgSummary, email='false') {
    buildStatus = getBuildStatus(msgSummary.totalCount, msgSummary.failCount)
    if (email == 'true') {
        messageText = '<b style="font-size:18px;">' + "${resultsLabel} ${buildStatus["status"]}" + '</b><br>'
    } else {
        messageText = ":${buildStatus["emoji"]}: *${resultsLabel} ${buildStatus["status"]}*"
    }
    // Build the message
    echo "Building Test Results notification for '${buildStatus["status"]}' build status..."
    project = java.net.URLDecoder.decode(env.JOB_NAME.substring(10), 'UTF-8')
    shortHash = env.GIT_COMMIT.substring(0, 11)
    if (email == 'true') {
        messageText += '<b style="font-size:18px;">Commit: ' + "${shortHash}" + '<br>'
        messageText += 'Details: ' + "${env.RUN_DISPLAY_URL}" + '<br>'
        messageText += 'Build #' + "${currentBuild.id}" + ' in ' + "${project}" + '</b><br>'
        messageText += '<b style="color:#0049FF;font-size:18px;">Tests: ' + "${msgSummary.totalCount}" + '</b><br>'
        messageText += '<b style="color:#00B503;font-size:18px;">Passed: ' + "${msgSummary.passCount}" + '</b><br>'
        messageText += '<b style="color:red;font-size:18px;">Failures: ' + "${msgSummary.failCount}" + '</b><br>'
        messageText += '<b style="color:orange;font-size:18px;">Skipped: ' + "${msgSummary.skipCount}" + '</b><br>'
    } else {
        messageText += "\nCommit: `${shortHash}`"
        messageText += "\nDetails: <${env.RUN_DISPLAY_URL}|Build #${currentBuild.id} in ${project}>"
        messageText += "\n *Tests: ${msgSummary.totalCount}*\n *Passed: ${msgSummary.passCount}*\n *Failures: ${msgSummary.failCount}*\n *Skipped: ${msgSummary.skipCount}*"
    }
    return messageText
}

def slackNotify(resultsLabel, slackChannelId, summarySlack) {
    buildStatus = getBuildStatus(summarySlack.totalCount, summarySlack.failCount)
    messageText = buildMessage(resultsLabel, summarySlack)
    slackSend channel: slackChannelId, color: buildStatus["color"], message: messageText
}

def emailNotify(resultsLabel, email_to, summaryEmail) {
    buildStatus = getBuildStatus(summaryEmail.totalCount, summaryEmail.failCount)
    subject = "${resultsLabel} ${buildStatus["status"]}: ${summaryEmail.passCount}/${summaryEmail.failCount}/${summaryEmail.skipCount}/${summaryEmail.totalCount} PASS/FAIL/SKIP/TOTAL"
    messageText = buildMessage(resultsLabel, summaryEmail, email='true')
    sh "python-e2e-framework/send_email.sh hs-for-sfdc-qa@hellosign.com \"${email_to}\" \"${subject}\" \'${messageText}\'"
}

def notifyResult (summary, notifyType) {
    if ( params.NO_SLACK_NOTIFY.toBoolean() == false ) {
        if ( notifyType == 'hsprod-hsapi' ) {
            slackNotify('HSApi HS Prod Build', "${env.SLACK_API_ID}", summary)
        } else if ( notifyType == 'hsstaging-hsapi' ) {
            slackNotify('HSApi HS Staging Build', "${env.SLACK_API_ID}", summary)
            //slackNotify('HSApi HS Staging Build', "${env.SLACK_STAGING_ID}", summary)
        } else if ( notifyType == 'hsqa-hsapi' ) {
            slackNotify('HSApi HS QA Build', "${env.SLACK_API_ID}", summary)
            //slackNotify('HSApi HS QA Build', "${env.SLACK_QQ_ID}", summary)
        } else {
            echo "Unhandled notifyType: ${notifyType}"
        }
    }
}
