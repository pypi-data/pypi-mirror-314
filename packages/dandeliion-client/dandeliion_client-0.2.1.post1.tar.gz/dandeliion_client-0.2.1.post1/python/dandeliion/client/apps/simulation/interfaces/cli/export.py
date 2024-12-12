import argparse
import json
import sys
from dandeliion.client.apps.simulation import Simulation
from .connection import connect


def export():

    parser = argparse.ArgumentParser(description='Export Dandeliion simulation as BPX.')
    parser.add_argument(
        'id',
        metavar='JOB_ID',
        help='simulation job id'
    )
    parser.add_argument(
        '-o',
        '--outfile',
        metavar='OUT_FILE',
        help='output file',
    )
    parser.add_argument(
        '-c',
        '--credentials',
        metavar='CRED_FILE',
        default=None,
        help='path to a Dandeliion credential file'
    )

    args = parser.parse_args()

    try:
        connect(credentials=args.credentials)
        sim = Simulation.get(pk=args.id)
        with open(args.outfile, 'w') as fb:
            json.dump(sim.to_bpx(), fb)
    except Exception as e:
        print(f'Something went wrong while exporting model: {e}')
        sys.exit(1)

    print(f'Simulation model written in BPX format to {args.outfile}')
