#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
# File              : custom_filter.py
# Date              : 2024-12-31 12:12:39
# Last Modified time: 2025-01-02 14:22:20
#
# Author:           : Christophe Vermeren
#

import re
from datetime import datetime
from typing import Optional, List, Union


class FilterModule(object):
    '''
    A class to define custom filters for processing content, specifically for
    finding the latest image of a specified Linux distribution.
    '''

    '''
        ██████  ██    ██ ██████  ██      ██  ██████
        ██   ██ ██    ██ ██   ██ ██      ██ ██
        ██████  ██    ██ ██████  ██      ██ ██
        ██      ██    ██ ██   ██ ██      ██ ██
        ██       ██████  ██████  ███████ ██  ██████
    '''

    def filters(self) -> dict:
        ''' filters
            Returns a dictionary of filter functions that can be used in
            templates or processing pipelines.

            Returns:
                dict: A dictionary mapping filter names to their corresponding
                      methods.
        '''
        return {
            'lastest_image': self.latest_image,
        }

    def latest_image(
            self,
            content: str,
            distro: Union[List[str], str]) -> Optional[Union[List[str], str]]:
        ''' latest_image
            Finds the latest available image for a specified Linux distribution
            (distro) within the provided HTML content.

            Args:
                self: Reference to the class instance. (Not used in this
                      function but kept for class structure.)
                content (str): The HTML content from which to extract image
                               information.
                distro (list|str): The name of the distribution to search for
                                   (e.g., "debian").

            Returns:
                List: A list containing the filenames of the latest image
                       Returns None if no matching images are found.
        '''

        if isinstance(distro, list):
            latest_images = []

            for el in distro:
                image = self.__find(content, el)

                if image is not None:
                    latest_images.append(image)
            return latest_images if latest_images else None

        elif isinstance(distro, str):
            return [self.__find(content, distro)]

        else:
            return None

    '''
    ██████  ██████  ██ ██    ██  █████  ████████ ███████
    ██   ██ ██   ██ ██ ██    ██ ██   ██    ██    ██
    ██████  ██████  ██ ██    ██ ███████    ██    █████
    ██      ██   ██ ██  ██  ██  ██   ██    ██    ██
    ██      ██   ██ ██   ████   ██   ██    ██    ███████
    '''

    def __find(self, content: str, distro: str) -> Optional[list]:
        ''' __find
            Finds the latest version of a given Linux distribution in the
            provided content.

            Args:
                content (str): The HTML content to search through.
                distro (str): The name of the Linux distribution to look for.

            Returns:
                Optional[str]: The filename of the latest version's image or
                               None if not found.
        '''

        # Regular expression to find distro versions with .tar.gz, .tar.zst,
        # or .tar.xz extensions. Also extracts the associated date in
        # DD-MMM-YYYY format
        pattern = r"href=\"([^\"]*" + distro + \
            "[^\"]*amd64.tar.[(zst|gz|xz)]*)\"" + \
            ".*?([0-9]{2}-[A-Za-z]{3}-[0-9]{4})"

        # Find all matches using the regex pattern
        matches = re.findall(pattern, content)

        if matches:
            # Convert the extracted dates to a uniform format (YYYY-MM-DD)
            updated_content = [
                (name, datetime.strptime(
                    date,
                    "%d-%b-%Y").strftime("%Y-%m-%d"))
                for name, date in matches
            ]

            # Sort by date and return the latest entry
            latest = sorted(updated_content, key=lambda x: x[1])[-1]
            return latest[0]

        else:
            # Return None if no matches are found
            return None
