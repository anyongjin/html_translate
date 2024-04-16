# html_translate
将html中的文本翻译为目标语言，保持html结构不变，支持批量翻译。  
支持的云端翻译渠道：百度  

## 如何使用
#### 安装
```shell
pip install -r requirements.txt
python setup.py install
```
#### 开通百度云-文本翻译服务
注册账号实名后赠送100W字符的免费翻译额度。
[文本翻译产品链接](https://cloud.baidu.com/product/mt/text_trans)  
开通后创建应用，得到`api key`和`secret key`。
#### 创建配置文件
如在当前目录下创建`example.yml`
```yaml
by: baidu
from: auto # 这里是源语言，默认auto，自动检测
to: zh # 这里是目标语言，语言代码参考：https://ai.baidu.com/ai-doc/MT/4kqryjku9
baidu:
  apikey: xxx  # 这里填写百度应用的api key
  secretkey: xxx # 这里填写百度应用的secret key
```
#### 执行翻译
```shell
python -m html_translate -c example.yml [html文件路径或文件夹路径]
```
会在输入的文件同级目录下创建一个`trans`文件夹，里面存放翻译后html文件。
## 翻译epub文件
将epub文件后缀改为zip，然后解压缩到文件夹。  
将`text`文件夹的绝对路径进行翻译。  
检查翻译后的html文件，替换原始html文件。  
重新打包为zip文件，重命名为epub。  
