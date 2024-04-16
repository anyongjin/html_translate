#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
import requests
from pathlib import Path
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from typing import *
from io import StringIO

cvt_name = 'baidu'
cvtr = None
code_src = 'auto'
code_tgt = 'zh'
chl_config: Optional[dict] = None


def translate_inputs(items: List[str]):
    paths: List[Path] = []
    out_dir: Path = None
    for item in items:
        p = Path(item)
        if p.is_dir():
            if not out_dir:
                out_dir = p / 'trans'
            for path in p.iterdir():
                if path.suffix in {'.html', '.htm'}:
                    paths.append(path)
        elif p.is_file():
            if not out_dir:
                out_dir = p.parent / 'trans'
            paths.append(p)
        else:
            text = translate_html(item)
            print(text)
    if paths:
      out_dir.mkdir(parents=True, exist_ok=True)
      for path in paths:
          name = os.path.basename(path.name)
          outfile = out_dir / name
          if outfile.exists():
              continue
          print(f'trans: {path}')
          in_text = path.read_text('utf-8')
          out_text = translate_html(in_text)
          with open(outfile.name, 'w', encoding='utf-8') as f:
              f.write(out_text)
      print(f'process {len(paths)} files complete')


def translate_html(input_html):
    soup = BeautifulSoup(input_html, 'html.parser')

    for element in soup.find_all(string=True):
        modified_text = trans_text(element)
        if element.parent.name not in ['script', 'style']:
            element.replace_with(modified_text)

    return str(soup)

def trans_text(text: str):
    if not text or not text.strip():
        return ''
    if cvt_name == 'baidu':
        return trans_by_baidu(text)
    else:
        raise ValueError('unsupport translate channel:' + cvt_name)

def trans_by_baidu(text):
    global cvtr
    if not cvtr:
        client_id = chl_config['apikey']
        api_secret = chl_config['secretkey']
        if not client_id or not api_secret:
            raise ValueError('baidu.apikey or baidu.secretkey is required')
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={api_secret}"
        rsp = http_json('POST', url)
        cvtr = rsp.get('access_token')
        if not cvtr:
            raise ValueError(f'get baidu access_token err: {rsp}')
    url = 'https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=' + cvtr
    payload = {'q': text, 'from': code_src, 'to': code_tgt}
    rsp = http_json('POST', url, payload)
    b = StringIO()
    res = rsp.get('result')
    if res:
        items = res.get('trans_result')
        if items:
            for it in items:
                b.write(it.get('dst'))
                b.write('\n')
    else:
        code = rsp.get('error_code')
        if code:
            raise ValueError(f'baidu translate error: {rsp}')
    return b.getvalue()


def http_json(method: str, url: str, data: Optional[dict] = None) -> dict:
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json'
    }
    if data:
        data = json.dumps(data)
    rsp = requests.request(method, url, headers=headers, data=data)
    rsp_text = rsp.content.decode('utf-8')
    if rsp.status_code != 200:
        raise ValueError(f'get baidu access_token fail: {rsp_text}')
    return json.loads(rsp_text)


def main():
    global chl_config, cvt_name, code_src, code_tgt
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", default="", help="yaml config")
    parser.add_argument("src", nargs="+", help="The html you want to translate. ")
    data = parser.parse_args()
    import yaml
    with open(data.config, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f.read())
    cvt_name = config['by']
    code_src = config['from']
    code_tgt = config['to']
    chl_config = config[cvt_name]
    translate_inputs(data.src)
