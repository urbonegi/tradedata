import argparse
import os

from lib.app import app, activate_job

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'common')


parser = argparse.ArgumentParser(description='Start flask webserver.')
parser.add_argument('--dir', type=str, default=DEFAULT_DATA_DIR,
                    help='Trade client-provided data dir. Defaults to {}'.format(DEFAULT_DATA_DIR))
parser.add_argument('--host', type=str, default='0.0.0.0',
                    help='Flask webserver host. Default to "0.0.0.0".')
parser.add_argument('--port', type=int, default=8080,
                    help='Flask webserver port. Default to "8080".')


if __name__=='__main__':
    args = parser.parse_args()
    activate_job(args.dir)
    app.run(host=args.host, port=args.port)
