# Investigating Expert Users’ Strategies to Detect Email Signature Spoofing Attacks

This repository contains supplemental material for the paper:

Mayer, P., Pddebniak, D., Fischer, K., Brinkmann, M., Somorovsky, J., Sasse, A., Schinzel, S. and Volkamer, M. “I don’t know why I check this...” - Investigating Expert Users’ Strategies to Detect Email Signature Spoofing Attacks. Eighteenth Symposium on Usable Privacy and Security (SOUPS 2022) (Boston, MA).

Yu can find the paper on the [SOUPS 2022 website](https://www.usenix.org/conference/soups2022/presentation/mayer).

## Overview of this Repository

Each folder in the repository contains specific materials for the study:

**FOSDEM** - The scripts and testcases to replicate the main study

**Questionnaires** - The questionnaires used in pre-study 1 and the main study

**Software** - The versions of Thunderbird and Enigmail used in the main study

## Study Setup

You will need a Linux system to run the main study scripts (other OSes might work but are untested). Pyhon 3 is needed to execute the scripts.

The questionnaires are provided as a [SoSciSurvey](https://www.soscisurvey.de/) project. The XML-file can be directly imported and should be ready to go. Note that the links in the study script need to be updated with the name of you project, though.

### Setup Study Machine (Ubuntu Linux)

**Caution**: We recommend that you create a backup of your `~/.thunderbird` and `~/.gnupg` folders before executing anything from this repository. If you are just looking around, it is better to use a virtual machine.

### Install Dependencies

```sh
sudo apt install curl git ffmpeg
```

### Install Thunderbird 68.4.1

Download Thunderbird 68.4.1 from ...

	https://ftp.mozilla.org/pub/thunderbird/releases/68.4.1

For example, on a x86-64 machine, you can execute ...

```sh
curl -O https://ftp.mozilla.org/pub/thunderbird/releases/68.4.1/linux-x86_64/en-US/thunderbird-68.4.1.tar.bz2
```

Unpack the Thunderbird archive ...

```sh
tar -xf thunderbird-68.4.1.tar.bz2
```

... and include it into your PATH ...

```sh
cd thunderbird-68.4.1
export PATH=`pwd`:$PATH
```

Now, verify that you have the correct version of Thunderbird by calling ...

```sh
thunderbird --version
```

You should see "Thunderbird 68.4.1".

**Note**: You should proceed with the next steps in the same terminal window. Otherwise, make sure to adjust your PATH environment variable again.

## Start the Study

First, checkout the repository with ...

```sh
git clone https://github.com/SecUSo/email-signature-expert-study.git
```

... and change into the "email-signature-expert-study/FOSDEM" folder with ...

```sh
cd email-signature-expert-study/FOSDEM
```

Now, you need to (rename and) copy "thunderbird_genesis" and "gnupg_genesis" to your home directory, i.e., `~/.thunderbird` and `~/.gnupg`. There is a chance that these folders already exist. **Make sure to create a backup** of them and replace them with the `*_genesis` variants. (No commands given here so that a less attentive reader doesn't purge their config by accident :-))

Now, you should be ready to start the study by executing ...

```sh
python3 run_study <your_name>
```

