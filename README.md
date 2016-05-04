# Net Tool

[![Build Status](https://travis-ci.org/heyglen/nettool.svg?branch=master)](https://travis-ci.org/heyglen/nettool)
[![Coverage Status](https://coveralls.io/repos/github/heyglen/nettool/badge.svg?branch=master)](https://coveralls.io/github/heyglen/nettool?branch=master)

Network objects for network admins


## Install

```bash
pip install git+git://github.com/heyglen/nettool.git#egg=nettool
```

## Uninstall

```bash
pip uninstall nettool -y
```

# Examples

```python
from nettool.nettest import NetTest as ntest

ntest.convert.string.cidr('1.2.3.1/24')                 # '1.2.3.0/24'
ntest.convert.string.cidr('1.2.3.0 255.255.255.0')      # '1.2.3.0/24'
ntest.convert.string.cidr('1.2.3.0 255.255.255.255')    # '1.2.3.0/32'
ntest.convert.string.cidr('1.2.3.0 0.0.0.255')          # '1.2.3.0/24'

ntest.convert.string.ip('1.2.3.1/24')                   # '1.2.3.1'
ntest.convert.string.ip('1.2.3.0 255.255.255.0')        # '1.2.3.0'
ntest.convert.string.ip('1.2.3.0 255.255.255.255')      # '1.2.3.0'
ntest.convert.string.ip('1.2.3.0 0.0.0.255')            # '1.2.3.0'

ntest.convert.netmask.wildcard('255.255.0.0')           # '0.0.255.255'
ntest.convert.wildcard.netmask('0.0.255.255')           # '255.255.0.0'
ntest.convert.netmask.prefix('255.255.0.0')             # 16

ntest.validate.network('10.0.0.0/8')                    # True
ntest.validate.ip('10.0.0.1')                           # True
ntest.validate.hostname('host.example.com')             # True
ntest.validate.netmask('255.255.255.0')                 # True
ntest.validate.wildcard('0.0.0.255')                    # True
ntest.validate.prefix(27)                               # True

ntest.validate.network('1.2.3.4/32')                    # True
ntest.validate.network('1.2.3.4/0')                     # True
ntest.validate.network('1.2.3.4')                       # True
ntest.validate.network(u'1.2.3.4')                      # True
ntest.validate.network(u'1.2.3.0 255.255.255.0')        # True
ntest.validate.network(u'1.2.3.0 0.0.0.255')            # True
```
