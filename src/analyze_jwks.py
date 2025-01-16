import sys
import jwt
import argparse
import json
import collections
import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import base64
import re

def analyze_jwks(jwks: str):
    jwks_json = json.loads(jwks)
    #alg = jwt.get_unverified_header(jwks)['alg']
    #decoded = jwt.decode(jwks, algorithms=[alg], options={"verify_signature": False})
    jwks_keys = jwks_json.get('keys', [])
    public_keys = collections.OrderedDict()
    for jwks_key in jwks_keys:
        kid = jwks_key.get('kid')
        public_keys[kid] = {'orig': jwks_key, 'key': jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwks_key))}
    print ('The following keys are present')
    for (kid, jwks_key) in public_keys.items():
        print ('Key ID "{}":'.format(kid))
        # Decode the first certificate found in list of certificates in field x5c
        cert_encoded = jwks_key['orig']['x5c'][0]
        print (cert_encoded)
        print ('')

def analyze_jwks_from_url(url: str):
    r = requests.get(url)
    if r.status_code == 200:
        cache_control = r.headers.get('Cache-Control', None)
        if cache_control is not None:
            max_age_str = name = re.search('.*=([0-9]*)[^0-9]*', cache_control).group(1)
            max_age = int(max_age_str)
            print(f'Identity Provider is sending the "Cache-Control" header with a value for max age of {max_age} seconds (={max_age/(60*60)} hours)')
            print ('')
        analyze_jwks(r.text)
    else:
        print ('Unable to fetch data from provided URL')



if __name__=='__main__':
    if sys.version_info >= (3, 9):
        parser = argparse.ArgumentParser(prog='decode_jwt',
            exit_on_error=False) # type: ignore  # pragma: no cover
    else:
        parser = argparse.ArgumentParser(prog='ccloud_list_environments') # type: ignore  # pragma: no cover
    parser.add_argument('--jwks', '-j')
    parser.add_argument('--url', '-u')
    #parsed_args = parser.parse_args(args=sys.argv)
    parsed_args = parser.parse_args()
    jwks = parsed_args.jwks
    url = parsed_args.url
    if jwks is None and url is None:
        print('Please provide either a JWKS with "--jwks" or "-j" or a URL for downloading a JWKS with "--url" or "-u"')
        sys.exit(1)
    if jwks is not None:
        analyze_jwks(jwks)
    elif url is not None:
        analyze_jwks_from_url(url)
