import logging
import math
import operator
import random
import pandas as pd

import numpy as np

import westpa
from westpa.core.we_driver import WEDriver
from westpa.core.segment import Segment
from westpa.core.states import InitialState

log = logging.getLogger(__name__)

weight_threshold = False
largest_weight = 0.2
smallest_weight = 1E-10
num_resample = 25

class MyFirstDriver(WEDriver):
   
    def _split_by_data(self, bin, to_split, split_into):

        if len(to_split) > 1:
            for segment in to_split:
                bin.remove(segment)
                new_segments_list = self._split_walker(segment, split_into, bin)
                bin.update(new_segments_list)
        else:
            to_split = to_split[0]
            bin.remove(to_split)
            new_segments_list = self._split_walker(to_split, split_into, bin)
            bin.update(new_segments_list)

    def _merge_walkers(self, segments, cumul_weight, bin):
        '''Merge the given ``segments`` in ``bin``, previously sorted by weight, into one conglomerate segment.
        ``cumul_weight`` is the cumulative sum of the weights of the ``segments``; this may be None to calculate here.'''

        if cumul_weight is None:
            cumul_weight = np.add.accumulate([segment.weight for segment in segments])

        glom = Segment(
            n_iter=segments[0].n_iter,  # assumed correct (and equal among all segments)
            weight=cumul_weight[len(segments) - 1],
            status=Segment.SEG_STATUS_PREPARED,
            pcoord=self.system.new_pcoord_array(),
        )

        # Select the history to use
        # The following takes a random number in the interval 0 <= x < glom.weight, then
        # sees where this value falls among the (sorted) weights of the segments being merged;
        # this ensures that a walker with (e.g.) twice the weight of its brethren has twice the
        # probability of having its history selected for continuation
        iparent = np.digitize((random.uniform(0, glom.weight),), cumul_weight)[0]
        gparent_seg = segments[iparent]

        # Inherit history from this segment ("gparent" stands for "glom parent", as opposed to historical
        # parent).
        glom.parent_id = gparent_seg.parent_id
        glom.pcoord[0, :] = gparent_seg.pcoord[0, :]

        # Weight comes from all segments being merged, and therefore all their
        # parent segments
        glom.wtg_parent_ids = set()
        for segment in segments:
            glom.wtg_parent_ids |= segment.wtg_parent_ids

        # The historical parent of gparent is continued; all others are marked as merged
        for segment in segments:
            if segment is gparent_seg:
                # we must ignore initial states here...
                if segment.parent_id >= 0:
                    self._parent_map[segment.parent_id].endpoint_type = Segment.SEG_ENDPOINT_CONTINUES
            else:
                # and "unuse" an initial state here (recall that initial states are in 1:1 correspondence
                # with the segments they initiate), except when a previously-split particle is being
                # merged
                if segment.parent_id >= 0:
                    self._parent_map[segment.parent_id].endpoint_type = Segment.SEG_ENDPOINT_MERGED
                else:
                    if segment.initial_state_id in {segment.initial_state_id for segment in bin}:
                        log.debug('initial state in use by other walker; not removing')
                    else:
                        initial_state = self.used_initial_states.pop(segment.initial_state_id)
                        log.debug('freeing initial state {!r} for future use (merged)'.format(initial_state))
                        self.avail_initial_states[initial_state.state_id] = initial_state
                        initial_state.iter_used = None

        if log.isEnabledFor(logging.DEBUG):
            log.debug('merging ({:d}) {!r} into 1:\n    {!r}'.format(len(segments), segments, glom))

        return glom, iparent


    def _merge_by_data(self, bin, to_merge):

        bin.difference_update(to_merge)
        new_segment, iparent = self._merge_walkers(to_merge, None, bin)
        bin.add(new_segment)
        
        return iparent


    def _run_we(self):
        '''Run recycle/split/merge. Do not call this function directly; instead, use
        populate_initial(), rebin_current(), or construct_next().'''
        self._recycle_walkers()

        # sanity check
        self._check_pre()

        # dummy resampling block
        for bin in self.next_iter_binning:
            if len(bin) == 0:
                continue
            else:
                # this will just get you the final pcoord for each segment... which may not be enough
                segments = np.array(sorted(bin, key=operator.attrgetter('weight')), dtype=np.object_)
                pcoord = np.array(list(map(operator.attrgetter('pcoord'), segments)))[:,:,0]
                weights = np.array(list(map(operator.attrgetter('weight'), segments)))

                nsegs = pcoord.shape[0]
                nframes = pcoord.shape[1]

                pcoord = pcoord.reshape(nsegs,nframes,-1)[:,0]

                # this will allow you to get the pcoords for all frames
                # here we just use it to check if we are initializing
                current_iter_segments = self.current_iter_segments

                curr_segments = np.array(sorted(current_iter_segments, key=operator.attrgetter('weight')), dtype=np.object_)
                curr_pcoord = np.array(list(map(operator.attrgetter('pcoord'), curr_segments)))[:,:,0]
                curr_weights = np.array(list(map(operator.attrgetter('weight'), curr_segments)))

                curr_pcoord = curr_pcoord.reshape(nsegs,nframes)

                # check if not initializing, then split and merge
                init_check = curr_pcoord[:,0] != curr_pcoord[:,-1]
                                                                           
                if np.any(init_check):

                    # change the following for different algorithms
    
                    progress = np.zeros((nsegs), dtype=float)

                    for iseg, segval in enumerate(pcoord):
                        progress[iseg] = 1/np.absolute(0-segval)

                    sorted_progress = np.argsort(-progress,axis=0)
                    to_split_idx = sorted_progress[:num_resample]

                            
                    if not weight_threshold:
                        to_split = np.array([segments[to_split_idx]])[0]
                        self._split_by_data(bin, to_split, 2)
                                                                                      
                        mydf_split = pd.DataFrame()
                        mydf_split['split index'] = to_split_idx
                        mydf_split['pcoord'] = pcoord[to_split_idx]
                        mydf_split['score'] = progress[to_split_idx]
                        mydf_split['weights'] = weights[to_split_idx]
                        print("\n", mydf_split)
                                                                                      
                    # split, trying to preserve weight thresholds
                    #else:
                    #    to_split_idx = top_half[sorted_by_rmsd]
                    #    to_split_weights = weights[to_split_idx]
                    #    num_splits = 0
                    #    for idx, val in enumerate(to_split_idx):
                    #        while num_splits < num_resample:
                    #            w = to_split_weights[idx] 
                    #            for split_into in np.arange(2,num_resample+1)[::-1]:
                    #                wr = w/split_into
                    #                if wr < largest_weight
                                                                                      
                                                                                      
                                                                                      
                    # merge walker with lowest scaled diff into next lowest
                                                                                      
                    if not weight_threshold:
                        bottom_half = sorted_progress[::-1][:int(nsegs/2)]
                        bottom_num = bottom_half[:num_resample*2]
                                                                                      
                        to_merge_idx = []
                        for i in np.arange(1,num_resample*2,2):
                            seg1_idx = bottom_num[i]
                            seg2_idx = bottom_num[i-1]
                            to_merge = [segments[seg1_idx], segments[seg2_idx]] 
                            iparent = self._merge_by_data(bin, to_merge)
                            to_merge_idx.append([seg1_idx, seg2_idx][iparent])
                            
                        mydf_merge = pd.DataFrame()
                        mydf_merge['merge index'] = to_merge_idx
                        mydf_merge['pcoord'] = pcoord[to_merge_idx]
                        mydf_merge['score'] = progress[to_merge_idx]
                        mydf_merge['weights'] = weights[to_merge_idx]
                        print("\n", mydf_merge)
                                                                                      
                    # merge, trying to preserve weight thresholds
                    #else:

        # another sanity check
        self._check_post()

        self.new_weights = self.new_weights or []

        log.debug('used initial states: {!r}'.format(self.used_initial_states))
        log.debug('available initial states: {!r}'.format(self.avail_initial_states))
