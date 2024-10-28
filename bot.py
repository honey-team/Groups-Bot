import argparse, os

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    parser.add_argument("-t", "--token", default=None)
    args = parser.parse_args()

    if args.action == "run":
        if args.token:
            with open("data/token.env", "w") as tf:
                tf.write(args.token)
        import main

if __name__ == "__main__":
    main()