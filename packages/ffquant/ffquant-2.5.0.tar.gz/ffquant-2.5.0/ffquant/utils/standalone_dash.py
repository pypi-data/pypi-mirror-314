import argparse
import os
import ffquant.plot.dash_graph as dash_graph
import pickle

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Standalone program for showing backtest results\n")
    parser.add_argument('file_path', type=str, help='pickle file path')
    parser.add_argument('--task_id', type=str, required=False, help='Task ID(Default: None)', default=None)
    parser.add_argument('--debug', action='store_true', help="Enable or disable debugging mode")
    args = parser.parse_args()

    if not os.path.isfile(args.file_path):
        print(f"{args.file_path} does not exist or is not a file\n")
        exit(1)

    backtest_data = None
    with open(args.file_path, 'rb') as f:
        backtest_data = pickle.load(f)
    dash_graph.show_perf_graph(backtest_data, is_live=False, task_id=args.task_id, debug=args.debug)