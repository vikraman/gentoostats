
import logging
import os
import platform
import portage
from _emerge.actions import relative_profile_path

class Environment(object):
    """
    A class encapsulating all environment and portage variable providers
    """

    def __init__(self):
        """
        Initialize the class and portdir
        """
        self.portdir = portage.settings['PORTDIR']

    def getVar(self, myvar):
        """
        Return the value of a portage variable
        """
        return portage.settings[myvar]

    def getPlatform(self):
        """
        Return host platform
        """
        return platform.platform(aliased=1)

    def getLastSync(self):
        """
        Return portage tree last sync time
        """
        lastsync = None
        try:
            lastsync = portage.grabfile(os.path.join(self.portdir, 'metadata', 'timestamp.chk'))
        except portage.exception.PortageException:
            pass
        if lastsync is None:
            return 'Unknown'
        return lastsync[0]

    def getProfile(self):
        """
        Return selected portage profile
        """
        profilever = None
        profile = portage.settings.profile_path
        if profile:
            profilever = relative_profile_path(self.portdir, profile)
            if profilever is None:
                try:
                    for parent in portage.grabfile(os.path.join(profile, 'parent')):
                        profilever = relative_profile_path(self.portdir, os.path.join(profile, parent))
                        if profilever is not None:
                            break
                except portage.exception.PortageException:
                    pass

                if profilever is None:
                    try:
                        profilever = '!' + os.readlink(profile)
                    except (OSError):
                        pass

        if profilever is None:
            profilever = 'Unknown'

        return profilever
