import argparse
import subprocess
import os


def main():
    description = 'Run a command in docker'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--test', required=False, default='app')

    args, extra_params = parser.parse_known_args()

    test_cmd = "pytest -s -q /philo/tests/{}".format(
        args.test)

    # test_cmd = 'pip3 install  webcolors'

    cmd_entrypoint = "docker-compose run --rm --volume={}/../:/philo python sh -c".format(os.getcwd())
    cmd = cmd_entrypoint.split(" ")
    cmd.append(test_cmd)

    try:
        subprocess.call(cmd)

    except Exception:
        subprocess.run(cmd)


if __name__ == '__main__':
    main()
