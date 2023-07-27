###############################################################################
# 
# File: histplot.py
# Author: Rongqian Qian
# Date Created: 2023-1-3
#
#Purpose: Define the function used in Histogram plots.
#
#
###############################################################################





from ROOT import *
import numpy as np

from datetime import datetime, timedelta ,date
from dateutil.relativedelta import relativedelta
from sMDT import db, tube
from sMDT.data import status
from sMDT.data.status import UMich_Status

import sys


def status_selection(isGood,tube_status):
    """return the status of tube
    
    Args:
        isGood: 
        the status of the tube that is choosen to selected.

        tube_status:
        the status of the tube that needs to be selected
    """
    if tube_status == "PASS":
        if isGood == status.Status.PASS:
            return(1)

    if tube_status == "INCOMPLETE":
        if isGood == status.Status.INCOMPLETE:
            return(1)
    
    if tube_status == "FAIL":
        if isGood == status.Status.FAIL:
            return(1)

    if tube_status == "INCLUSIVE":
            return(1)

    if tube_status == "PASS or FAIL":
        if isGood == status.Status.PASS or isGood == status.Status.FAIL:
            return(1)

    return(0)

def UM_status_selection(isGood,tube_status):
    """return the UM status of tube
    
    Args:
        isGood: 
        the status of the tube that is choosen to selected.

        tube_status:
        the status of the tube that needs to be selected
    """
    if tube_status == "PASS":
        if isGood == UMich_Status.PASS:
            return(1)

    if tube_status == "INCOMPLETE":
        if isGood == UMich_Status.UMICH_INCOMPLETE:
            return(1)
    
    if tube_status == "FAIL":
        if isGood == UMich_Status.FAIL:
            return(1)

    if tube_status == "PASS or FAIL":
        if isGood == UMich_Status.PASS or isGood == UMich_Status.FAIL:
            return(1)

    if tube_status == "INCLUSIVE":
        if isGood == UMich_Status.UMICH_INCOMPLETE or isGood == UMich_Status.PASS:
            return(1)

    return(0)



def Selected_test_status(Pass_Fail):
    """
    Return the status of the test.
    """
    if Pass_Fail == "All":  
        return  "All" 

    if Pass_Fail == False:
        return "Pass"

    if Pass_Fail == True:
        return  "Fail"  
          


def UM_selected_test_status(test_result,wanted_result):
    """
    Return the status whether the test fail. So if the arg is False, return "PASS".
    Args:
        test_result:
        the status of the tube that needs to be selected

        wanted_result: 
        the status of the tube that is choosen to selected.
    """
    if wanted_result == "PASS or FAIL":
        if test_result == UMich_Status.PASS:
            return(1)

    if wanted_result == "PASS":
        if test_result == UMich_Status.PASS:
            return(1)

    if wanted_result == "FAIL":
        if test_result == UMich_Status.FAIL:
            return(1)


    if wanted_result == "INCOMPLETE":
        if test_result == UMich_Status.UMICH_INCOMPLETE:
            return(1)

    if wanted_result == "INCLUSIVE":
            return(1)

    return(0)

def overflow_fill(hist):
    """Add the overflow of the TH1F into the last bin"""
    nbins = hist.GetNbinsX()
    hist.SetBinContent(nbins,hist.GetBinContent(int(nbins))+hist.GetBinContent(int(nbins+1)))
    hist.SetBinError(nbins,np.sqrt(hist.GetBinError(int(nbins))**2+hist.GetBinError(int(nbins+1))**2))
    return(hist)

def get_dark_current(tube, min_date):
    """Return the last record after the minimum date of dark current , whether pass the test and the ID of the tube."""
    try:
        if tube.dark_current.get_record('last').date > min_date:
            return (tube.dark_current.get_record('last').dark_current,tube.dark_current.get_record('last').fail(),tube.dark_current.get_record('last').date)
    except (IndexError,TypeError):
        return None

