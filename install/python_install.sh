# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root."
    exit 1
fi

# Check the distribution
if [ -f /etc/os-release ]; then
    source /etc/os-release
    distro="$ID"
else
    echo "Unsupported distribution."
    exit 1
fi

# Install Python based on the distribution
case "$distro" in
    debian|ubuntu)
        apt update
        apt install -y python3
        ;;
    fedora)
        dnf install -y python3
        ;;
    centos|rhel)
        yum install -y python3
        ;;
    *)
        echo "Unsupported distribution: $distro"
        exit 1
        ;;
esac

echo "Python has been installed successfully."
