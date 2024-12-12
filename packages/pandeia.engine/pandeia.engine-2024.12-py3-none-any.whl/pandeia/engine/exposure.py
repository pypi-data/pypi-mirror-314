# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import numpy.ma as ma
from .custom_exceptions import EngineInputError, DataError

class ExposureSpec:
    """
    Parent class for all exposure times, MultiAccum and SingleAccum
    """
class ExposureSpec_MultiAccum(ExposureSpec):
    """
    Parent class for MultiAccum
    """

    def __init__(self, config={}, webapp=False, **kwargs):
        """
        Create a generic Exposure Specification.

        Inputs
        ------
        config: dict
            dictionary of detector configuration setups

        webapp: bool
            Switch to toggle strict API checking
            
        **kwargs: keyword/value pairs
            Additional configuration data
        """
        self.webapp = webapp

        # Required parameters
        self.readout_pattern = config["input_detector"]["readout_pattern"]
        self.subarray = config["input_detector"]["subarray"]
        self.ngroup = config["input_detector"]["ngroup"]
        self.nint = config["input_detector"]["nint"]
        self.nexp = config["input_detector"]["nexp"]
        self.tframe = config["subarray"]["default"][self.subarray]["tframe"]
        self.tfffr = config["subarray"]["default"][self.subarray]["tfffr"]
        if self.readout_pattern in config["subarray"] and self.subarray in config["subarray"][self.readout_pattern]:
            self.tframe = config["subarray"][self.readout_pattern][self.subarray]["tframe"]
            self.tfffr = config["subarray"][self.readout_pattern][self.subarray]["tfffr"]

        # these errors specifically name the properties by their engine 
        # internal name; the client will catch errors for the web interface 
        # and thus the engine will never trigger this for web users. 
        # (JETC-1957)
        if not isinstance(self.ngroup, int):
            raise EngineInputError("ngroups must be an integer, got {}".format(type(self.ngroup)))
        if not isinstance(self.nint, int):
            raise EngineInputError("nint must be an integer, got {}".format(type(self.nint)))
        if not isinstance(self.nexp, int):
            raise EngineInputError("nexp must be an integer, got {}".format(type(self.nexp)))

        # Optional parameters
        # These are defined by the Instrument's reference data as Instrument properties.
        self.nframe = config["readout_pattern"][self.readout_pattern]["nframe"]
        self.ndrop2 = config["readout_pattern"][self.readout_pattern]["ndrop2"]

        self.nprerej = config["detector_config"]["nprerej"]
        self.npostrej = config["detector_config"]["npostrej"]
        # Going from general to specific: start with the default reset values, then check the defaults, then check
        # the actual readout pattern for this subarray. Use the most appropriate reset values for this setup, otherwise
        # the defaults
        self.nreset1 = 1
        self.nreset2 = 1
        if "nreset1" in config["subarray"]["default"][self.subarray]:
            self.nreset1 = config["subarray"]["default"][self.subarray]["nreset1"]
            self.nreset2 = config["subarray"]["default"][self.subarray]["nreset2"]
        if self.readout_pattern in config["subarray"] and self.subarray in config["subarray"][self.readout_pattern]:
            if "nreset1" in config["subarray"][self.readout_pattern][self.subarray]:
                self.nreset1 = config["subarray"][self.readout_pattern][self.subarray]["nreset1"]
                self.nreset2 = config["subarray"][self.readout_pattern][self.subarray]["nreset2"]
        if "nreset1" in config["readout_pattern"][self.readout_pattern]:
            self.nreset1 = config["readout_pattern"][self.readout_pattern]["nreset1"]
            self.nreset2 = config["readout_pattern"][self.readout_pattern]["nreset2"]


        # These are never specified in our data, currently; they were always the default
        # value from the ExposureSpec __init__ signature.
        if "ndrop1" in config["readout_pattern"][self.readout_pattern]:
            self.ndrop1 = config["readout_pattern"][self.readout_pattern]["ndrop1"]
        else:
            self.ndrop1 = 0
        if "ndrop3" in config["readout_pattern"][self.readout_pattern]:
            self.ndrop3 = config["readout_pattern"][self.readout_pattern]["ndrop3"]
        else:
            self.ndrop3 = 0
        self.frame0 = False
        if "frame0" in config["subarray"]["default"][self.subarray]:
            self.frame0 = config["subarray"]["default"][self.subarray]["frame0"]
        if self.readout_pattern in config["subarray"] and self.subarray in config["subarray"][self.readout_pattern]:
            if "frame0" in config["subarray"][self.readout_pattern][self.subarray]:
                self.nreset1 = config["subarray"][self.readout_pattern][self.subarray]["frame0"]

        # If these are trivial, we don't have to define them.
        if "nsample" in config["readout_pattern"][self.readout_pattern]:
            self.nsample = config["readout_pattern"][self.readout_pattern]["nsample"]
            self.nsample_skip = config["readout_pattern"][self.readout_pattern]["nsample_skip"]
        else:
            self.nsample = 1
            self.nsample_skip = 0

        # Target acqs only use a subset of the groups
        if "ngroup_extract" in config["input_detector"]:
            self.ngroup_extract = config["input_detector"]["ngroup_extract"]

        self.get_times()

        # Derived quantities
        self.nramps = self.nint * self.nexp

    def get_times(self):
        """
        The time formulae are defined in Holler et al. 2021, JWST-STScI-006013-A. Note
        that we have to subtract the groups that are rejected (by the pipeline) from the
        measurement time (nprerej+npostrej). The saturation time conservatively considers
        the ramp saturated even if saturation occurs in a rejected frame.

        Also note that these equations are generic, suitable for both H2RG and SiAs
        detectors.

        The equations in this method are duplicated in the front-end (workbook.js,
        update_detector_time_labels function). Please ensure that changes to these
        equations are reflected there.
        """

        self.tgroup = self.tframe * (self.nframe + self.ndrop2)

        # MIRI measurement time for ngroups < 5 is now handled with dropframes
        # This reduces to Equation 3 for H2RG detectors and Equation 5 for SiAs detectors.
        if self.ngroup == 1:
            # in the special case of a single group, the measurement is between the
            # superbias frame and the end of the only group (JETC-3290)
            self.measurement_time = self.nint * self.tframe * self.ngroup * (self.nframe + self.ndrop2)
        else:
            self.measurement_time = self.nint * self.tframe * (self.ngroup - 1 - self.nprerej - self.npostrej) * (self.nframe + self.ndrop2)
        # Equation 4
        if self.frame0:
            self.measurement_time += 0.5 * self.nint * self.tframe * (self.nframe - 1)

        # Equation 1, which naturally simplifies to Equation 2 for SiAs detectors.
        self.exposure_time = (self.tfffr * self.nint) + self.tframe * (self.nreset1 + (self.nint - 1) * self.nreset2 +
                                self.nint * (self.ndrop1 + (self.ngroup - 1) * (self.nframe + self.ndrop2) +
                                self.nframe + self.ndrop3))

        # Equation 6, which reduces to Equation 7 for SiAs detectors.
        self.saturation_time = self.tframe * (self.ndrop1 + (self.ngroup - 1) * (self.nframe + self.ndrop2) + self.nframe)

        self.duty_cycle = self.saturation_time * self.nint / self.exposure_time
        self.total_exposure_time = self.nexp * self.exposure_time
        self.exposures = self.nexp

        self.total_integrations = self.nexp * self.nint

