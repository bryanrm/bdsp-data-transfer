# Created by Bryan R Martinez on 11/17/2016
import bluetooth
import sys

uuid = "f1239387-98b2-4dce-a7d5-635ce03572a0"  # must match app uuid
config_file = "config"  # name of config file
data_file = "data.txt"  # edit this to change file data being sent


# returns data in specified data file
def get_data():
    try:
        f = open(data_file)
        data = f.read()
        f.close()
    except IOError:
        data = 'Error: Could not retrieve data'
    return data


# connects to server and sends data
# if save flag is true, save device address
def send_data(address, save):
    print(address)
    service_matches = bluetooth.find_service(uuid=uuid, address=address)
    if len(service_matches) == 0:
        return False
    else:
        match = service_matches[0]
        port = match["port"]
        name = match["name"]
        host = match["host"]

        print("Connecting to \"%s\" on %s" % (name, host))

        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((host, port))
        sock.send(get_data())
        sock.close()

        if save:
            return save_bt_address(address)
        else:
            return True


# saves bt address in config file
def save_bt_address(address):
    reset()
    try:
        f = open(config_file, 'w')
        f.write(address)
        f.close()
        return True
    except IOError:
        print("Error storing address")
        return False


# run with /r or /reset arg
# resets stored bt address
def reset():
    try:
        open(config_file, 'w').close()
    except IOError:
        sys.exit(0)


# performs device discovery, always returns paired devices
def search():
    devices = bluetooth.discover_devices(duration=1)
    return devices


def main(argv):
    if (len(argv) > 1) and ((argv[1] == '/r') or (argv[1] == '/reset')):
        reset()
    else:
        try:
            config = open(config_file)
            bt_address = config.readline()
            config.close()
            if bt_address == '':
                results = search()
                if results is not None:
                    for address in results:
                        result = send_data(address, save=True)
                        if result:
                            break
                else:
                    print("No devices found")
            else:
                send_data(bt_address, save=False)
        except IOError:
            reset()


if __name__ == "__main__":
    main(sys.argv)
