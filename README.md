# masnmap
masscan + nmap 快速端口存活检测和服务识别。

思路很简单，将masscan在端口探测的高速和nmap服务探测的准确性结合起来，达到一种相对比较理想的效果。
先使用masscan以较高速率对ip存活端口进行探测，再以多进程的方式，使用nmap对开放的端口进行服务探测。

## 安装依赖
需先安装`masscan `、`nmap`和`python-nmap`库。 masscan和nmap请自行安装，python-nmap库可通过如下命令安装。

* pip3 install python-nmap -i https://pypi.douban.com/simple/

目前其版本为：python-nmap==0.6.1

## 文件说明
简要文件说明如下：

* masnmap.py： masscan + nmap结合快速端口存活和服务探测脚本；
* ips.txt: 需探测的ip地址列表，每行一个ip地址；

## 参数配置说明
简要参数说明如下：

* ip_file = 'ips.txt'   					 # ip地址文件
* masscan_exe = '/usr/bin/masscan'   # masscan可执行文件路径
* masscan_rate = 1000000                 # masscan扫描速率
* masscan_file = 'masscan.json'          # masscan扫描结果文件
* process_num = 800				# 执行nmap扫描的进程数量

具体参数值可以自行调优。

## 检测说明
主要执行步骤调用在main函数中，如下：

	def main():
	    # Step 1, run masscan to detect all the open port on all ips
	    run_masscan()

	    # Step 2, extract masscan result file:masscan.json to ip:port format
	    extract_masscan()
	
	    # Step 3, using nmap to scan ip:port
	    run_nmap()
	
	    # Step 4, save results
	    save_results()

## 使用说明
直接使用如下命令执行即可。

```
# python3 masnmap.py
```

## 扫描测试说明
对8930个ip地址进行探测，共探测出231687个开放端口及进行服务探测。

```
# wc -l ips.txt 
8930 ips.txt
# wc -l services.txt 
231687 services.txt
```
masscan rate 100 0000，并发nmap进程数800，共耗时：
`It takes 800 process 4761 seconds to run ... 231687 tasks`

具体参数值配置需要根据扫描机器的性能和带宽进行调整。