class ExposureSpec_H2RG(ExposureSpec_MultiAccum):

    pass


class ExposureSpec_SiAs(ExposureSpec_MultiAccum):

    def get_times(self):
        """
        SiAs detectors obey the time formulae defined in Holler et al. 2021,
        JWST-STScI-006013-A. They need two additional values defined, which we compute
        here.
        """
        super().get_times()

        # This is where we adjust values so we can still use the same
        # MULTIACCUM formula as for the NIR detectors. We need the effective
        # "average time per sample" for MIRI.
        self.tsample = self.tframe / (self.nsample + self.nsample_skip)
        # 'nsample_total' for MIRI is the total number of non-skipped samples X number of averaged frames.
        # Note that in practice, it currently never happens that both the number of samples and number of
        # averaged frames are >1 (i.e., no SLOWGRPAVG exists). However, this will deal with that situation,
        # should it occur.
        self.nsample_total = self.nframe * self.nsample


class ExposureSpec_UnevenMultiAccum(ExposureSpec):

    def __init__(self, config={}, webapp=False, **kwargs):
        """
        Create a generic UnevenMultiAccum Exposure Specification.

        Inputs
        ------
        config: dict
            dictionary of detector configuration setups

        webapp: bool
            Switch to toggle strict API checking
            
        **kwargs: keyword/value pairs
            Additional configuration data
        """
        self.webapp = webapp

        # Required parameters
        self.ma_table_name = config["input_detector"]["ma_table_name"].lower()
        self.subarray = config["input_detector"]["subarray"]
        self.nresultants = config["input_detector"]["nresultants"]
        self.nexp = config["input_detector"]["nexp"]
        
        try:
            self.ma_table = config["readout_pattern"][self.ma_table_name]
        except KeyError:
            raise EngineInputError(f"Invalid MA Table name: {self.ma_table_name}")

        self.tframe = self.ma_table["frame_time"]
        self.treset = self.ma_table["reset_read_time"]
        self.nreset = self.ma_table["reset_reads"]
        self.reference_downlink = False
        self.reset_downlink = False
        self.nreference = 0
        # subtract_reference_read is no longer guaranteed to be in MA Tables.
        if "subtract_reference_read" in self.ma_table and self.ma_table["subtract_reference_read"]:
            self.nreference = 1
        if "resultant_type" in self.ma_table["resultants"][0] and self.ma_table["resultants"][0]["resultant_type"] == "Reference": # If it's taken AND downlinked...
            self.reference_downlink = True # Don't need to count the reference read specially if it's downlinked
        if "resultant_type" in self.ma_table["resultants"][0] and self.ma_table["resultants"][0]["resultant_type"] == "ResetRead": # If it's downlinked...
            self.reset_downlink = True
        

        self.max_total_samples = self.ma_table["max_samples"]
        self.max_resultants = self.ma_table["max_resultants"]
        self.min_resultants = self.ma_table["min_resultants"]
        # Allow a simple "maximum number of resultants" option
        if self.nresultants == -1:
            self.nresultants = self.max_resultants

        if self.nresultants > self.max_resultants:
            raise EngineInputError(f"MA Table {self.ma_table_name} supports a maximum of {self.max_resultants} resultants.")
        if self.nresultants < 1:
            raise EngineInputError(f"MA Table {self.ma_table_name} supports a minimum of {self.min_resultants} resultants.")

        # we've read the full table, now consider only out to the requested stopping
        # point.
        try:
            self.readout_pattern = self._enumerate_pattern()[:self.nresultants]
            self.readout_pattern_full = self._enumerate_pattern()
        except TypeError:
            raise EngineInputError(f"Number of resultants ({self.nresultants}) must be an integer.")

        # Get number of reads in each resultant
        self.nreads = np.array([len(i) for i in self.readout_pattern])
        # Get total number of frames (read and unread) in each resultant
        first = np.array([i[0] for i in self.readout_pattern ])
        self.lastframe = [i[-1] for i in self.readout_pattern]
        self.lastframe_full = [i[-1] for i in self.readout_pattern_full]
        self.ntotal = np.append(len(self.readout_pattern[0]), np.diff(self.lastframe))
        
        self.max_samples = self.readout_pattern[-1][-1]

        self.get_times()

    def _enumerate_pattern(self):
        """
        Given an MA Table pattern description, write out the list of resultants and frames in each resultant

        Returns
        -------
        readout_pattern: list
            A list of resultants, where each resultant is a list of consitituent frames.
        """
        resultants = self.ma_table["resultants"]
        readout_pattern = []
        frame_counter = 1
        if "resultant_type" in resultants[0]:
            if resultants[0]["resultant_type"] == "Reference":
                frame_counter -= self.nreference
            elif resultants[0]["resultant_type"] == "ResetRead":
                frame_counter -= self.nreset

        for idx, resultant in enumerate(resultants):
            frames = frame_counter + resultant["pre_resultant_skips"] + np.arange(resultant["read_frames"])
            readout_pattern.append(list(frames))
            frame_counter += resultant["pre_resultant_skips"] + resultant["read_frames"]

        return readout_pattern

    def get_times(self):
        """
        UnevenMultiaccum detectors follow the multiaccum table definitions specified in the Roman PRD
        (Roman-STScI-000058 revision J, section 4.6.2) with the addition of the saturation time (utilizing the fact
        that the detector IS exposing on-sky during the reference read, S. Gomez private
        communication) which is not precisely the total_accumulated_exposure_time
        
        The equations in this method are duplicated in the front-end (workbook.js,
        update_detector_time_labels function). Please ensure that changes to these
        equations are reflected there.
        """

        # The frame-based time between the middle of the first and middle of the last readout
        # Equivalent to total_effective_exposure_time in the PRD (4.6.2, 2.1.14.6)
        # If the reference exists but is not downlinked, it still matters for the exposure time
        resultant_map = self.ntotal
        if self.reset_downlink: # remove the reset, so we can treat it the same way we do resets (with its own reset time)
            resultant_map = resultant_map[self.nreset:]
        if not self.reference_downlink and self.nreference > 0: # insert the reference if it's not already in the resultant table, just for time calcs
            resultant_map = np.insert(resultant_map, 0, self.nreference)

        if len(resultant_map) <= self.nreference or (len(resultant_map) == 0 and self.reset_downlink == True): # there IS a chance of an empty resultant_map, if resultants=1 and the reset frame is downlinked.
            self.measurement_time = 0
        else:
            self.measurement_time = (np.sum(resultant_map[self.nreference:-1]) + self._midpoint(-1)) * self.tframe

        # The total time spent on one exposure, including resets
        # Total number of frames + optional reference read (part of the resultant_map, above) + reset read
        # Equivalent to total_integration_duration in the PRD (4.6.2, 2.1.14.7)
        self.exposure_time = self.nreset * self.treset + np.sum(resultant_map) * self.tframe

        # The total time spent exposing this observation (exposure time, times number of exposures)
        self.total_exposure_time = self.exposure_time * self.nexp

        # The time that's important for computing saturation; the time spent collecting photons.
        # This is the total_accumulated_exposure_time (4.6.2, 2.1.14.5) plus the reference read.
        self.saturation_time = np.sum(resultant_map) * self.tframe

        self.duty_cycle = self.saturation_time/self.exposure_time
        self.nramps = self.nexp
        self.exposures = self.nexp
        self.total_integrations = self.nexp

    def _midpoint(self, resultantnum):
        """
        Helper function to just get the midpoint of the particular resultant

        Parameters
        ----------
        resultantnum : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        if resultantnum == -1:
            resultantnum = self.nresultants-1
        resultant = self.ma_table["resultants"][resultantnum]
        skip = resultant["pre_resultant_skips"]
        reads = resultant["read_frames"]

        return skip + reads/2.

class ExposureSpec_H4RG(ExposureSpec_UnevenMultiAccum):

    pass

class ExposureSpec_SingleAccum(ExposureSpec):
    """
    Parent class for SingleAccum
    """

    def __init__(self, config={}, webapp=False, **kwargs):
        """
        Create a single accum Exposure Specification.

        Inputs
        ------
        config: dict
            dictionary of detector configuration setups

        webapp: bool
            Switch to toggle strict API checking

        **kwargs: keyword/value pairs
            Additional configuration data

        """
        self.webapp = webapp

        self.time = config["input_detector"]["time"]

        # Required parameters
        #self.readout_pattern = config["input_detector"]["readout_pattern"]
        #self.subarray = config["input_detector"]["subarray"]
        if "nexp" in config["input_detector"]:
            raise DataError("SingleAccum calculations cannot use nexp")
        self.nsplit = config["input_detector"]["nsplit"]

        self.get_times()

        # Derived quantities needed for the generic noise equation
        self.nramps = 1

    def get_times(self):
        """
        The following times are defined for use in Pandeia to parallel JWST usage.


        See also ExposureSpec_SingleAccum.set_time()
        """
        # measurement time is the time from the first measurement to the last read of the
        # exposure. HST has no skipped or dropped frames; this is simply the time for one
        # frame.
        self.measurement_time = self.time / self.nsplit

        # exposure time is the total time of one exposure (including any skipped reads,
        # reset reads, and the like - HST doesn’t have them.)
        self.exposure_time = self.time / self.nsplit

        # saturation time is the time the detector spends collecting photons between
        # resets, including skipped and dropped reads. It is the time that saturation
        # calculations depend on.
        self.saturation_time = self.time / self.nsplit

        # total exposure time is the time for the entire observation, including all
        # exposures and all the resets and skipped frames.
        self.total_exposure_time = self.time

        self.duty_cycle = self.saturation_time/self.exposure_time
        self.total_integrations = self.nsplit
        self.exposures = self.nsplit


class ExposureSpec_CCD(ExposureSpec_SingleAccum):

    pass

class ExposureSpec_H1R(ExposureSpec_CCD):

    pass

class ExposureSpec_MAMA(ExposureSpec_SingleAccum):

    pass

class ExposureSpec_XDL(ExposureSpec_MAMA):

    pass
