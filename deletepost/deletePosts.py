import logging

import azure.functions as func
import logging
import requests
import jwt
import json
from datetime import datetime as date


def getAllPosts(ghosturl, token):
    url = str(ghosturl) + '/ghost/api/admin/posts/'
    params = {'formats': 'html,mobiledoc', 'limit': 'all', 'fields': 'id,title,url'}
    headers = {'Authorization': 'Ghost {}'.format(token)}
    result = requests.get(url, params=params, headers=headers)
    data = result.json()
    ids = []
    for each in data['posts']:
        ids.append(each['id'])
    return ids


def deletePostById(id, ghosturl, token):
    url = str(ghosturl) + '/ghost/api/admin/posts/' + id + '/'
    headers = {'Authorization': 'Ghost {}'.format(token)}
    result = requests.delete(url, headers=headers)
    if result.ok:
        result = 'success: post deleted (status_code:' + str(result.status_code) + ')'
    else:
        result = 'error: post NOT deleted (status_code:' + str(result.status_code) + ')'

    print(result)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ghosturl = req.params.get('ghosturl')
    key = req.params.get('key')


    if not key:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            key = req_body.get('key')
            ghosturl = req_body.get('ghosturl')

    if key:
        id, secret = key.split(':')
        iat = int(date.now().timestamp())
        header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
        payload = {
            'iat': iat,
            'exp': iat + 5 * 60,
            'aud': '/admin/'
        }
        token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)
        posts = getAllPosts(ghosturl, token)
        for postID in posts:
            deletePostById(postID, ghosturl, token)
        return func.HttpResponse(
            "All posts are deleted.",
            status_code=200
        )
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Please provide key: Ghost API Key and ghosturl: Ghost URL",
            status_code=200
        )
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
AP
