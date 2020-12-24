import argparse

from vsom import VsomTester


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--vsom', '-v', type=str, help='VSOM VMS Ip Address')
    parser.add_argument('--user', '-u', type=str, help='VSOM VMS User ID')
    parser.add_argument('--password', '-p', type=str, help='VSOM VMS User Password')
    parser.add_argument('--verify', '-t', action='store_true', help='(False, True) Use TLS')
    parser.add_argument('--camera', '-c', type=str, help='VSOM VMS Camera name')
    parser.add_argument('--playback', '-b', type=int, help='Playback time')

    args = parser.parse_args()

    return args


def main():

    args = parse_args()
    vsom = VsomTester(args.vsom, args.user, args.password, verify=args.verify)
    stream_url = vsom.get_streaming(args.camera)

    print(stream_url)


if __name__ == '__main__':

    main()