def get_UMich_dark_current(tube, min_date):
    """Return the UM record after the minimum date of dark current , whether pass the test and the ID of the tube."""
    try:
        return (tube.umich_dark_current.get_record('last').umich_dark_current,tube.umich_dark_current.status(),tube.get_ID())
    except (IndexError,TypeError):
        return None

def get_leak(tube, min_date, max_date = datetime.now()):
    """Return the last record of leakage after the minimum date and before the maximum date, whether pass the test and the ID of the tube."""
    try:
        if tube.leak.get_record('last').date > min_date and tube.leak.get_record('last').date < max_date:
            return (tube.leak.get_record('last').leak_rate,tube.leak.get_record('last').fail(),tube.get_ID())
    except (IndexError,TypeError):
        return None

def get_UMich_leak(tube, min_date):
    """Return the UM record of leakage after the minimum date, whether pass the test and the ID of the tube."""
    try:
        print(tube.umich_leak.get_record('last').leak_rate)
        return (tube.umich_leak.get_record('last').umich_leak,tube.umich_leak.status(),tube.get_ID())
    except (IndexError,TypeError):
        return None

def get_tension1(tube, min_date):
    """Return the last record of tension after the minimum date and before the tube was swaged, whether pass the test and the ID of the tube."""
    swage_records = sorted([record for record in tube.swage.m_records if record.date], key=lambda rec: rec.date)
    swage_length_rec = None
    try:  # gets the first SwageRecord with a value for swage_length
        swage_length_rec = next(rec for rec in swage_records if rec.swage_length and rec.date.date() > min_date)
    except StopIteration:
        # tube has no swage length recorded
        pass
    if swage_length_rec:  # only consider the tensions if the tube has been swaged
        # sort tension records by date
        tension_records = sorted(tube.tension.m_records, key=lambda rec: rec.date)
        pre_tension_rec = None
        try:  # gets the last TensionRecord before the tube was swaged
            generator = (rec for rec in tension_records if rec.date < swage_length_rec.date)
            while True:
                pre_tension_rec = next(generator)
        except StopIteration:
            # we hit this exception after we run out of tension records before swaging,
            # meaning pre_tension record is now the last record before swaging
                return (pre_tension_rec.tension, pre_tension_rec.fail(),pre_tension_rec.date) if pre_tension_rec else None

def get_tension2(tube, min_date):
    """Return the last record of tension, whether pass the test and the ID of the tube after the minimum date for the swaged tube."""
    swage_records = sorted([record for record in tube.swage.m_records if record.date], key=lambda rec: rec.date)
    swage_length_rec = None
    try:  # gets the first SwageRecord with a value for swage_length
        swage_length_rec = next(rec for rec in swage_records if rec.swage_length and rec.date.date() > min_date)
    except StopIteration:
        # tube has no swage length recorded
        pass
    if swage_length_rec:  # only consider the tensions if the tube has been swaged
        # sort tension records by date
        tension_records = sorted(tube.tension.m_records, key=lambda rec: rec.date)
        pre_tension_rec = None
        try:  # gets the last TensionRecord after the tube was swaged
            generator = (rec for rec in tension_records if rec.date > swage_length_rec.date)
            while True:
                pre_tension_rec = next(generator)
        except StopIteration:
            # we hit this exception after we run out of tension records before swaging,
            # meaning pre_tension record is now the last record before swaging
                return (pre_tension_rec.tension, pre_tension_rec.fail()) if pre_tension_rec else None

def get_UMich_tension1(tube, min_date):
    """Return the UM record of tension whether pass the test and the ID of the tube after the minimum date."""
    if str(tube.umich_tension.get_record('last').tension_flag) == "pass":
        status = UMich_Status.PASS
    if str(tube.umich_tension.get_record('last').tension_flag) == "fail":
        status = UMich_Status.FAIL  
    if str(tube.umich_tension.get_record('last').tension_flag) == "N/A":
        status = UMich_Status.UMICH_INCOMPLETE
 
    try:
        #print(tube.umich_tension.get_record('last').umich_tension,str(tube.umich_tension.get_record('last').tension_flag),status)
        return (tube.umich_tension.get_record('last').umich_tension,status,tube.get_ID())
    except (IndexError,TypeError):
        return None

