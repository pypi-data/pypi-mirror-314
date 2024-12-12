#! /usr/bin/env python3

from nmdb.parser import nmdb_parser

# --------------------------------------------------------------------------
def main():
    """Entry point for the application script"""
    parser = nmdb_parser()
    # add subparsers!
    args = parser.parse_args()
    #args.func(args)

    if args.verbose > 2:
        print(f"Running '{__file__}'")
    if args.verbose:
        print(args)

    if args.cmd is None:
        parser.print_help()

    if (args.cmd == "status"):
        print("calling status")
    elif (args.cmd == "realtime"):
        print("calling realtime")
        from nmdb.realtime import realtime
        data = realtime(args)
        print(data)
    elif (args.cmd == "download"):
        print("calling download")
    elif (args.cmd == "upload"):
        from nmdb.upload import upload
        upload(args)
    elif (args.cmd == "revise"):
        print("calling revise")
    elif (args.cmd == "alert"):
        print("calling alert")
    else:
        print("command not recognized")
    
    if not args.quiet:
        print("Ready.")


# --------------------------------------------------------------------------
if __name__ == '__main__':
    main()

# BUG unset PYTHONPATH otherwise old nmdb versions will be executed...
# but without PYTHONPATH nmrena_kiel3.sh does not work (used nmdb3)...
# TODO convert nmrena import script, include in nmdb tool
