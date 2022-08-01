# Investigating Expert Users’ Strategies to Detect Email Signature Spoofing Attacks

All test emails are in the "FOSDEM/testcases" folder.

**Caution**: Make a backup of your Thunderbird and GnuPG folders first before executing any script in this repository. Then, replace them with the corresponding "_genesis" folders. Afterwards, the script takes care of everything else.

```sh
$ cp thunderbird_genesis ~/.thunderbird`
$ cp gnupg_genesis ~/.gnupg
$ python run_study.py
```
