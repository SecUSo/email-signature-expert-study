# Investigating Expert Users’ Strategies to Detect Email Signature Spoofing Attacks

This repository contains supplemental material for the the paper:

Mayer, P., Pddebniak, D., Fischer, K., Brinkmann, M., Somorovsky, J., Sasse, A., Schinzel, S. and Volkamer, M. “I don’t know why I check this...” - Investigating Expert Users’ Strategies to Detect Email Signature Spoofing Attacks. Eighteenth Symposium on Usable Privacy and Security (SOUPS 2022) (Boston, MA).

Yu can find the paper on the [SOUPS 2022 website](https://www.usenix.org/conference/soups2022/presentation/mayer).

## Overview of This Repository

Each folder in the repository contains specific materials for the study:

__FOSDEM__ - The scripts and testcases to replicate the main study

**Questionnaires** - The questionnaires used in pre-study 1 and the main study

**Software** - The versions of Thunderbird and Enigmail used in the main study

## Study Setup

You will need a Linux system to run the main study scripts (other OSes might work but are untested). Pyhon 3 is needed to execute the scripts.

The questionnaires are provided as a [SoSciSurvey](https://www.soscisurvey.de/) project. The XML-file can be directly imported and should be ready to go. Note that the links in the study script need to be updated with the name of you project, though.

## Testcases

All test emails are in the "FOSDEM/testcases" folder.

**Caution**: Make a backup of your Thunderbird and GnuPG folders first before executing any script in this repository. Then, replace them with the corresponding "_genesis" folders. Afterwards, the script takes care of everything else.

```sh
$ cp thunderbird_genesis ~/.thunderbird`
$ cp gnupg_genesis ~/.gnupg
$ python run_study.py
```
