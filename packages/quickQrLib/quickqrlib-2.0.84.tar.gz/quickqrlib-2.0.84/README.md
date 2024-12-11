# quickQrLib

quickQrLib is a library for quickqr.

## Notes

This is where we will update the relevant packages that are universal for all
microservices, such as S3BUCKET, etc.

## Setting up PyPi API Key

If you don't have an API Key:

1. Sign in to PyPi, then go to <https://pypi.org/manage/account/token/>
2. Create token, paste it into `api_key.txt`

Note: Create API Key File, i.e., `touch api_key.txt`, in highest dir.

## Deploying

For both `--username` in the scripts MUST be set CORRECTLY FOR API_KEY

### from WSL/Linux/Unix

in `upgradePupgradePackageFull.sh` located in
`twine upload --skip-existing --verbose dist/* --username <username> --password "$API_KEY"`

```bash
chmod +x ./upgradePackageFull.sh
./upgradePackageFull.sh
```

### from Windows

in `update_pypi.bat` located in
`twine upload --skip-existing --verbose dist/* --username <username> --password %API_KEY%`

``` powershell
./upgrade_package_full.bat
```
