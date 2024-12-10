[![PyPI](https://img.shields.io/pypi/v/pybashproof)](https://pypi.org/project/pybashproof/)
![Python Version](https://img.shields.io/badge/Python-3.6-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# bashproof

This little project is just a conceptual work used for my thesis about documentation of forensic processes.

It's purpose is to log the input/output of the bash terminal in a readable and evidentiary way. Forensic staff would be able to prove any of their actions when confronted with digital evidence.

However, this project is just a CONCEPT - it only shows how one step of documentation COULD be done as a small part of the whole project. One problem is that the script does not directly start an interactive shell in the traditional sense, but simulates one by creating a custom shell-like environment. A sub-process is used to pipe the input to bash and receive stdout/stderr accordingly. Because of this, you cannot use auto-completion. Also, I have not tested complex input.

There is the Linux `script` utility, but it lacks good timestamping and readability.

# Usage

- Run with `bashproof`
- Stores log in your home dir `bashproof.log`
- Leave Session with `CTRL+C`
- Close Case with `bashproof --close`
  - Renames to `bashproof_closed.log`
  - Creates `bashproof_sha256.log` with SHA for `bashproof.log`

# Example log

```
[2024-12-09 11:27:01] 
[2024-12-09 11:27:01] ----------------------------------
[2024-12-09 11:27:01] STARTED SHELL-TRACKING
[2024-12-09 11:27:01] ----------------------------------
[2024-12-09 11:27:01] HOST: somehost; USER: someuser
[2024-12-09 11:27:01] ----------------------------------
[2024-12-09 11:27:01] 
[2024-12-09 11:27:09] --> [ stdIN] lsblk
[2024-12-09 11:27:09] ────────────────────────────────────────────────────
[2024-12-09 11:27:09] <-- [stdOUT] NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
[2024-12-09 11:27:09] <-- [stdOUT] device0     259:0    0 XXXXXX  0 disk
[2024-12-09 11:27:09] <-- [stdOUT] ├─device0p1 259:1    0   XXXM  0 part /boot/efi
[2024-12-09 11:27:09] <-- [stdOUT] ├─device0p2 259:2    0 XXXXXG  0 part /var/log
[2024-12-09 11:27:09] <-- [stdOUT] │                                     /home
[2024-12-09 11:27:09] <-- [stdOUT] │                                     /var/cache
[2024-12-09 11:27:09] <-- [stdOUT] │                                     /
[2024-12-09 11:27:09] <-- [stdOUT] ├─device0p3 259:3    0    XXM  0 part
[2024-12-09 11:27:09] <-- [stdOUT] └─device0p4 259:4    0 XXXXXG  0 part
[2024-12-09 11:27:09] ────────────────────────────────────────────────────
[2024-12-09 11:27:25] --> [ stdIN] wget google.com
[2024-12-09 11:27:25] ────────────────────────────────────────────────────
[2024-12-09 11:27:25] <-- [stdERR] --2024-12-09 11:27:25--  http://google.com/
[2024-12-09 11:27:25] <-- [stdERR] Resolving google.com (google.com)... 0000:0000:0000:000::0000, 172.217.16.174
[2024-12-09 11:27:25] <-- [stdERR] Connecting to google.com (google.com)|0000:0000:0000:000::0000|:80... connected.
[2024-12-09 11:27:25] <-- [stdERR] HTTP request sent, awaiting response... 301 Moved Permanently
[2024-12-09 11:27:25] <-- [stdERR] Location: http://www.google.com/ [following]
[2024-12-09 11:27:25] <-- [stdERR] --2024-12-09 11:27:25--  http://www.google.com/
[2024-12-09 11:27:25] <-- [stdERR] Resolving www.google.com (www.google.com)... 0000:0000:0000:000::0000, 142.251.37.4
[2024-12-09 11:27:25] <-- [stdERR] Connecting to www.google.com (www.google.com)|0000:0000:0000:000::0000|:80... connected.
[2024-12-09 11:27:25] <-- [stdERR] HTTP request sent, awaiting response... 200 OK
[2024-12-09 11:27:25] <-- [stdERR] Length: unspecified [text/html]
[2024-12-09 11:27:25] <-- [stdERR] Saving to: ‘index.html’
[2024-12-09 11:27:25] <-- [stdERR] 
[2024-12-09 11:27:25] <-- [stdERR] 0K .......... .........                                    376K=0,05s
[2024-12-09 11:27:25] <-- [stdERR] 
[2024-12-09 11:27:25] <-- [stdERR] 2024-12-09 11:27:25 (376 KB/s) - ‘index.html’ saved [19563]
[2024-12-09 11:27:25] <-- [stdERR] 
[2024-12-09 11:27:25] ────────────────────────────────────────────────────
[2024-12-09 11:27:30] 
[2024-12-09 11:27:30] ----------------------------------
[2024-12-09 11:27:30] TERMINATED SHELL-TRACKING
[2024-12-09 11:27:30] ----------------------------------
[2024-12-09 11:27:32] ----------------------------------
[2024-12-09 11:27:32] ------------ CASE DONE -----------
```