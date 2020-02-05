# -*- coding: utf-8 -*-
'''
    pygeodiff.main
    --------------
    Main entry of the library
    :copyright: (c) 2019 Peter Petrik
    :license: MIT, see LICENSE for more details.
'''

from .geodifflib import GeoDiffLib


class GeoDiff:
    """
        if libname is None, it tries to import c-extension from wheel
        messages are shown in stdout. Use environment variable GEODIFF_LOGGER_LEVEL 0(Nothing)-4(Debug) to
        set level (Errors by default)
    """
    def __init__(self, libname=None):
        self.clib = GeoDiffLib(libname)

    """
     Assign custom logger
     Replace default stdout logger with custom.
     Based on maxLogLevel, the messages are filtered by level:
     maxLogLevel = 0 nothing is passed to logger callback
     maxLogLevel = 1 errors are passed to logger callback
     maxLogLevel = 2 errors and warnings are passed to logger callback
     maxLogLevel = 3 errors, warnings and infos are passed to logger callback
     maxLogLevel = 4 errors, warnings, infos, debug messages are passed to logger callback
    """
    def set_logging(self, callback, maxLevel):
        return self.clib.set_logging(callback, maxLevel)

    """
        Creates changeset file (binary) in such way that
        if CHANGESET is applied to BASE by applyChangeset,
        MODIFIED will be created

        BASE --- CHANGESET ---> MODIFIED

        \param base [input] BASE sqlite3/geopackage file
        \param modified [input] MODIFIED sqlite3/geopackage file
        \param changeset [output] changeset between BASE -> MODIFIED

        raises SqliteDiffError on error
    """
    def create_changeset(self, base, modified, changeset):
        return self.clib.create_changeset(base, modified, changeset)

    """
        Inverts changeset file (binary) in such way that
        if CHANGESET_INV is applied to MODIFIED by applyChangeset,
        BASE will be created

        \param changeset [input] changeset between BASE -> MODIFIED
        \param changeset_inv [output] changeset between MODIFIED -> BASE
        
        \returns number of conflics

        raises SqliteDiffError on error
    """

    def invert_changeset(self, changeset, changeset_inv):
        return self.clib.invert_changeset(changeset, changeset_inv)

    """ 
        Rebases local modified version from base to modified_their version
  
               --- > MODIFIED_THEIR
        BASE -|
               ----> MODIFIED (local) ---> MODIFIED_THEIR_PLUS_MINE
   
        Steps performed on MODIFIED (local) file:
        1. undo local changes MODIFIED -> BASE
        2. apply changes from MODIFIED_THEIR
        3. apply rebased local changes and create MODIFIED_THEIR_PLUS_MINE
 
        Note, when rebase is not successfull, modified could be in random state.
        This works in general, even when base==modified, or base==modified_theirs
        
         \param base [input] BASE sqlite3/geopackage file
         \param modified_their [input] MODIFIED sqlite3/geopackage file
         \param modified [input] local copy of the changes to be rebased
         \param conflict [output] file where the automatically resolved conflicts are stored
         \returns number of conflicts
         
         raises SqliteDiffError on error
    """
    def rebase(self, base, modified_their, modified, conflict):
        return self.clib.rebase(base, modified_their, modified, conflict)

    """ 
        Creates changeset file (binary) in such way that
        if CHANGESET is applied to MODIFIED_THEIR by
        applyChangeset, the new state will contain all
        changes from MODIFIED and MODIFIED_THEIR.

               --- CHANGESET_THEIR ---> MODIFIED_THEIR --- CHANGESET ---> MODIFIED_THEIR_PLUS_MINE
        BASE -| 
               -----------------------> MODIFIED

         \param base [input] BASE sqlite3/geopackage file
         \param modified [input] MODIFIED sqlite3/geopackage file
         \param changeset_their [input] changeset between BASE -> MODIFIED_THEIR
         \param changeset [output] changeset between MODIFIED_THEIR -> MODIFIED_THEIR_PLUS_MINE
         \param conflict [output] file where the automatically resolved conflicts are stored
         \returns number of conflicts

         raises SqliteDiffError on error
    """
    def create_rebased_changeset(self, base, modified, changeset_their, changeset, conflict):
        return self.clib.create_rebased_changeset(base, modified, changeset_their, changeset, conflict)

    """
        Applies changeset file (binary) to BASE
        
        \param base [input/output] BASE sqlite3/geopackage file
        \param changeset [input] changeset to apply to BASE
        \returns number of conflicts
        
        raises SqliteDiffError on error
    """
    def apply_changeset(self, base, changeset):
        return self.clib.apply_changeset(base, changeset)

    """ 
        Lists changeset content JSON file
        JSON contains all changes in human/machine readable name
        \returns number of changes
         
         raises SqliteDiffError on error
    """
    def list_changes(self, changeset, json):
        return self.clib.list_changes(changeset, json)

    """ 
        \returns whether changeset contains at least one change
        
        raises SqliteDiffError on error
    """

    """ 
        Lists changeset summary content JSON file 
        JSON contains a list of how many inserts/edits/deletes is contained in changeset for each table
        \returns number of changes

         raises SqliteDiffError on error
    """

    def list_changes_summary(self, changeset, json):
        return self.clib.list_changes_summary(changeset, json)

    """ 
        \returns whether changeset contains at least one change

        raises SqliteDiffError on error
    """

    def has_changes(self, changeset):
        return self.clib.has_changes(changeset)

    """ 
        \returns number of changes

         raises SqliteDiffError on error
    """

    def changes_count(self, changeset):
        return self.clib.changes_count(changeset)

    """
       geodiff version
    """
    def version(self):
        return self.clib.version()


def main():
    diff_lib = GeoDiff()
    print("pygeodiff " + diff_lib.version())
