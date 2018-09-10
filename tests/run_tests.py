import argparse
import subprocess


def main():
    description = 'Run a command in docker'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--container_id', help='Run to docker ps to get the container id ',
        required=True)

    parser.add_argument('--test', required=False, default='app')

    args, extra_params = parser.parse_known_args()

    test_cmd = 'pytest -s -q /philo/tests/{}'.format(
        args.test)
    #test_cmd = 'pip3 install flask-cors'
    #print(test_cmd)
    cmd = [
        'docker',
        'exec',
        '-it',
        args.container_id,
        'sh',
        '-c',
        test_cmd

    ]

    try:
        subprocess.call(cmd)

    except Exception:
        subprocess.run(cmd)

if __name__ == '__main__':
    main()
