# Notes

## JWT

    The same applies to bearer Access Tokens. If that could pose problems to your application, you can change the Bearer token into a Proof of Possession token (a PoP token) by adding a cnf claim - a confirmation claim. The claim can e.g. contain a fingerprint of the clients certificate, which can then be validated by the resource server.

    Whether the token is signed (a JWS), or encrypted (a JWE) it will contain an alg claim in the header, that indicates which algorithm has been used for signing or encryption.When verifying / decrypting the token you should always check the value of this claim with a whitelist of algorithms that your system accepts. This mitigates an attack vector where someone would tamper with the token and make you use a different, probably less secure algorithm to verify the signature or decrypt the token.

## Tortoise

> Init the DB models before this import

    Tortoise.init_models(['database.models'], 'models')
    from routers import parents, children, users, perms

## MySQL

    db_url="mysql://root:root@127.0.0.1:3306/tortoise"


## Imports - root parent

    import sys
    sys.path.append("..\<parent_folder>")

## password policy

    ^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$

    This regex will enforce these rules:

    At least one upper case English letter, (?=.*?[A-Z])
    At least one lower case English letter, (?=.*?[a-z])
    At least one digit, (?=.*?[0-9])
    At least one special character, (?=.*?[#?!@$%^&*-])
    Minimum eight in length .{8,} (with the anchors)