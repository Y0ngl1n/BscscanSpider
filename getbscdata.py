from bs4 import BeautifulSoup
import urllib.request
import time
import ssl
import re

clu = "0x1162E2EfCE13f99Ed259fFc24d99108aAA0ce935" #测试用clucoin的地址
myApiToken = "9WB12KSWQQ5FPIFXDPC7PP8BNDBUCI3BWW"
MyWalletAddress = "0x9dFE30b57E7B189F5ac5b3B9ab7180bB3a9991CD"


# TokenInfor
def getSupplybycondress():  #通过合约地址得到总发行量
    try:
        tokenAddress = input("Please enter the address of the token:")
        response = urllib.request.urlopen("http://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress="+tokenAddress+"&apikey="+myApiToken,timeout=2)
        responselist = eval(response.read().decode('utf-8'))
        for key,value in responselist.items():
            if key == "result":
                val = str(value)
                print("The total supply of this token：%s" %val)
    except urllib.error.URLError as e:
        print("Time Out")
    time.sleep(3)


def getMyBalancebycondress():  # 根据合约地址与钱包地址获取持仓量
    try:
        myaddress = input("Please enter the address of your wallet:")
        tokenAddress = input("Please enter the address of the token:")
        response1 = urllib.request.urlopen("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress="+tokenAddress+"&address="+myaddress+"&tag=latest&apikey="+myApiToken)
        responselist1 = eval(response1.read().decode('utf-8'))
        for key, value in responselist1.items():
            if key == "result":
                val = str(value)
                print("The token banlance of this wallet address：%s" % val)
    except Exception as e2:
        print("Error catched and ignored")
    time.sleep(3)

def getHolderlistbycondress():

    tokenAddress = input("Please enter the address of the token:")
    requestbscurl = "https://bscscan.com/token/"+tokenAddress
    head = {
        "authority": "bscscan.com", "method": "GET",
        "accept": "text / html, application / xhtml + xml, application / xml", "accept - language": "zh - CN, zh",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    try:
        request = urllib.request.Request(requestbscurl,headers=head)
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        soupparser = BeautifulSoup(html,"html.parser")
    # 解析后用正则表达式匹配
        holderlist = soupparser.find_all('div',class_="mr-3")
        holdernum = str(holderlist[0])
        pattern = re.compile(r'<div class="mr-3">(.*)</div>',re.S)
        result = re.sub(r'\n','',re.findall(pattern,holdernum)[0])
        print(result)
    except Exception as e:
        print("ERROR:%s"%e)
    time.sleep(3)


def getNameInfobycondress():
    tokenAddress = input("Please enter the address of the token:")
    requestbscurl = "https://bscscan.com/address/"+tokenAddress
    head ={
    "authority": "bscscan.com", "method": "GET", "accept": "text / html, application / xhtml + xml, application / xml", "accept - language": "zh - CN, zh", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    try:
        request = urllib.request.Request(requestbscurl, headers=head)
        response = urllib.request.urlopen(request)
        html = str(response.read().decode("utf-8"))
        soup = BeautifulSoup(html,"html.parser")
        tokeninfotag = str(soup.find_all('a',href="/token/"+tokenAddress)[0])
        pattern = re.compile(r'<a data-toggle="tooltip" href=".*">(.*)</a>',re.S)
        result = re.findall(pattern,tokeninfotag)[0]
        print(result)
    except Exception as e:
        print("ERROR:%s"%e)
    time.sleep(3)
#
# #AccountInfo
#     def getBNBBalance():
#     def getTransactions():

# #ContractInfo
def getCode():   # 根据合约地址获取源码
    try:
        tokenAddress = input("Please enter the address of the token:")
        response3 = urllib.request.urlopen("https://api.bscscan.com/api?module=contract&action=getsourcecode&address="+tokenAddress+"&apikey="+myApiToken)
        responselist = eval(response3.read().decode('utf-8'))
        for key, value in responselist.items():
            if key == "result":
                val = str(value)
                codefile = open(tokenAddress+"Code.txt", "a")  # 创建文件
                codefile.write("%s"%val)  # 写入合约代码
                codefile.close()
                print("The code have saved.")  # 显示源码已保存
    except Exception as e3:
        print("ERROR OCCURED WITH SOMEREASON")
    time.sleep(3)


def main():
    while True:
        print("=====================================")          # 命令行功能选择界面
        print("1.The Supply By Contract Address")
        print("2.The Name By Contract Address")
        print("3.Your Balance By Contract Address")
        print("4.The Holder List By Contract Address")
        print("5.Get Codes By Contract Address")
        print("---－---PRESS Q BUTTON TO EXIT---－---")
        print("=====================================")
        number = input("Enter the function number:")

        if number == "1":
            getSupplybycondress()
        elif number == "2":
            getNameInfobycondress()
        elif number == "3":
            getMyBalancebycondress()
        elif number == "4":
            getHolderlistbycondress()
        elif number == "5":
            getCode()

        elif number =="q"or"Q":
            break
        else:
            continue

if __name__ == "__main__": #这句程序入口在被其他文件调用时不执行
    main()



