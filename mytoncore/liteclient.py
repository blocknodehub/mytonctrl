import random
import subprocess


class LiteClient:
	def __init__(self, local):
		self.local = local
		self.appPath = "/opt/tonmain/core/lite-client"
		self.configPath = "/mnt/tonmain/conf/global.json"
		self.pubkeyPath = "/mnt/tonmain/conf/keys/liteserver.pub"
		self.addr = "127.0.0.1:43679"
	#end define

	def Run(self, cmd, **kwargs):
		index = kwargs.get("index")
		timeout = kwargs.get("timeout", 60)
		useLocalLiteServer = kwargs.get("useLocalLiteServer", True)
		args = [self.appPath, "--global-config", self.configPath, "--verbosity", "0", "--cmd", cmd]
		if index is not None:
			index = str(index)
			args += ["-i", index]
		elif useLocalLiteServer and self.pubkeyPath:
			args = [self.appPath, "--addr", self.addr, "--pub", self.pubkeyPath, "--verbosity", "0", "--cmd", cmd]
		else:
			liteServers = self.local.db.get("liteServers")
			if liteServers is not None and len(liteServers):
				index = random.choice(liteServers)
				index = str(index)
				args += ["-i", index]
		#end if
		print(" ".join(args))

		process = subprocess.run(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
		output = process.stdout.decode("utf-8")
		err = process.stderr.decode("utf-8")
		if len(err) > 0:
			self.local.add_log("args: {args}".format(args=args), "error")
			raise Exception("LiteClient error: {err}".format(err=err))
		return output
	#end define
#end class