def get_UMich_tension2(tube, min_date):
    """Return the UM record of tension whether pass the test and the ID of the tube after the minimum date."""
    try:
        return (tube.umich_tension.get_record('last').umich_tension + tube.umich_tension.get_record('last').tens_diff,tube.umich_tension.status(),tube.get_ID())
    except (IndexError,TypeError):
        return None

def get_raw_length(tube, min_date):
    swage_records = sorted([record for record in tube.swage.m_records if record.date], key=lambda rec: rec.date)
    try:  # gets the first SwageRecord with a value for raw_length
        raw_length_rec = next(rec for rec in swage_records if rec.raw_length and (rec.date.date()>min_date))
        return (raw_length_rec.raw_length, raw_length_rec.fail(), tube.get_ID())
    except StopIteration:
        pass

def get_swage_length(tube, min_date):
    swage_records = sorted([record for record in tube.swage.m_records if record.date], key=lambda rec: rec.date)
    try:  # gets the first SwageRecord with a value for swage_length
        swage_length_rec = next(rec for rec in swage_records if rec.swage_length and (rec.date.date()>min_date))
        return (swage_length_rec.swage_length, swage_length_rec.fail(), tube.get_ID())
    except StopIteration:
        pass

def get_UMich_length(tube, min_date):
    """
    Return the UM record of tube length, whether pass the 
    test and the ID of the tube after the minimum date.
    """
    try:
        return (tube.umich_misc.get_record('all')[0].length,tube.get_ID())
    except (IndexError,TypeError):
        return None

def get_tension_diffs():
    """
    Return the difference of the post-swaged tension between the first record and last, 
    whether pass the test and the ID of the tube after the minimum date.
    """
    swage_records = sorted([record for record in tube.swage.m_records if record.date], key=lambda rec: rec.date)
    swage_length_rec = None
    try:  # gets the first SwageRecord with a value for swage_length
        swage_length_rec = next(rec for rec in swage_records if rec.swage_length and rec.date.date() > min_date)
    except StopIteration:
        # tube has no swage length recorded
        pass
    if swage_length_rec:  # only consider the tensions if the tube has been swaged
        # sort tension records by date
        tension_records = sorted(tube.tension.m_records, key=lambda rec: rec.date)
        pre_tension_rec = None
        n_record = 0
        try:  # gets the last TensionRecord after the tube was swaged
            generator = (rec for rec in tension_records if rec.date > swage_length_rec.date)
            while True:
                pre_tension_rec = next(generator)
                if n_record == 0:
                    first_pre_tension_tension = pre_tension_rec.tension
                n_record += 1
                
        except StopIteration:
            # we hit this exception after we run out of tension records before swaging,
            # meaning pre_tension record is now the last record before swaging
    
                return (pre_tension_rec.tension-first_pre_tension_tension, pre_tension_rec.fail()) if (pre_tension_rec or n_record > 1) else None



def get_length_diffs(tube, min_date):
    try:
        swage_length, date, _ = get_swage_length(tube, min_date)
        raw_length = get_raw_length(tube, min_date)[0]
        return (swage_length - raw_length, date, tube.get_ID())
    except TypeError:
        return None

def get_tension_diffs(tube, min_date):
    try:
        tension1, status = get_tension1(tube, min_date)[0],get_tension1(tube, min_date)[1]
        tension2 = get_tension2(tube, min_date)[0]
        return (tension2 - tension1, date, tube.get_ID(),status)
    except TypeError:
        return None

def fill_TH2F(TH2F_hists,name,x,y):
    if np.isnan(x) == False and np.isnan(y) == False:
        TH2F_hists[name].Fill(x,y)
        TH2F_hists[name+"_array"][0].append(x)
        TH2F_hists[name+"_array"][1].append(y)
