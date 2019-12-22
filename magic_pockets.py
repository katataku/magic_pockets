#! /usr/local/bin/python3

import sys,shelve,pyperclip
import re,os,shutil,requests,json,pprint
import random
import logging
import datetime
import time

path_consumer_key = "./POCKET_CONSUMER_KEY"
with open(path_consumer_key) as f:
    POCKET_consumer_key = f.read()

path_access_token = "./POCKET_ACCESS_TOKEN"
with open(path_access_token) as f:
    POCKET_access_token = f.read()


def del_item(item_id):


    payload_tag = {
            'consumer_key': POCKET_consumer_key,
            'access_token': POCKET_access_token, 
            'actions': json.dumps([
                {
                    "action" :"delete",
                    "item_id":int(item_id) ,
                }
            ],)
        }
    req = requests.get('https://getpocket.com/v3/send',params=payload_tag)
    print('  item_del : {}'.format(req.text))
    

def main():

    payload = {
        'consumer_key':POCKET_consumer_key,
        'access_token': POCKET_access_token, 
        'state':'unread',
        'sort':'oldest',
        'since' : 1487010000,
        'count':300
        }
    r=requests.post('https://getpocket.com/v3/get',data=payload)

    ret_list = json.loads(r.text)
    OK_sum = 0
    NG_sum = 0 

    for item in ret_list['list'].values():
        if 'resolved_url' not in item :
            continue
        resolved_url = item['resolved_url']
        resolved_title = item['resolved_title']
        item_id = item['item_id']
        try:
            r = requests.get(resolved_url,timeout=60)
            print(' STS : {},title : {}'.format(r.status_code,resolved_title)) 
            if r.status_code == 200 :
                OK_sum += 1
            else:
                NG_sum += 1
                del_item(item_id)     
        except requests.exceptions.ConnectionError as identifier:
            print(' STS : Err,title : {} '.format(resolved_title))
            NG_sum += 1
            del_item(item_id)     
        except requests.exceptions.ReadTimeout :
            continue


    print('Samarry ')
    print('OK : {}, NG:{}'.format(OK_sum,NG_sum))

if __name__ == '__main__':
    main()