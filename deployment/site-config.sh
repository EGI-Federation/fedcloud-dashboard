#!/bin/sh

set -ex

# builds the clouds.yaml file needed for OpenStack clients
# Reads from config.yaml the clouds to use

dump_config() {
    # dumps a piece of yaml ready to be included in the
    # clouds.yaml Openstack client config
    cloud_name="$1"
    site="$2"
    vo="$3"
    oidc_token="$4"
    token="$(fedcloud openstack token issue \
                      --oidc-access-token "$oidc_token" \
                      --site "$site" --vo "$vo" -j \
                      | jq -r '.[0].Result.id')"
    eval "$(fedcloud site show-project-id --site "$site" --vo "$vo")"
    cat << EOF
  $cloud_name:
    auth_type: token
    auth:
      auth_url: $OS_AUTH_URL
      token: $token
      project_id: $OS_PROJECT_ID
EOF
}

OIDC_TOKEN=$(mytoken AT --MT-env MYTOKEN)

echo "::add-mask::$OIDC_TOKEN"

rm -f clouds.yaml
echo "clouds:" > tmp-clouds.yaml
dump_config backend \
            "$(yq -r .clouds.backend.site config.yaml)" \
            "$(yq -r .clouds.backend.vo config.yaml)" \
            "$OIDC_TOKEN" >> tmp-clouds.yaml

dump_config deploy \
            "$(yq -r .clouds.deploy.site config.yaml)" \
            "$(yq -r .clouds.deploy.vo config.yaml)" \
            "$OIDC_TOKEN" >> tmp-clouds.yaml

mv tmp-clouds.yaml clouds.yaml
mkdir -p ~/.config/openstack
