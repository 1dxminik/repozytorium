import argparse
parser = argparse.ArgumentParser()
parser.add_argument('greeting', help='the greeting message displayed')
parser.add_argument('-n', '--numbers', type=float, nargs='*',
                    help='the numbers to be added')
parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2],
                    help='helps with smth')

args = parser.parse_args()
print(args)

print(args.numbers)


if args.verbosity is None:
    print(args.greeting)
    if args.numbers is not None:
        print(sum(args.numbers))