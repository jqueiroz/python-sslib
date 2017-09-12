Secret sharing library
======

A Python3 library for sharing secrets. Currently, only [Shamir's secret sharing scheme](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing) is available, but other algorithms should be implemented in the future.

## Installation
```bash
pip install sslib
```

## Shamir's secret sharing
### Overview
[Shamir's algorithm](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing) allows one to to split an integer _S_ into _n_ shares in such a way that at least _k_ of these shares are required to recover the original secret.

The key ideia is to build a polynomial _Q_ of degree _k-1_ over a finite field _GF(P)_, where _P_ is a prime number greater than max(_S_, _n_), such that _Q(0) = S_.
Then, _n_ points are distributed to participants—for example, _(1, Q(1))_, _(2, Q(2))_, ..., _(n, Q(n))_.

Given the prime _P_ and any _k_ points, it is possible to recover the secret by reconstructing _Q_ and evaluating _Q(0_).
However, knowledge of fewer than _k_ points leaves the secret _S_ completely undetermined: for any _0 ≤ S' < P_, there exists a polynomial _Q'_ over _GF(P)_ passing through all given points such that _Q'(0) = S'_.

### Usage
Splitting a sequence of bytes _B_ into _n_ shares, at least _k_ of which are required to rebuild the original sequence, can be done by calling ````shamir.split_secret(B, k, n)````. This function outputs a _dict_ containing:

  * _required\_shares_: the number of shares required for recovery;
  * _prime\_mod_: the prime number _P_;
  * _shares_: a list containing _n_ points of the polynomial _Q_.

Subsequent recovery is possible by calling ````shamir.recover_secret(dict)````. Beware that _dict_ should include not only the list of shares (````shares````), but also the prime modulus used (````prime_mod````). The number of required shares (````required_shares````) is optional, but recommended. If fewer than necessary shares are provided, but ````required_shares```` is specified, an error will be reported; otherwise, an incorrect secret will be silently produced.

In the output of ````shamir.split_secret````, the prime modulus is represented as a sequence of bytes, and points of _Q_ are represented as ordered pairs _(x, y)_, where _x_ is an _int_ and _y_ is a sequence of bytes. In order to facilitate secret distribution, the functions ````shamir.to_base64````, ````shamir.from_base64````, ````shamir.to_hex```` and ````shamir.from_hex```` are provided (see examples below).

#### Splitting secret into shares (base64)
```python
>>> from sslib import shamir
>>> required_shares = 2
>>> distributed_shares = 5
>>> shamir.to_base64(shamir.split_secret("this is my secret".encode('ascii'), required_shares, distributed_shares))
{'required_shares': 2, 'prime_mod': 'AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhQ==', 'shares': ['1-Swwdr0O19NSMsoG4DXxvTeB9WTykw9+a', '2-lhg7XodrvzSw+5BPsYW+LkfaPxPmFVnA', '3-4SRZDcshiZTVRJ7nVY8NDq83JOsnZtPm', '4-LDB2vQ7XU/T5ja1++Zhb7xaUCsJouE2H', '5-dzyUbFKNHlUd1rwWnaGqz33w8JmqCcet']}
```

#### Recovering secret from shares (base64)
```python
>>> from sslib import shamir
>>> data = {'required_shares': 2, 'prime_mod': 'AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhQ==', 'shares': ['1-Swwdr0O19NSMsoG4DXxvTeB9WTykw9+a', '3-4SRZDcshiZTVRJ7nVY8NDq83JOsnZtPm']}
>>> shamir.recover_secret(shamir.from_base64(data)).decode('ascii')
'this is my secret'
```

#### Splitting secret into shares (hex)
```python
>>> from sslib import shamir
>>> required_shares = 2
>>> distributed_shares = 5
>>> shamir.to_hex(shamir.split_secret("this is my secret".encode('ascii'), required_shares, distributed_shares))
{'required_shares': 2, 'prime_mod': '01000000000000000000000000000000000000000000000085', 'shares': ['1-19bbe18e17f1d9af8144b09ceae46a13070d36ac81fcf606', '2-3377c31c2fe388ea9a1fee196c55b3b894f9f9f3a0878698', '3-4d33a4aa47d53825b2fb2b95edc6fd5e22e6bd3abf12172a', '4-66ef86385fc6e760cbd669126f384703b0d38081dd9ca7bc', '5-80ab67c677b8969be4b1a68ef0a990a93ec043c8fc27384e']}
```

#### Recovering secret from shares (hex)
```python
>>> from sslib import shamir
>>> data = {'required_shares': 2, 'prime_mod': '01000000000000000000000000000000000000000000000085', 'shares': ['1-19bbe18e17f1d9af8144b09ceae46a13070d36ac81fcf606', '3-4d33a4aa47d53825b2fb2b95edc6fd5e22e6bd3abf12172a']}
>>> shamir.recover_secret(shamir.from_hex(data)).decode('ascii')
'this is my secret'
```

#### Splitting secret into shares (raw)
```python
>>> from sslib import shamir
>>> required_shares = 2
>>> distributed_shares = 5
>>> shamir.split_secret("this is my secret".encode('ascii'), required_shares, distributed_shares)
{'required_shares': 2, 'prime_mod': b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x85', 'shares': [(1, b'OL\xc1\xfc\xc7\x18\xf2D\xd1\xcd\x087|N\xda\x9b\xfd\x19\x18\xddc!w\xcc'), (2, b'\x9e\x99\x83\xf9\x8e1\xba\x15;0\x9dN\x8f*\x94\xca\x81\x11\xbeUb\xd0\x8a$'), (3, b'\xed\xe6E\xf6UJ\x81\xe5\xa4\x942e\xa2\x06N\xf9\x05\nc\xcdb\x7f\x9c|'), (4, b"=3\x07\xf3\x1ccI\xb6\r\xf7\xc7|\xb4\xe2\t'\x89\x03\tEb.\xaeO"), (5, b'\x8c\x7f\xc9\xef\xe3|\x11\x86w[\\\x93\xc7\xbd\xc3V\x0c\xfb\xae\xbda\xdd\xc0\xa7')]}
```

#### Recovering secret from shares (raw)
```python
>>> from sslib import shamir
>>> data = {'required_shares': 2, 'prime_mod': b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x85', 'shares': [(1, b'OL\xc1\xfc\xc7\x18\xf2D\xd1\xcd\x087|N\xda\x9b\xfd\x19\x18\xddc!w\xcc'), (3, b'\xed\xe6E\xf6UJ\x81\xe5\xa4\x942e\xa2\x06N\xf9\x05\nc\xcdb\x7f\x9c|')]}
>>> shamir.recover_secret(data).decode('ascii')
'this is my secret'
```

### Optional parameters
#### Randomness source
By default, the function ````shamir.split_secret```` uses either ````randomness.RandomReader```` or ````randomness.UrandomReader```` as the source of randomness, depending on the size of the secret. Under Unix, the former reads random bytes from _/dev/random_, while the latter reads from _/dev/urandom_. Under Windows, both classes take bytes from _CryptGenRandom_.

It is possible to explicitly choose the source of randomness, as the following code illustrates.

```python
>>> from sslib import shamir, randomness
>>> required_shares = 2
>>> distributed_shares = 5
>>> shamir.to_base64(shamir.split_secret("this is my secret".encode('ascii'), required_shares, distributed_shares, randomness_source=randomness.UrandomReader()))
{'required_shares': 2, 'prime_mod': 'AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhQ==', 'shares': ['1-f9lIXSnvvJDKcg00a70hvT+a8mxFk1PG', '2-/7KQulPfTq0seqdIbgcjDQYVcXMntEIY', '3-f4vZF33O4MmOg0FccFEkXMyP8HoJ1S/l', '4-/2UhdKe+cuXwi9twcpslrJMKb4Dr9h43', '5-fz5p0dGuBQJSlHWEdOUm/FmE7ofOFwwE']}
```

#### Prime modulus
By default, the function ````shamir.split_secret```` chooses the modulus from a list of known primes based on the length of the secret. It is also possible to specify the prime modulus to be used, as the following code illustrates. In order to split an _n_-byte secret, a prime greater than 2<sup>8n+8</sup> must be provided (see implementation details).

_Warning_: if you follow this approach, please make sure that the provided modulus is indeed a prime number.

```python
>>> from sslib import shamir
>>> required_shares = 2
>>> distributed_shares = 5
>>> shamir.to_base64(shamir.split_secret("this is my secret".encode('ascii'), required_shares, distributed_shares, prime_mod=2**607-1))
{'required_shares': 2, 'prime_mod': 'f////////////////////////////////////////////////////////////////////////////////////////////////////w==', 'shares': ['1-cHBzILxFiPMcv3pmK1SHQoxRIn47n+JsrK1xv+1h86iTmEOK2IXUk/RGkskGnEDbWYx7gI3bADZD9K1GHMqTEnYVwtFGdcHSzLdMXA==', '2-YODmQXiLEeY5fvTMVqkOhRiiRPx3P8TZWVrjf9rD51EnMIcVsQupJ+iNJZINOIG2sxj3ARu2AGyH6TAX0SuzBIK4ZTUTyxBANfwzRQ==', '3-UVFZYjTQmtlWPm8ygf2Vx6TzZ3qy36dGBghVP8gl2vm6yMqgiZF9u9zTuFsT1MKSDKVygamRAKLL3bLphYzS9o9bB5jhIF6tn0EaLg==', '4-QcHMgvEWI8xy/emYrVIdCjFEifjuf4mysrXG/7WHzqJOYQ4rYhdST9EaSyQacQNtZjHuAjdsANkP0jW7Oe3y6Jv9qfyuda0bCIYBFw==', '5-MjI/o61brL+PvWP+2KakTL2VrHcqH2wfX2M4v6Lpwkrh+VG2Op0m48Vg3e0hDURIv75pgsVHAQ9TxriM7k8S2qigTGB7yvuIccroAA==']}
```

### Limitations
The current implementation of Shamir's algorithm only supports splitting secrets of up to ~26.3 KiB. While splitting larger secrets is theoretically possible, recovery from shares becomes increasingly slower. On my computer, recovering a 26 KiB secret from three shares takes around 0.9s.

The recommended approach for larger secrets is to perform encryption using a symmetric-key algorithm (such as AES) and then split the encryption key.

### Implementation details
Internally, the secret is converted to an integer by interpreting its bytes in Big-Endian. Since the first bytes of the secret could be zero, the magic byte ````b'*'```` is always prepended before conversion. Upon recovery, the first byte of the secret is subsequently discarded.
