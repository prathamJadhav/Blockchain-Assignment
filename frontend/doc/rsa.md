# Verification of Payload data and signature using RSA keys

## Generating the keys
The following shell script is used to generate the keys in the format required. 
```sh
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in private.pem -out private2.pem
rm private.pem
mv private2.pem private.pem
```

The steps taken in this process are:
- Generate a 2048-bit private key using ```openssl```
- Create a corresponding public key for the generated private key
- Convert the private key generated from PKCS#1 to PKCS#8.

The final result contains two files: `private.pem` and `public.pem`. These are our two keys.

## Verification
The payload data is signed using the private key and the `RSASSA-PKCS1-v1_5` algorithm.
It must be verified using the `public.pem` file that needs to be stored on the backend server.

Let us assume a sample message has been signed using `private.pem`.

The following is the Python code used to verify the signature:
```python
from Crypto import Signature
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base64

message = b"This is a test"
signature_b64 = "OhUKfdVY03lMUgJU46YA4g7F+2Ln4a155fAygH3lr8uxLa4cbhn3emAbRU3UZBqh3TMNSTSl4f1H4QtxDs8sWUTLg+nMmj66b2XzDljscqNQupcYkykzeFIcf3xeaRPxVGk9F8Kc8LOG/wJiCD3P3rbjMZh7Pow3h151i6Ylogkjz4H9NuSgvRRvzqb3kz/u8mVPMq8YvP86xc4qttfJfKqZDPQbijDP/Alo1akarlJR6rG3J35hxCNsuuiWSeLbr1tkMHBij+rP5z1rifKn0d57dx1DIxHL0eRh0w5ODle6Qhjdj57CxQWtvNlx+GJd9EgIYPjLQ0yLGKHGOWFigQ==" # this will be sent from the frontend

# import the key
key = RSA.import_key(open('public.pem').read())

h = SHA256.new(message)


try:
    pkcs1_15.new(key).verify(h, bytearray(base64.b64decode(signature_b64)))
    print("The signature is valid.")
except (ValueError, TypeError):
    print("The signature is not valid.")
```