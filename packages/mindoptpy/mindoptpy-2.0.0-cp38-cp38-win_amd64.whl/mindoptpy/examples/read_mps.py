from mindoptpy import *
import argparse


if __name__ == "__main__":

    # Register arguments.
    parser = argparse.ArgumentParser(description='Run MindOpt.')
    parser.add_argument('--filename', type=str, default='../data/afiro.mps', help='Input LP/MPS filename.')
    args = parser.parse_args()
    filename = args.filename

    print("Started MindOpt.")
    print(" - Filename  : {0}".format(filename))

    env = Env()
    env.start()
    model = read(filename, env)

    try:
        model.optimize()
        print(f"Optimal objective value is: {model.objval}")


    except MindoptError as e:
        print("Received MindOpt exception.")
        print(" - Code          : {}".format(e.errno))
        print(" - Reason        : {}".format(e.message))
    except Exception as e:
        print("Received exception.")
        print(" - Reason        : {}".format(e))
    finally:
        model.dispose()