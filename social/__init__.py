#!/usr/bin/env python
# -*- coding:utf-8 -*-

import oauth2 as oauth


def update(status, config):
    consumer = oauth.Consumer(config['consumer_key'], config['consumer_secret'])
    token = oauth.Token(config['oauth_token'], config['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    data = u'status=%s' % (status)
    resp, content = client.request(config['update_url'], method='POST', body=data)
    if resp['status'] != '200':
        print content
        raise Exception("Invalid response %s." % resp['status'])
