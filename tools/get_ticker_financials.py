"""
Save income statement to a file
"""

from secpy.secpy_client import SECPyClient
from secpy.tools import generate_financials
from secpy.utils.path import get_project_dir, create_dir
import configargparse
from pathlib import Path

def get_args():
    """Arguments parser."""
    parser = configargparse.ArgumentParser(description=__doc__)
    parser.add_argument('--save-dir', type=Path, help='save dir',default=None)
    parser.add_argument('--ticker', type=str, help='company ticker')
    # parser.add_argument('--form', type=str, default='10-Q', help='Quarterly or annually. 10-K or 10-Q')
    parser.add_argument('--overwrite', action='store_true', help='If overwrite, the file will be overwritten')
    parser.add_argument('--save', action='store_true', help='If True, the financials will be saved.')
    parser.add_argument('--plot', action='store_true', help='If True, the financials will be plotted.')
    parser.add_argument('--start-year', default=None, type=int, help='Starting year of the plots. If not defined, all the values will be plotted.')
    args = parser.parse_args()
    return args

def run(args):
    project_dir = get_project_dir()
    client = SECPyClient("<YOUR USER-AGENT>")
    ticker = args.ticker
    # form = args.form
    save_dir = args.save_dir
    save = args.save 
    overwrite = args.overwrite
    plot = args.plot
    start_year = args.start_year
    if save_dir == None: 
        save_dir = project_dir / 'data' / ticker
    assert create_dir(save_dir)  

    generate_financials(client,ticker,start_year,save_dir,save,plot,overwrite)

if __name__ == '__main__':
    args = get_args()
    run(args)



# with open('fundamental_analysis_keys_dei.txt', 'w') as f:
#     for key in my_dict['dei'].__dict__.keys():
#         f.write(key+'\n')

# for key, value in my_dict:
#     print(key)

# print(msft)