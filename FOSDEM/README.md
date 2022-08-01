# Setup

Copy the profiles here to your home folder. Then run `./run_study.py`.

The script will not delete/restore Thunderbird/GnuPG profile folders unless they contain a specific "<random>.canary" file. This is so that the tool does not accidentally destroys profiles.

```
cp gnupg_genesis ~/.gnupg_genesis
cp gnupg_genesis_wkd ~/.gnupg_genesis_wkd
cp thunderbird_genesis ~/.thunderbird_genesis
```
