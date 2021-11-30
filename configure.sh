#!/bin/sh

set -e

OAUTH_TOKEN="$1"
COMMIT_SHA="$2"

ansible-galaxy install grycap.docker

if ansible-playbook playbook.yaml >ansible.log 2>&1 ; then
   status_summary="success"
   #color="#6DBF59"
   #header="Successful deployment :rocket:"
else
   status_summary="fail"
   #color="#EA4F47"
   #header="Failed deployment :boom:"
fi

GITHUB_COMMIT_URL="https://api.github.com/repos/EGI-Federation/fedcloud-dashboard/commits/$COMMIT_SHA/pulls"

# Find out PR we need to update
ISSUE_NUMBER=$(curl \
                 -H "Authorization: token $OAUTH_TOKEN" \
                 -H "Accept: application/vnd.github.groot-preview+json" \
                 "$GITHUB_COMMIT_URL" | jq .[0].number)

GITHUB_ISSUE_URL="https://api.github.com/repos/EGI-Federation/fedcloud-dashboard/issues/$ISSUE_NUMBER/comments"

{
  echo "### Ansible deployment: \`$status_summary\`"
  echo '<details><summary>Deployment log</summary>'
  echo
  echo '```'
  cat ansible.log
  echo '```'
  echo
  echo '</details>'
} > github_body.txt
echo "{}" | jq --arg b "$(cat github_body.txt)" '{body: $b}' > github_body.json

# Let GitHub know
comment_url=$(curl -X POST \
                -H "Authorization: token $OAUTH_TOKEN" \
                -H "Accept: application/vnd.github.v3+json" \
                "$GITHUB_ISSUE_URL" \
                --data @github_body.json | \
              jq -r .html_url)

# This is here for possible future use
echo "$comment_url"
