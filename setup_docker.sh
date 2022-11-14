if ! command -v docker 2>/dev/null; then
	echo "docker not found: please install"
fi

docker build -t main_interface .
