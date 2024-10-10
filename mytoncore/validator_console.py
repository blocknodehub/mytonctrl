import subprocess


class ValidatorConsole:
	def __init__(self, local):
		self.local = local
		self.appPath = "/opt/tonmain/core/validator-engine-console"
		self.privKeyPath = "/mnt/tonmain/conf/keys/client"
		self.pubKeyPath = "/mnt/tonmain/conf/keys/server.pub"
		self.addr = "127.0.0.1:43678"
	#end define

	def Run(self, cmd, **kwargs):
		console_timeout = self.local.db.console_timeout if self.local.db.console_timeout else 3
		timeout = kwargs.get("timeout", console_timeout)
		if self.appPath is None or self.privKeyPath is None or self.pubKeyPath is None:
			raise Exception("ValidatorConsole error: Validator console is not settings")
		args = [self.appPath, "-k", self.privKeyPath, "-p", self.pubKeyPath, "-a", self.addr, "-v", "0", "--cmd", cmd]
		print(" ".join(args))
		process = subprocess.run(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
		output = process.stdout.decode("utf-8")
		err = process.stderr.decode("utf-8")
		if len(err) > 0:
			self.local.add_log("args: {args}".format(args=args), "error")
			raise Exception("ValidatorConsole error: {err}".format(err=err))
		return output
	#end define
#end class
