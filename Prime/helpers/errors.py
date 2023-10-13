# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

class Errors:
    """
    ## Errors

    ### Arguments:

        None
    """

    class SpamFailed(Exception):
        """
        Raises when the spam task was failed
        """

    class DownloadFailed(Exception):
        """
        Raises when the download task was failed
        """

    class DelAllFailed(Exception):
        """
        Raises when the del all function was failed
        """
