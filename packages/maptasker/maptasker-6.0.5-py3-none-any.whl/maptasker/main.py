"""Main entry point for maptasker"""
#! /usr/bin/env python3

#                                                                                      #
# Main: MapTasker entry point                                                          #
#                                                                                      #
# MIT License   Refer to https://opensource.org/license/mit                            #

import sys

from maptasker.src import mapit


def main() -> None:
    """
    Kick off the main program: mapit.pypwd

    """

    # Call the core function passing an empty filename
    return_code = mapit.mapit_all("")

    sys.exit(return_code)


if __name__ == "__main__":
    # FOR DEVELOPMENT ONLY  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # The following outputs a file "maptasker_profile.txt" with a breakdown of
    # function calls

    # import cProfile
    # import pstats

    # cProfile.run("main()", "results")
    # with open("maptasker_profile.txt", "w") as file:
    #     profile = pstats.Stats("results", stream=file).sort_stats("ncalls")
    #     profile.print_stats()
    #     file.close()

    main()
