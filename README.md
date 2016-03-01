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
      * NetTest

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
from nettool.nettest import NetTest as ntest

ntest.convert.netmask.wildcard('255.255.0.0')  # '0.0.255.255'
ntest.convert.wildcard.netmask('0.0.255.255')  # '255.255.0.0'
ntest.convert.netmask.prefix('255.255.0.0')     # 16

ntest.validate.network('10.0.0.0/8')        # True
ntest.validate.ip('10.0.0.1')               # True
ntest.validate.hostname('host.example.com') # True
ntest.validate.netmask('255.255.255.0')     # True
ntest.validate.wildcard('0.0.0.255')        # True
ntest.validate.prefix(27)                   # True

```
