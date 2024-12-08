# bitbucket-cloud-client
python sdk for bitbucket cloud rest api


#### Install me:  

```bash
pip install -i https://test.pypi.org/simple/ bitbucket-cloud-client-foolishnekozzz
```

#### Examples:  

```bash
export BITBUCKET_WORKSPACE="neko"
export BITBUCKET_USERNAME="neko"
export BITBUCKET_PASSWORD="neko"
```

```python
#!/usr/bin/env python3

from bitbucket_cloud_client_foolishnekozzz import BitbucketWorkspace, BitbucketGroup, Member

from os import environ

workspace = BitbucketWorkspace(name=environ.get("BITBUCKET_WORKSPACE"))
workspace.get_groups()

#docs:https://support.atlassian.com/user-management/docs/default-groups-and-permissions/
default_group = BitbucketGroup(name="default", workspace=workspace)

default_group.get_members()

for i in default_group.members:
    print(i)
```