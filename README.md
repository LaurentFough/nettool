# Network Objects

Python network objects

IT related python objects

Structure
  * netobj
    * host
      * Host
    * nutility
     * NUtility

## Install

```bash
pip install git+git://github.com/heyglen/netobj.git#egg=netobj
```

## Uninstall

```bash
pip uninstall netobj -y
```

# Usage

```python
from netobj.nutility import NUtility as nu

wildcard = nu.convert.netmask.wildcard('255.255.0.0')
# wildcard = '0.0.255.255'
netmask = nu.convert.wildcard.netmask('0.0.255.255')
# netmask = '255.255.0.0'
prefix = nu.convertnetmask.prefix('255.255.0.0')
# prefix = 16

```
