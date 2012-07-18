from lego_alpha_team.pac import PACFile

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3:
        f = PACFile(sys.argv[len(sys.argv) - 1])
        if sys.argv[1] == "list":
            if sys.argv[2] == "all":
                f.print_all_entries()
            else:
                f.print_entry(sys.argv[2])
        elif sys.argv[1] == "extract":
            if sys.argv[2] == "all":
                f.extract_all()
            else:
                f.extract(sys.argv[2])
    else:
        f = PACFile("lego_alpha_team/Etc.pac")
        f.print_all_entries()