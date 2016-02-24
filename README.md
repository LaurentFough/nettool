# Net Tool

[![Build Status](https://travis-ci.org/heyglen/nettool.svg?branch=master)](https://travis-ci.org/heyglen/nettool)
[![Coverage Status](https://coveralls.io/repos/github/heyglen/nettool/badge.svg?branch=master)](https://coveralls.io/github/heyglen/nettool?branch=master)

Network objects for network admins

Structure
  * nettool
    * host
      * Host
      * Hostname
    * nutility
      * NUtility

## Install

```bash
pip install git+git://github.com/heyglen/nettool.git#egg=nettool
```

## Uninstall

```bash
pip uninstall nettool -y
```

# Example Usage

```python
from nettool.nutility import NUtility as nu

nu.convert.netmask.wildcard('255.255.0.0')  # '0.0.255.255'
nu.convert.wildcard.netmask('0.0.255.255')  # '255.255.0.0'
nu.convert.netmask.prefix('255.255.0.0')     # 16

nu.validate.network('10.0.0.0/8')        # True
nu.validate.ip('10.0.0.1')               # True
nu.validate.hostname('host.example.com') # True
nu.validate.netmask('255.255.255.0')     # True
nu.validate.wildcard('0.0.0.255')        # True
nu.validate.prefix(27)                   # True

```
