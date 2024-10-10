#!/bin/bash

# installing pip package
if [ -f "setup.py" ]; then
    workdir=$(pwd)
else
    workdir=/usr/src/mytonctrl
fi

cd $workdir
pip3 install -U pip .

# update /usr/bin/mytonctrl
echo "    Updating /usr/bin/mytonctrl"
cat <<EOF > /usr/bin/mytonctrl
#!/bin/bash
/usr/bin/python3 -m mytonctrl \$@
EOF
chmod +x /usr/bin/mytonctrl
