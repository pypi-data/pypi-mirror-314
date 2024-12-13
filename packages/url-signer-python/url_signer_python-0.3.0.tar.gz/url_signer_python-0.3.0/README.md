# url-signer-python

[![PyPI version](https://badge.fury.io/py/url-signer-python.svg)](https://pypi.org/project/url-signer-python/)
[![Python version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![Build Status](https://github.com/ioriver/url-signer-python/actions/workflows/master.yml/badge.svg)](https://github.com/ioriver/url-signer-python/actions)

## Overview

**url-signer-python** is a Python library designed to generate signatures for URLs. These signatures can be used by the IO River service with Signed-URLs enabled to secure access to content. The library generates signatures for all CDN providers associated with the service.

---

## Installation

To install **url-signer-python**, you can use pip:

```bash
pip install url-signer-python
```

Alternatively, you can clone the repository and install it manually:

```bash
git clone https://github.com/ioriver/url-signer-python.git
cd url-signer-python
pip install .
```

## Usage

Below is some example to help you get started:

### Step 1: Create URL Signer

```python
from url-signer-python import feature

private_key = "YourPrivateKey"
encryption_key = "YourEncryptionKey"

# use the provider key information from your service
providers_key_info = {
    "cloudfront_key_id": "1234",
    "fastly_key_id": "5678"
}

singer = UrlSigner(private_key, encryption_key, providers_key_info)
```

### Step 2: Generate Signature

```python
# the policy to be signed
policy = {
    "resources": "https://test.example.com/streams/*",
    "condition": {
        "end_time": 1733356800
    }
}

# generate signature for all CDNs
signature = singer.generate_url_signature(policy)
```

## API Reference

### UrlSigner Constructor

#### Parameters

- **`private_key`** (string): The private key for signing the URL.
- **`encryption_key`** (string): The encryption key for signing the URL.
- **`providers_key_info`** (object): Information about the keys deployed within the CDN providers (copied from your service).

### generate_url_signature(policy)

#### Attributes for policy

- **`resources`** (required):
  A string specifying the URL or URL pattern the policy applies to.

- **`condition`** (required):  
  A dictionary containing conditions for the policy.

  - **`end_time`** (required):  
    An integer specifying the UNIX timestamp when the signature will expire.

  Additional optional attributes in the `condition` dictionary include:

  - **`start_time`**:  
    An integer specifying the UNIX timestamp when the signature becomes valid. Default: None.

## Requirements

This library requires:

- Python 3.7+
- Dependencies listed in requirements.txt.

To install dependencies manually:

```bash
pip install -r requirements.txt
```

## Testing

```bash
pytest
```

## Support

If you encounter any issues, please [open an issue](https://github.com/ioriver/url-signer-python/issues) on GitHub or contact us at support@ioriver.io.
