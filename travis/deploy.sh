#!/usr/bin/env bash

set -Eeuo pipefail

git clone https://github.com/navikt/github-apps-support.git
export PATH=`pwd`/github-apps-support/bin:$PATH

GH_TOKEN=$(generate-installation-token.sh `generate-jwt.sh ./travis/di-dep-ci.key.pem $GITHUB_APP_ID`)

echo -e "machine api.github.com login x-access-token password $GH_TOKEN" > ~/.netrc

echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin
docker push $DOCKER_IMG_NAME:$COMMIT_SHORT

PREPROD_NAISERATOR=$(docker run -v ${PWD}:/workdir mikefarah/yq yq r nais.yaml -j)
PREPROD_NAISERATOR=$(echo $PREPROD_NAISERATOR | jq '.spec.image = "'$DOCKER_IMG_NAME':'$COMMIT_SHORT'"' -c)

PREPROD_DEPLOYMENT=$(cat deployment.json | jq '.payload.kubernetes.resources += ['$PREPROD_NAISERATOR']')
PREPROD_DEPLOYMENT=$(echo $PREPROD_DEPLOYMENT | jq '.environment = "dev-fss"')
PREPROD_DEPLOYMENT=$(echo $PREPROD_DEPLOYMENT | jq '.ref = "'$COMMIT_SHORT'"')

curl -i -n \
     -X POST \
     -d "$PREPROD_DEPLOYMENT" \
     -H "Accept: application/vnd.github.ant-man-preview+json" \
     https://api.github.com/repos/navikt/di-dep-kafka-connect/deployments
