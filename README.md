# Net Tool

Network objects for network admins

Structure
  * nettool
    * host
      * Host
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

# Usage

```python
from nettool.nutility import NUtility as nu

wildcard = nu.convert.netmask.wildcard('255.255.0.0')
# wildcard = '0.0.255.255'
netmask = nu.convert.wildcard.netmask('0.0.255.255')
# netmask = '255.255.0.0'
prefix = nu.convertnetmask.prefix('255.255.0.0')
# prefix = 16

```
