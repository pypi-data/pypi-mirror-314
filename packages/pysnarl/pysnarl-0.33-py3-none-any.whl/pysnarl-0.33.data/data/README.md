# PySnarl

PySnarl python lib, Send SNP/3.1 messages. (Snarl)

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

$ pip install pysnarl

pysnarl supports Python 3 and newer

## Example

use as module/lib

```python
from pysnarl import Snarl
Snarl.send("REGISTER", 'test_app', 'TEST', icon = 'snarl.png', '127.0.0.1', 9899, verbose = True)
Snarl.send("NOTIFY", 'test_app', 'TEST', 'TEST MESSAGE', 'snarl.png', '127.0.0.1', 9899, priority = 1, verbose = True)
```

outputs:
```bash
[SNP/3.1 REGISTER
app-id: test_app
title: TEST
icon: snarl.png
END]
request xxx: SNP/3.1 REGISTER
app-id: test_app
title: TEST
icon: snarl.png
END

result: [SNP/3.1 SUCCESS
END]

[SNP/3.1 NOTIFY
app-id: test_app
title: TEST
text: TEST MESSAGE
icon: snarl.png
priority: 1
END]
request xxx: SNP/3.1 NOTIFY
app-id: test
title: TEST
text: TEST MESSAGE
icon: snarl.png
priority: 1
END

result: [SNP/3.1 SUCCESS
END]
```

or run on terminal/cmd

```bash
> snarl 127.0.0.1 9889 -a test_app -i "snarl.png" -t TEST -v -R
> snarl 127.0.0.1 9889 -a test_app -b "TEST MESSAGE" -i "snarl.png" -p 1 -t TEST -v -N
> pysnarl 127.0.0.1 9889 -a test_app -i "snarl.png" -t TEST -v -R
> pysnarl 127.0.0.1 9889 -a test_app -b "TEST MESSAGE" -i "snarl.png" -p 1 -t TEST -v -N
[SNP/3.1 NOTIFY
app-id: test_app
title: TEST
text: TEST MESSAGE
icon: snarl.png
priority: 1
END]
request xxx: SNP/3.1 NOTIFY
app-id: test_app
title: TEST
text: TEST MESSAGE
icon: snarl.png
priority: 1
END

result: [SNP/3.1 SUCCESS
END]
```

## Tips
`always register (-R) before send message`

## Links

- License: [GPL](https://github.com/cumulus13/snarl/blob/master/LICENSE.md)
- Code: [https://github.com/cumulus13/snarl](https://github.com/cumulus13/snarl)
- Issue tracker: [https://github.com/cumulus13/snarl/issues](https://github.com/cumulus13/snarl/issues)

## Author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)
[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)
 [Support me on Patreon](https://www.patreon.com/cumulus13)
