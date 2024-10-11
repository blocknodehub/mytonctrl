import os

import pkg_resources

from mypylib.mypylib import color_print
from modules.pool import PoolModule


class SingleNominatorModule(PoolModule):

    description = 'Orbs\'s single nominator pools.'
    default_value = False

    def do_create_single_pool(self, pool_name, owner_wallet_name):
        self.ton.local.add_log("start create_single_pool function", "debug")

        self.check_download_pool_contract_scripts()

        file_path = self.ton.poolsDir + pool_name
        if os.path.isfile(file_path + ".addr"):
            self.ton.local.add_log("create_single_pool warning: Pool already exists: " + file_path, "warning")
            return

        fift_script = pkg_resources.resource_filename('mytoncore', 'contracts/single-nominator-pool/init.fif')
        code_boc = pkg_resources.resource_filename('mytoncore', 'contracts/single-nominator-pool/single-nominator-code.hex')
        validator_wallet = self.ton.GetLocalWallet(owner_wallet_name)
        args = [fift_script, code_boc, validator_wallet.addrB64, validator_wallet.addrB64, file_path]
        print(" ".join(args))
        result = self.ton.fift.Run(args)
        if "Saved single nominator pool" not in result:
            raise Exception("create_single_pool error: " + result)

        pools = self.ton.GetPools()
        new_pool = self.ton.GetLocalPool(pool_name)
        for pool in pools:
            if pool.name != new_pool.name and pool.addrB64 == new_pool.addrB64:
                new_pool.Delete()
                raise Exception("create_single_pool error: Pool with the same parameters already exists.")

    def new_single_pool(self, args):
        try:
            pool_name = args[0]
            owner_wallet_name = args[1]
        except:
            color_print("{red}Bad args. Usage:{endc} new_single_pool <pool-name> <owner_wallet_name>")
            return
        self.do_create_single_pool(pool_name, owner_wallet_name)
        color_print("new_single_pool - {green}OK{endc}")

    def do_activate_single_pool(self, pool, owner_wallet_name):
        self.local.add_log("start activate_single_pool function", "debug")
        boc_mode = "--with-init"
        validator_wallet = self.ton.GetLocalWallet(owner_wallet_name)
        self.ton.check_account_active(validator_wallet.addrB64)
        result_file_path = self.ton.SignBocWithWallet(validator_wallet, pool.bocFilePath, pool.addrB64_init, 1, boc_mode=boc_mode)
        self.ton.SendFile(result_file_path, validator_wallet)

    def activate_single_pool(self, args):
        try:
            pool_name = args[0]
            owner_wallet_name = args[1]
        except:
            color_print("{red}Bad args. Usage:{endc} activate_single_pool <pool-name> <owner_wallet_name>")
            return
        pool = self.ton.GetLocalPool(pool_name)
        if not os.path.isfile(pool.bocFilePath):
            self.local.add_log(f"Pool {pool_name} already activated", "warning")
            return
        self.do_activate_single_pool(pool, owner_wallet_name)
        color_print("activate_single_pool - {green}OK{endc}")

    def withdraw_from_single_pool(self, args):
        try:
            pool_addr = args[0]
            amount = float(args[1])
        except:
            color_print("{red}Bad args. Usage:{endc} withdraw_from_single_pool <pool-addr> <amount>")
            return
        self.ton.WithdrawFromPoolProcess(pool_addr, amount)
        color_print("withdraw_from_single_pool - {green}OK{endc}")
    #end define

    def add_console_commands(self, console):
        console.AddItem("new_single_pool", self.new_single_pool, self.local.translate("new_single_pool_cmd"))
        console.AddItem("activate_single_pool", self.activate_single_pool, self.local.translate("activate_single_pool_cmd"))
        console.AddItem("withdraw_from_single_pool", self.withdraw_from_single_pool, self.local.translate("withdraw_from_single_pool_cmd"))
