# Simple Secret Injector CLI tool

[![pypi package](https://badge.fury.io/py/envix.svg)](https://pypi.org/project/envix)

## Support Envs Types
- Raw
- Local
- GoogleCloudSecretManager

## Usage

```sh
cat > envix.toml <<EOF
[envix]
version = 1

[[envs]]
type = "Raw"
[envs.items]
MY_SECRET = '!!!secret!!!!'

EOF

envix inject --clear-environments -- env
```
