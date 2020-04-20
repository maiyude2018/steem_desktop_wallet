from PyQt5 import QtWidgets, QtCore
import sys
from PyQt5.QtCore import *
import random
import time
from SUI import cure
from steemwaller import Ui_steem
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
from PyQt5 import QtWidgets
from beem.steem import Steem
from steemengine.wallet import Wallet
import json
import requests
import sqlite3
from beem.account import Account
from beembase.transactions import Signed_Transaction
import hashlib
from binascii import hexlify
from beem.market import Market
from steemengine.api import Api as SApi
from beemgraphenebase.account import PasswordKey



sapi = SApi()


node2 = "https://api.hive.blog"


# 继承QThread
class Runthread(QtCore.QThread):
    #通过类成员对象定义信号对象
    _signal = pyqtSignal(str)
    def __init__(self):
        super(Runthread, self).__init__()
    def __del__(self):
        self.wait()
    def run(self):
        for i in range(100):
            time.sleep(0.02)
            self._signal.emit(str(i))  # 注意这里与_signal = pyqtSignal(str)中的类型相同



class CamShow(QMainWindow, Ui_steem):
    def __init__(self, parent=None):
        super(CamShow, self).__init__(parent)
        self.setupUi(self)
        self.pbar.hide()
        self.par_text.hide()
        # 读取用户列表
        self.additem()
        self.Button_load_acc.clicked.connect(self.funs)
        # self.Button_load_acc.setHidden(True)
        # 读取节点
        self.nodes = "https://api.justyy.com"
        print("当前节点", self.nodes)

        # 切换节点
        self.node_box.highlighted[str].connect(self.nodes_choice)
        # 切换用户
        self.accbox.highlighted[str].connect(self.print_value)
        # 保存用户
        self.Button_save.clicked.connect(self.save_acc)
        # 删除用户
        self.Button_del.clicked.connect(self.del_acc)
        # 读取账号信息
        self.Button_load_accmess.clicked.connect(self.acc)

        # 读取钱包信息
        self.Button_load_accwaller.clicked.connect(self.scot)


        # 点击钱包币种显示
        self.moneyWidget.clicked.connect(self.tokens)

        # 转账
        self.Button_trans.clicked.connect(self.bar)
        self.Button_trans.clicked.connect(self.steem_sbd)

        # Powerup & down
        self.Button_power.clicked.connect(self.powerups)
        # 取消POWERdown
        self.Button_cancer_power.clicked.connect(self.cancer_powerdown)
        # 取消所有订单
        self.Button_cancer.clicked.connect(self.marker_cance_all)
        # 兑换成STEEM
        self.Button_to_steem.clicked.connect(self.market_buy_steem)
        # 兑换成SBD
        self.Button_to_sbd.clicked.connect(self.market_buy_sbd)
        # 代理SP
        self.Button_daili.clicked.connect(self.daili)
        # 取消代理
        self.Button_daili_cancer.clicked.connect(self.canner_daili)

        # 查询代理
        self.Button_daili_towho.clicked.connect(self.def_daili_towho)
        self.Button_daili_who.clicked.connect(self.def_daili_who)

        # 见证人投票
        self.Button_witness_yes.clicked.connect(self.votewitness_yes)
        self.Button_witness_no.clicked.connect(self.votewitness_cancel)

        # 出售所有SCOT
        self.Button_scot_sell_all.clicked.connect(self.sell_all_scot)

        # steemp提现
        self.Button_steemp.clicked.connect(self.steemp_out)
        #获取账户创建票数量
        self.ticket_load.clicked.connect(self.ticker_number)
        # 索取账户创建票
        self.Button_rc.clicked.connect(self.new_ticket_rc)
        self.Button_3steem.clicked.connect(self.new_ticket_3steem)

        #创建账号
        self.Button_create_name_chack.clicked.connect(self.name_check)
        self.Button_create.clicked.connect(self.new_acc)
        self.Button_creante_mima.clicked.connect(self.password_random)
        

        # 窗口初始化
        self.thread = None  # 初始化线程

    #生成随机密码
    def password_random(self):
        player = self.create_name.text()
        if player == "":
            player="maiyude"
        num = random.sample("stringascii_letters", 10)
        strs = ''
        password = strs.join(num)
        owner_key = PasswordKey(player, password, role="owner")
        owner_key = owner_key.get_private()
        key = "P5" + (str(owner_key))[2:51]
        self.create_mima.setText(key)

    #检查名字
    def name_check(self):
        self.bar()
        nodes = self.nodes
        player=self.create_name.text()
        try:
            data = {"jsonrpc": "2.0", "method": "condenser_api.get_accounts", "params": [[player]], "id": 1}
            r = requests.post(url=nodes, json=data)
            rjson = r.json()
            if rjson["result"] == []:
                ok = 1
            else:
                ok = 0
        except:
            ok = 1
        if ok == 1:
            self.printmessage.setText("账户名可用")
        else:
            self.printmessage.setText("账户名不可用")
        self.funs()

    #创建账号
    def new_acc(self):
        self.bar()
        player = self.player.text()
        nodes = self.nodes
        key = self.key.text()
        account_name = self.create_name.text()
        password = self.create_mima.text()

        if player == "" or key == "" or account_name == "" or password == "":
            url = "请输入账号和密码"
        else:
            try:
                s = Steem(node=nodes, keys=[key])
                tx = s.create_claimed_account(account_name, creator=player, password=password)
                # 获取TXID
                tx = Signed_Transaction(tx)
                tx.data.pop("signatures", None)
                h = hashlib.sha256(bytes(tx)).digest()
                transaction_id = hexlify(h[:20]).decode("ascii")
                url = "https://steemd.com/tx/%s" % transaction_id
                print(url)
                try:
                    owner_key, posting_key, active_key, memo_key=self.keys(account_name,password)
                except:
                    print("haha")
                url=url+"\n"+"owner_key :"+str(owner_key) +"\n"+"posting_key :"+str(posting_key) +"\n"+"active_key :"+ str(active_key) +"\n"+"memo_key :"+str(memo_key)
            except Exception as e:
                url=str(e)
        self.printmessage.setText("完成\n" + url)
        self.funs()
        self.ticker_number()



    def keys(self,account_name,password):
        owner_key = PasswordKey(account_name, password, role="owner")
        posting_key = PasswordKey(account_name, password, role="posting")
        active_key = PasswordKey(account_name, password, role="active")
        memo_key = PasswordKey(account_name, password, role="memo")

        owner_key=owner_key.get_private()
        posting_key = posting_key.get_private()
        active_key = active_key.get_private()
        memo_key = memo_key.get_private()
        print(owner_key)
        return owner_key,posting_key,active_key,memo_key

    #索取账户创建票
    def new_ticket_rc(self):
        fee=None
        self.new_ticket(fee)
    def new_ticket_3steem(self):
        fee="3 STEEM"
        self.new_ticket(fee)

    def new_ticket(self,fee):
        self.bar()
        player = self.player.text()
        nodes = self.nodes
        key = self.key.text()
        if player == "" or key == "":
            url = "请输入账号和密码"
        else:
            try:
                s = Steem(node=nodes, keys=[key])
                tx = s.claim_account(player, fee=fee, steem_instance=s)
                #获取TXID
                tx = Signed_Transaction(tx)
                tx.data.pop("signatures", None)
                h = hashlib.sha256(bytes(tx)).digest()
                transaction_id = hexlify(h[:20]).decode("ascii")
                url = "https://steemd.com/tx/%s" % transaction_id
                print(url)
            except Exception as e:
                url=str(e)
        self.printmessage.setText("完成\n" + url)
        self.funs()


    #账户创建票数量
    def ticker_number(self):
        try:
            data={"jsonrpc":"2.0", "method":"database_api.find_accounts", "params": {"accounts":[self.player.text()]}, "id":1}
            r=requests.post(url=self.nodes,json=data)
            rjson=r.json()
            result=rjson["result"]["accounts"][0]["pending_claimed_accounts"]
            print(result)
            result=str(result)
        except:
            result="000"
        self.ticker_num.setText(result)

    #steemp提现
    def steemp_out(self):
        self.bar()
        url = ":)"
        player = self.player.text()
        nodes=self.nodes
        key=self.key.text()
        nums=self.steemp_num.text()

        if player == "" or key == "":
            url = "请输入账号和密码"
        else:
            try:
                nums=float(nums)
                s = Steem(keys=[key], node=nodes)
                json_data = {"contractName": "steempegged", "contractAction": "withdraw",
                             "contractPayload": {"quantity": str(nums)}}
                kk = s.custom_json('ssc-mainnet1', json_data, required_auths=[player])
                tx = Signed_Transaction(kk)
                tx.data.pop("signatures", None)
                h = hashlib.sha256(bytes(tx)).digest()
                transaction_id = hexlify(h[:20]).decode("ascii")
                url = "https://steemd.com/tx/%s" % transaction_id
                print(url)
                self.funs()
            except Exception as e:
                url=str(e)
                print(url)
        self.printmessage.setText("完成\n" + url)


    # 出售所有SCOT
    def sell_all_scot(self):
        self.bar()
        player = self.player.text()
        nodes=self.nodes
        key=self.key.text()
        url=":)"

        if player == "" or key == "":
            url = "请输入账号和密码"
        else:
            try:
                tokens=[]
                scot_balance=[]
                s = Steem(keys=[key], node=nodes)
                wallet = Wallet(player, steem_instance=s)
                scot = wallet.get_balances()
                for i in scot:
                    if float(i["balance"]) > 0:
                        tokens.append(i["symbol"])
                        scot_balance.append(i["balance"])
                print(tokens)
                print(scot_balance)
                try:
                    for i in range(len(tokens)):
                        try:
                            money_number=scot_balance[i]
                            token=tokens[i]
                            if token != "STEEMP":
                                price_market = sapi.find("market", "buyBook", query={'symbol': token})
                                price = price_market[-1]["price"]
                                print("出售:",token,money_number)
                                print("价格：", price)
                                print("数量：", money_number)
                                # 出售
                                money = float(money_number) * float(price)
                                money = float(money_number) * float(price)
                                print("价值：", money)
                                json_data = {"contractName": "market", "contractAction": "sell",
                                             "contractPayload": {"symbol": token, "quantity": str(money), "price": str(price)}}
                                kk = s.custom_json('ssc-mainnet1', json_data, required_auths=[player])
                                tx = Signed_Transaction(kk)
                                tx.data.pop("signatures", None)
                                h = hashlib.sha256(bytes(tx)).digest()
                                transaction_id = hexlify(h[:20]).decode("ascii")
                                url = "https://steemd.com/tx/%s" % transaction_id
                                print(url)
                                self.funs()
                        except:
                            pass
                except Exception as e:
                    url = str(e)
                    print(url)
            except Exception as e:
                url=str(e)
                print(url)
        self.printmessage.setText("完成\n" + url)


    def funs(self):
        num = random.randint(1, 100)
        self.dial_5.setProperty("value", num)
        self.dial_6.setProperty("value", num)

    # 清除左侧
    def cleaner_tree(self):
        self.moneyWidget.clear()

    # 见证人投票
    def votewitness_cancel(self):
        self.bar()
        approve = False
        self.votewitness(approve)
        self.funs()

    def votewitness_yes(self):
        self.bar()
        approve = True
        self.votewitness(approve)
        self.funs()

    def votewitness(self, approve=True):
        print("见证人投票")
        url = "error"
        nodes = self.nodes
        player = self.player.text()
        name = self.witness_to.text()
        key = self.key.text()
        print("投票", name, approve)
        if player == "" or key == "":
            url = "请输入账号和密码"
        else:
            try:
                s = Steem(keys=[key], node=nodes)
                acc = Account(player, steem_instance=s)
                list = name
                kk = acc.approvewitness(list, approve=approve)
                tx = Signed_Transaction(kk)
                tx.data.pop("signatures", None)
                h = hashlib.sha256(bytes(tx)).digest()
                transaction_id = hexlify(h[:20]).decode("ascii")
                url = "https://steemd.com/tx/%s" % transaction_id
                print(url)
                print("完成")
            except Exception as e:
                url = str(e)
                print(e)
        self.printmessage.setText("完成\n" + url)

    # 代理查询
    def def_daili_towho(self):
        self.dele(0)
        self.funs()
    def def_daili_who(self):
        self.dele(1)
        self.funs()
    def dele(self, num):  # num=0谁代理给你，num=1，你代理给谁
        self.bar()
        url = ":)"
        self.cleaner_tree()
        self.moneyWidget.headerItem().setText(0, "Name")
        who = self.daili_to_who.text()

        if who != "":
            try:
                deleli = []
                # 谁代理给你
                url1 = "http://test.steems.top:667/who?id=%s&hash=7DFC55A884A937A8AB81CD1EBAB3385E" % who
                url2 = "http://test.steems.top:667/towho?id=%s&hash=7DFC55A884A937A8AB81CD1EBAB3385E" % who
                url = [url1, url2]
                r = requests.get(url[num])

                delegators = r.json()
                delegatorss = []
                sps = []
                times = []

                for i in delegators["data"]:
                    if num == 0:
                        delegator = i["towho"]
                    else:
                        delegator = i["name"]
                    sp = int(i["sp"])
                    time = i["time"]
                    delegatorss.append(delegator)
                    sps.append(sp)
                    times.append(time)

                number = 0
                for i in range(len(sps)):
                    print(delegatorss[i], str(sps[i]))
                    item_0 = QtWidgets.QTreeWidgetItem(self.moneyWidget)
                    self.moneyWidget.topLevelItem(number).setText(0, delegatorss[i])
                    self.moneyWidget.topLevelItem(number).setText(1, str(sps[i]))
                    number += 1
            except Exception as e:
                url = str(e)
                print(e)
        # self.printmessage.setText("完成\n" + url)

    # 添加左侧选单
    def add_2(self):
        item_0 = QtWidgets.QTreeWidgetItem(self.moneyWidget)
        self.moneyWidget.topLevelItem(0).setText(0, "STEEM")
        self.moneyWidget.topLevelItem(0).setText(1, "0")
        item_0 = QtWidgets.QTreeWidgetItem(self.moneyWidget)
        self.moneyWidget.topLevelItem(1).setText(0, "SBD")
        self.moneyWidget.topLevelItem(1).setText(1, "0")

    # 取消代理
    def canner_daili(self):
        self.daili_num.setText("0")
        self.daili()
        self.funs()

    # 代理SP
    def daili(self):
        self.bar()
        print("代理SP")
        url = "error"
        nodes = self.nodes
        player = self.player.text()
        key = self.key.text()
        toplayer = self.daili_to.text()
        sp = self.daili_num.text()

        if player == "" or key == "":
            url = "请输入账号和密码"
        else:
            try:
                sp = float(sp)
            except:
                pass
            try:
                s = Steem(keys=[key], node=nodes)
                acc = Account(player, steem_instance=s)
                kk = acc.delegate_vesting_shares(
                    toplayer,
                    s.sp_to_vests(sp),
                    account=player
                )
                tx = Signed_Transaction(kk)
                tx.data.pop("signatures", None)
                h = hashlib.sha256(bytes(tx)).digest()
                transaction_id = hexlify(h[:20]).decode("ascii")
                url = "https://steemd.com/tx/%s" % transaction_id
                print(url)
                print("完成")
            except Exception as e:
                url = str(e)
                print(url)
        self.printmessage.setText("完成\n")
        self.funs()

    # 取消所有订单
    def marker_cance_all(self):
        self.bar()
        print("取消所有订单")
        url = "error"
        nodes = self.nodes
        player = self.player.text()
        key = self.key.text()

        if player == "" or key == "":
            url = "请输入账号和密码"
        else:
            try:
                s = Steem(keys=[key], node=nodes)
                mar = Market(steem_instance=s)
                order = mar.accountopenorders(account=player)
                url = []
                for i in order:
                    try:
                        orderid = i["orderid"]
                        print("取消订单", orderid)
                        kk = mar.cancel(orderid, account=player)
                        tx = Signed_Transaction(kk)
                        tx.data.pop("signatures", None)
                        h = hashlib.sha256(bytes(tx)).digest()
                        transaction_id = hexlify(h[:20]).decode("ascii")
                        url_1 = "https://steemd.com/tx/%s" % transaction_id
                        print(url_1)
                        url.append(url_1)
                        time.sleep(3)
                    except Exception as e:
                        url = str(e)
                        print(url)
            except Exception as e:
                url = str(e)
                print(url)
        url = str(url)
        self.printmessage.setText("完成\n" + url)
        self.funs()

    # 兑换成STEEM
    def market_buy_steem(self):
        self.bar()
        print("兑换成STEEM")
        url = "error"
        nodes = self.nodes
        player = self.player.text()
        key = self.key.text()
        amount = self.steem_to_sbd.text()
        try:
            amount = float(amount)
        except:
            pass
        if player == "" or key == "":
            url = "请输入账号和密码"
        else:
            try:
                s = Steem(keys=[key], node=nodes)
                mar = Market(steem_instance=s)
                ticker = mar.ticker(raw_data=False)
                lowest_ask = ticker["lowest_ask"]  # 购买STEEM价格
                buy_steem = float(lowest_ask) + 0.01
                buy_steem = 1 / buy_steem
                highest_bid = ticker["highest_bid"]  # 购买SBD价格
                buy_sbd = float(highest_bid) - 0.01
                buy_sbd = 1 / buy_sbd

                # 兑换成STEEM
                sell = mar.sell(buy_steem, amount, account=player)
                tx = Signed_Transaction(sell)
                tx.data.pop("signatures", None)
                h = hashlib.sha256(bytes(tx)).digest()
                transaction_id = hexlify(h[:20]).decode("ascii")
                url = "https://steemd.com/tx/%s" % transaction_id
                print(url)
                self.printmessage.setText("完成\n" + url)
                self.steem_acc()
            except Exception as e:
                print(e)
                url = str(e)

        self.printmessage.setText("完成\n" + url)
        self.funs()

    # 兑换成SBD
    def market_buy_sbd(self):
        self.bar()
        print("兑换成SBD")
        url = "error"
        nodes = self.nodes
        player = self.player.text()
        key = self.key.text()
        amount = self.steem_to_sbd.text()
        try:
            amount = float(amount)
        except:
            pass
        if player == "" or key == "":
            url = "请输入账号和密码"
        else:
            try:
                s = Steem(keys=[key], node=nodes)
                mar = Market(steem_instance=s)
                ticker = mar.ticker(raw_data=False)
                lowest_ask = ticker["lowest_ask"]  # 购买STEEM价格
                buy_steem = float(lowest_ask) + 0.01
                buy_steem = 1 / buy_steem
                highest_bid = ticker["highest_bid"]  # 购买SBD价格
                buy_sbd = float(highest_bid) - 0.01
                buy_sbd = 1 / buy_sbd
                amount = round(amount / buy_sbd, 3)
                # 兑换成SBD
                buy = mar.buy(buy_sbd, amount, account=player)
                tx = Signed_Transaction(buy)
                tx.data.pop("signatures", None)
                h = hashlib.sha256(bytes(tx)).digest()
                transaction_id = hexlify(h[:20]).decode("ascii")
                url = "https://steemd.com/tx/%s" % transaction_id
                print(url)
                self.printmessage.setText("完成\n" + url)
                self.steem_acc()
            except Exception as e:
                url = str(e)
                print(url)

        self.printmessage.setText("完成\n" + url)
        self.funs()

    # power up & downm
    def powerups(self):
        self.bar()
        url = "error"
        print("使用节点", self.nodes)
        key = self.key.text()
        player = self.player.text()
        player = player.lower()
        print("power up & down")

        if player == "" or key == "":
            url = "请输入账号和密码"
        else:
            power1 = self.power_up.text()
            power2 = self.power_down.text()
            if power1 != "" and power2 != "":
                url = "UP和DOWN填一个即可,请检查"
                print(url)
            else:
                s = Steem(keys=[key], node=self.nodes)
                acc = Account(player, steem_instance=s)

                if power1 != "":
                    try:
                        power1 = float(power1)
                    except Exception as e:
                        print(e, "power1")
                    amount = power1
                    print("开始powerup", "数量:", amount)
                    try:
                        tx = acc.transfer_to_vesting(amount, to=player)
                        tx = Signed_Transaction(tx)
                        tx.data.pop("signatures", None)
                        h = hashlib.sha256(bytes(tx)).digest()
                        transaction_id = hexlify(h[:20]).decode("ascii")
                        url = "https://steemd.com/tx/%s" % transaction_id
                        print(url)
                    except Exception as e:
                        print(e)
                        url = str(e)

                if power2 != "":
                    if power2 == "cancel":
                        print("取消POWERDOWN")
                        power2 = 0
                    try:
                        power2 = float(power2)
                    except Exception as e:
                        print(e, "power2")
                    amount = power2
                    print("开始powerdown", "数量:", amount)
                    if amount != 0:
                        amount = acc.steem.sp_to_vests(amount)
                    else:
                        amount = 0
                    try:
                        tx = acc.withdraw_vesting(amount)
                        tx = Signed_Transaction(tx)
                        tx.data.pop("signatures", None)
                        h = hashlib.sha256(bytes(tx)).digest()
                        transaction_id = hexlify(h[:20]).decode("ascii")
                        url = "https://steemd.com/tx/%s" % transaction_id
                        print(url)
                    except Exception as e:
                        print(e)
                        url = str(e)
            self.printmessage.setText("完成\n" + url)
            self.steem_acc()
        self.printmessage.setText("完成\n" + url)
        self.funs()

    def cancer_powerdown(self):
        self.power_down.setText("cancel")
        self.powerups()
        self.funs()

    # 转账steem_sbd_hive_hbd,scot
    def steem_sbd(self):
        self.bar()
        print("转账使用节点", self.nodes)
        print("转账")
        self.printmessage.setText("转账")
        key = self.key.text()
        player = self.player.text()
        if player == "" or key == "":
            url = "请输入账号和密码"
        else:
            token = self.trans_token.text()
            token = token.upper()
            mymoney = self.trans_num.text()
            mymoney = float(mymoney)
            toplayer = self.trans_to.text()
            memo = self.trans_memo.text()

            if token == "HIVE" or token == "HBD":
                print("hive转账")
                self.printmessage.setText("hive转账")
                hiv = Steem(keys=[key], nodes=node2)
                account = Account(player, steem_instance=hiv)
                kk = account.transfer(toplayer, mymoney, token, memo)

                tx = Signed_Transaction(kk)
                tx.data.pop("signatures", None)

                h = hashlib.sha256(bytes(tx)).digest()
                transaction_id = hexlify(h[:20]).decode("ascii")

                url = "https://hiveblocks.com/tx/%s" % transaction_id
                print("转账完成")
                print(url)

            if token == "STEEM" or token == "SBD":
                s = Steem(keys=[key], node=self.nodes)
                account = Account(player, steem_instance=s)
                # 转账
                kk = account.transfer(toplayer, mymoney, token, memo)

                tx = Signed_Transaction(kk)
                tx.data.pop("signatures", None)

                h = hashlib.sha256(bytes(tx)).digest()
                transaction_id = hexlify(h[:20]).decode("ascii")

                url = "https://steemd.com/tx/%s" % transaction_id
                print("转账完成")
                print(url)
                self.steem_acc()
            else:
                print("scot转账")
                s = Steem(keys=[key], node=self.nodes)
                contract_payload = {'symbol': token, 'to': toplayer, 'quantity': str(mymoney), 'memo': memo}
                json_data = {'contractName': 'tokens', 'contractAction': 'transfer',
                             'contractPayload': contract_payload}
                kk = s.custom_json('ssc-mainnet1', json_data, required_auths=[player])
                tx = Signed_Transaction(kk)
                tx.data.pop("signatures", None)
                h = hashlib.sha256(bytes(tx)).digest()
                transaction_id = hexlify(h[:20]).decode("ascii")
                url = "https://steemd.com/tx/%s" % transaction_id
                print(url)
                print("转账完成")
        self.printmessage.setText("转账完成\n" + url)
        self.funs()

    # 获取scot信息
    def scot(self):
        self.bar()
        self.moneyWidget.headerItem().setText(0, "Token")
        print("使用节点", self.nodes)
        try:
            steem_ban = self.moneyWidget.topLevelItem(0).text(1)
            if steem_ban != "STEEM":
                self.cleaner_tree()
                self.add_2()
        except:
            pass

        try:
            steem_ban = self.moneyWidget.topLevelItem(0).text(1)
            sbd_ban = self.moneyWidget.topLevelItem(1).text(1)
        except Exception as e:
            print(e)
        print("获取信息中")
        token = []
        scot_balance = []
        player = self.player.text()

        if player != "":
            if steem_ban == "0" and sbd_ban == "0":
                print("acc")
                self.acc()
            try:

                data = {"jsonrpc": "2.0", "method": "condenser_api.get_accounts", "params": [[player]], "id": 1}
                response = requests.post(url=node2, data=json.dumps(data))
                rjson = response.json()

                # 获取print(steem_balance,sbd_balance)
                steem_balance = rjson["result"][0]["balance"]
                sbd_balance = rjson["result"][0]["sbd_balance"]
                steem_balance = str(steem_balance).replace("HIVE", "")
                steem_balance = float(steem_balance)
                sbd_balance = str(sbd_balance).replace("HBD", "")
                sbd_balance = float(sbd_balance)

                scot_balance.append(steem_balance)
                scot_balance.append(sbd_balance)
                token.append("HIVE")
                token.append("HBD")
            except:
                pass

            print("获取信息中---")

            try:
                s = Steem(node=self.nodes)
                wallet = Wallet(player, steem_instance=s)
                scot = wallet.get_balances()
                for i in scot:
                    if float(i["balance"]) > 0:
                        token.append(i["symbol"])
                        scot_balance.append(i["balance"])

            except:
                token.append("error")
                scot_balance.append("999999")

            print("获取信息中------")

            nums = 2
            for i in range(len(token)):
                try:
                    item_0 = QtWidgets.QTreeWidgetItem(self.moneyWidget)
                    self.moneyWidget.topLevelItem(nums).setText(0, token[i])
                    self.moneyWidget.topLevelItem(nums).setText(1, str(scot_balance[i]))
                    nums += 1
                except Exception as e:
                    print("错误", i)
                    print(e)

        print("完成")
        self.printmessage.setText("获取完成！")
        self.funs()

    # 切换节点
    def nodes_choice(self, i):
        self.nodes = i
        self.funs()

    # 点击币种转账
    def tokens(self, index):
        item = self.moneyWidget.currentItem()
        token = item.text(0)
        self.trans_token.setText(token)
        self.funs()

    # 读取数据库的用户
    def additem(self):
        self.accbox.clear()
        con = sqlite3.connect('acc.db')
        cur = con.cursor()
        whois = 'select * from acc '
        cur.execute(whois)
        vip = cur.fetchall()
        con.commit()
        con.close()
        for i in vip:
            self.accbox.addItem(i[0])
        # self.printmessage.setText(str(vip))
        self.funs()

    # 保存用户到数据库
    def save_acc(self):

        con = sqlite3.connect('acc.db')
        cur = con.cursor()
        player = self.player.text()
        player = player.lower()
        key = self.key.text()
        print("保存账号:", player)
        try:
            whois = 'REPLACE INTO acc (player, password) VALUES(?,?)'
            cur.execute(whois, (player, key))
            con.commit()
            con.close()
            print("已保存")
            self.printmessage.setText("已保存")
        except Exception as e:
            print(e)
            self.printmessage.setText(str(e))
        self.additem()
        self.funs()

    # 数据库删除用户
    def del_acc(self):
        con = sqlite3.connect('acc.db')
        cur = con.cursor()
        player = self.player.text()
        player = player.lower()
        print("删除账号:", player)
        try:
            delete_sql = 'delete from acc where player = "%s"' % player
            print(delete_sql)
            cur.execute(delete_sql)
            con.commit()
            con.close()
            print("已删除")
            self.printmessage.setText("已删除")
        except Exception as e:
            print(e)
            self.printmessage.setText(str(e))
        self.additem()
        self.funs()

    # 读取数据库用户，输入到player和key
    def print_value(self, i):
        self.player.setText(i)
        player = i
        player = player.lower()
        con = sqlite3.connect('acc.db')
        cur = con.cursor()
        whois = 'select * from acc where player = "%s" ' % player
        cur.execute(whois)
        mima = cur.fetchall()
        con.commit()
        self.key.setText(mima[0][1])
        self.cleaner_tree()
        self.add_2()
        self.funs()

    # 读取账户信息
    def acc(self):
        self.bar()
        self.moneyWidget.headerItem().setText(0, "Token")
        print("使用节点", self.nodes)
        print("获取信息中")
        try:
            steem_ban = self.moneyWidget.topLevelItem(0).text(1)
            if steem_ban != "STEEM":
                self.cleaner_tree()
                self.add_2()
        except:
            pass
        self.printmessage.setText("获取信息中")
        player = self.player.text()
        player = player.lower()
        sp = sp_de = voting = down = rc = steem_balance = sbd_balance = 0
        try:
            # 详细SP信息
            if player != "":
                data = {"jsonrpc": "2.0", "method": "condenser_api.get_accounts", "params": [[player]], "id": 1}
                response = requests.post(url=self.nodes, data=json.dumps(data))
                rjson = response.json()
                ticket=rjson["result"][0]["pending_claimed_accounts"]
                self.ticker_num.setText(str(ticket))
                # 获取voting_power,downvote_per
                downvote_mana = rjson["result"][0]["downvote_manabar"]["current_mana"]
                voting_manabar = rjson["result"][0]["voting_manabar"]["current_mana"]
                voting_power = rjson["result"][0]["voting_power"]
                if float(voting_manabar) > 100000 and float(downvote_mana) > 100000 and int(voting_power) == 0:
                    voting_power = 10000
                try:
                    downvote_per = float(downvote_mana) / (float(voting_manabar) / float(voting_power) * 25)
                except:
                    downvote_per = 0
                if downvote_per >= 99.5:
                    downvote_per = 100
                down = int(downvote_per)
                voting = int(voting_power) / 100
                self.voting_bar.setProperty("value", voting)
                self.down_bar.setProperty("value", down)

                # 获取print(steem_balance,sbd_balance)
                steem_balance = rjson["result"][0]["balance"]
                sbd_balance = rjson["result"][0]["sbd_balance"]
                steem_balance = str(steem_balance).replace("STEEM", "")
                steem_balance = float(steem_balance)
                sbd_balance = str(sbd_balance).replace("SBD", "")
                sbd_balance = float(sbd_balance)
                self.moneyWidget.topLevelItem(0).setText(1, str(steem_balance))
                self.moneyWidget.topLevelItem(1).setText(1, str(sbd_balance))

                print("获取信息中---")

                # 获取print(sp_de, "SP")
                vesting_shares = rjson["result"][0]["vesting_shares"]
                vesting_shares = str(vesting_shares).replace("VESTS", "")
                vesting_shares = float(vesting_shares)
                sp_de = vesting_shares / 1955.466
                sp_de = int(sp_de)

                # 获取SP
                delegated_vesting_shares = rjson["result"][0]["delegated_vesting_shares"]
                delegated_vesting_shares = str(delegated_vesting_shares).replace("VESTS", "")
                delegated_vesting_shares = float(delegated_vesting_shares)

                received_vesting_shares = rjson["result"][0]["received_vesting_shares"]
                received_vesting_shares = str(received_vesting_shares).replace("VESTS", "")
                received_vesting_shares = float(received_vesting_shares)

                vesting_withdraw_rate = rjson["result"][0]["vesting_withdraw_rate"]
                vesting_withdraw_rate = str(vesting_withdraw_rate).replace("VESTS", "")
                vesting_withdraw_rate = float(vesting_withdraw_rate)

                # 获取SP
                sp = vesting_shares + received_vesting_shares - delegated_vesting_shares - vesting_withdraw_rate
                sp = float(sp) / 1955.466
                sp = int(sp)
                message = "%s sp   steem power：%s SP" % (sp, sp_de)
                self.sp_mess.setText(message)

                print("获取信息中------")

            try:
                response = ""
                cnt2 = 0
                while str(response) != '<Response [200]>' and cnt2 < 10:
                    data = {"jsonrpc": "2.0", "method": "rc_api.find_rc_accounts", "params": {"accounts": [player]},
                            "id": 1}
                    response = requests.post(self.nodes, json=data)
                    rjson = response.json()
                    rc = rjson["result"]["rc_accounts"]
                    max_rc = float(rc[0]["max_rc"])
                    rc_manabar = float(rc[0]["rc_manabar"]["current_mana"])
                    rate = (rc_manabar / max_rc) * 100
                    cnt2 += 1
                rc = int(rate)
                self.rcbar.setProperty("value", rc)


            except Exception as e:
                print(e)
                rc = 0
            self.printmessage.setPlainText("获取完成" + "\n" + ":)")
            print("读取完毕")

        except Exception as e:
            print(e)
            sp = sp_de = voting = down = rc = steem_balance = sbd_balance = 0
            self.printmessage.setText("出现了一些错误")
        self.funs()


        

    def steem_acc(self):
        # 详细SP信息
        self.bar()
        player = self.player.text()
        if player != "":
            data = {"jsonrpc": "2.0", "method": "condenser_api.get_accounts", "params": [[player]], "id": 1}
            response = requests.post(url=self.nodes, data=json.dumps(data))
            rjson = response.json()

            # 获取print(steem_balance,sbd_balance)
            steem_balance = rjson["result"][0]["balance"]
            sbd_balance = rjson["result"][0]["sbd_balance"]
            steem_balance = str(steem_balance).replace("STEEM", "")
            steem_balance = float(steem_balance)
            sbd_balance = str(sbd_balance).replace("SBD", "")
            sbd_balance = float(sbd_balance)
            self.moneyWidget.topLevelItem(0).setText(1, str(steem_balance))
            self.moneyWidget.topLevelItem(1).setText(1, str(sbd_balance))
        self.funs()


    def bar(self):
        # 创建线程
        self.pbar.show()
        self.par_text.show()
        self.thread = Runthread()
        # 连接信号
        self.thread._signal.connect(self.call_backlog)  # 进程连接回传到GUI的事件
        # 开始线程
        self.thread.start()


    def call_backlog(self, msg):
        self.pbar.setValue(int(msg))  # 将线程的参数传入进度条
        if int(msg) % 10 == 0:
            self.funs()
        if int(msg) >= 99:
            self.pbar.hide()
            self.par_text.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = cure.Windows(CamShow(), 'trayname', 'blueDeep', 'steems.top', 'myicon.ico')
    sys.exit(app.exec_())