#!/usr/bin/env python3
"""Generates full, unabridged THIRD_PARTY_NOTICES.md with verbatim license texts."""
from pathlib import Path

apache_path = Path("/usr/share/common-licenses/Apache-2.0")
mpl_path = Path("/usr/share/common-licenses/MPL-2.0")
py_lic_path = Path("/usr/lib/python3.12/LICENSE.txt")

apache_txt = apache_path.read_text(encoding="utf-8").strip()
mpl_txt = mpl_path.read_text(encoding="utf-8").strip()

py_raw = py_lic_path.read_text(encoding="utf-8")
sec_b = py_raw[py_raw.find("PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2"):]
sec_b = sec_b[:sec_b.find("BEOPEN.COM LICENSE AGREEMENT")].strip()

mit_text = """Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

bsd3_text = """Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""

header = """# Third-Party Software Notices and Licenses

This repository, distributed binary packages, Python wheels, npm packages, and container images of **InBoost AI Proxy** incorporate, link to, or bundle third-party open-source software components under permissive, developer-friendly licenses.

In compliance with the copyright and licensing obligations of these respective open-source projects (including the MIT License, BSD 3-Clause License, Apache License 2.0, Python Software Foundation License, and Mozilla Public License 2.0), the applicable copyright notices, disclaimers, and full verbatim license texts are reproduced in full below.

---

## 1. Table of Third-Party Components

| Component | License | Copyright Notice / Attribution | Upstream Project |
| :--- | :--- | :--- | :--- |
| **agent-tool-parser** | MIT | Copyright (c) 2026 InBoost Team | [inboost-dev/agent-tool-parser](https://github.com/inboost-dev/agent-tool-parser) |
| **FastAPI** | MIT | Copyright (c) 2018 Sebastián Ramírez | [tiangolo/fastapi](https://github.com/tiangolo/fastapi) |
| **Pydantic** | MIT | Copyright (c) 2017 to present Pydantic Services Inc. and contributors | [pydantic/pydantic](https://github.com/pydantic/pydantic) |
| **Pydantic Core** | MIT | Copyright (c) 2022 Samuel Colvin | [pydantic/pydantic-core](https://github.com/pydantic/pydantic-core) |
| **PyYAML** | MIT | Copyright (c) 2017-2020 Ingy döt Net, (c) 2006-2016 Kirill Simonov | [yaml/pyyaml](https://github.com/yaml/pyyaml) |
| **AnyIO** | MIT | Copyright (c) 2018 Alex Grönholm | [agronholm/anyio](https://github.com/agronholm/anyio) |
| **h11** | MIT | Copyright (c) 2016 Nathaniel J. Smith and other contributors | [python-hyper/h11](https://github.com/python-hyper/h11) |
| **sniffio** | MIT / Apache-2.0 | Copyright (c) 2019 Nathaniel J. Smith | [python-trio/sniffio](https://github.com/python-trio/sniffio) |
| **Uvicorn** | BSD 3-Clause | Copyright (c) 2017-present, Encode OSS Ltd. All rights reserved. | [encode/uvicorn](https://github.com/encode/uvicorn) |
| **Starlette** | BSD 3-Clause | Copyright (c) 2018-present, Encode OSS Ltd. All rights reserved. | [encode/starlette](https://github.com/encode/starlette) |
| **HTTPX** | BSD 3-Clause | Copyright (c) 2019-present, Encode OSS Ltd. All rights reserved. | [encode/httpx](https://github.com/encode/httpx) |
| **HTTPCore** | BSD 3-Clause | Copyright (c) 2020-present, Encode OSS Ltd. All rights reserved. | [encode/httpcore](https://github.com/encode/httpcore) |
| **idna** | BSD 3-Clause | Copyright (c) 2013-2026, Kim Davies and contributors. All rights reserved. | [kjd/idna](https://github.com/kjd/idna) |
| **click** | BSD 3-Clause | Copyright (c) 2014 Pallets. All rights reserved. | [pallets/click](https://github.com/pallets/click) |
| **Cryptography** | Apache-2.0 / BSD-3 | Copyright (c) Individual contributors, The Cryptography Developers. All rights reserved. | [pyca/cryptography](https://github.com/pyca/cryptography) |
| **CPython (Embedded Runtime)** | PSFL | Copyright (c) 2001-2026 Python Software Foundation. All Rights Reserved. | [python/cpython](https://github.com/python/cpython) |
| **certifi** | MPL-2.0 | Copyright (c) Kenneth Reitz and contributors | [certifi/python-certifi](https://github.com/certifi/python-certifi) |

---

## 2. Full Verbatim License Texts

### A. MIT License

**Applicable to:** `agent-tool-parser`, `FastAPI`, `Pydantic`, `Pydantic Core`, `PyYAML`, `AnyIO`, `h11`, `sniffio`

#### Component Copyright Attributions:
- **agent-tool-parser**: Copyright (c) 2026 InBoost Team
- **FastAPI**: Copyright (c) 2018 Sebastián Ramírez
- **Pydantic**: Copyright (c) 2017 to present Pydantic Services Inc. and individual contributors
- **Pydantic Core**: Copyright (c) 2022 Samuel Colvin
- **PyYAML**: Copyright (c) 2017-2020 Ingy döt Net, Copyright (c) 2006-2016 Kirill Simonov
- **AnyIO**: Copyright (c) 2018 Alex Grönholm
- **h11**: Copyright (c) 2016 Nathaniel J. Smith <njs@pobox.com> and other contributors
- **sniffio**: Copyright (c) 2019 Nathaniel J. Smith

```text
""" + mit_text + """
```

---

### B. BSD 3-Clause License

**Applicable to:** `Uvicorn`, `Starlette`, `HTTPX`, `HTTPCore`, `idna`, `click`, `Cryptography` (BSD option)

#### Component Copyright Attributions:
- **Uvicorn**: Copyright (c) 2017-present, Encode OSS Ltd. All rights reserved.
- **Starlette**: Copyright (c) 2018-present, Encode OSS Ltd. All rights reserved.
- **HTTPX**: Copyright (c) 2019-present, Encode OSS Ltd. All rights reserved.
- **HTTPCore**: Copyright (c) 2020-present, Encode OSS Ltd. All rights reserved.
- **idna**: Copyright (c) 2013-2026, Kim Davies and contributors. All rights reserved.
- **click**: Copyright 2014 Pallets. All rights reserved.
- **Cryptography**: Copyright (c) Individual contributors, The Cryptography Developers. All rights reserved.

```text
""" + bsd3_text + """
```

---

### C. Apache License, Version 2.0

**Applicable to:** `Cryptography` (Dual-licensed with BSD 3-Clause), `sniffio` (Dual-licensed with MIT)

```text
""" + apache_txt + """
```

---

### D. Python Software Foundation License (PSF License Version 2)

**Applicable to:** Embedded CPython runtime components packaged in standalone binaries, and `typing-extensions`.

```text
""" + sec_b + """
```

---

### E. Mozilla Public License Version 2.0 (MPL-2.0)

**Applicable to:** `certifi` (CA certificate bundle utilized by HTTPX / HTTPCore for secure TLS communication).  
*Source code for `certifi` is available at:* [https://github.com/certifi/python-certifi](https://github.com/certifi/python-certifi)

```text
""" + mpl_txt + """
```
"""

output_path = Path("/home/antigravity/.gemini/antigravity-cli/scratch/inboost-ai-proxy-runtime/THIRD_PARTY_NOTICES.md")
output_path.write_text(header.strip() + "\n", encoding="utf-8")
print(f"Generated {output_path}: {len(output_path.read_text().splitlines())} lines, {output_path.stat().st_size} bytes")
