import logging
import os

from beelzebub.base import INIT_CONF
from beelzebub.base.__main__ import parse_cmdln, update_conf_from_cmdln
from beelzebub.md_iso import MdjsonToISO19115_2

PROGNAME = 'beelzebub_md_iso'
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)

def main():
    args = parse_cmdln(prog=PROGNAME)
    conf = update_conf_from_cmdln(INIT_CONF, args)

    x = MdjsonToISO19115_2(conf=conf)
    x.run(args.in_file, args.out_file)

    if args.out_file == '-':
        print(x.writer.output, end='')

if __name__ == '__main__':
    main()

