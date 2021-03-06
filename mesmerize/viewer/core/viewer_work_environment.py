#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 21:08:09 2018

@author: kushal

Chatzigeorgiou Group
Sars International Centre for Marine Molecular Biology

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

"""

from .mesfile import *
from .data_types import ImgData
import numpy as np
import pickle
import tifffile
import os
from shutil import rmtree
from ...common import get_sys_config, get_proj_config
from uuid import uuid4
from uuid import UUID as UUID_type
import json
from typing import Optional, Tuple


class ViewerWorkEnv:
    def __init__(self, imgdata=None, sample_id='', UUID=None, meta=None, stim_maps=None,
                 roi_manager=None, roi_states=None, comments='', origin_file='',
                 custom_cols = None, history_trace: list = None,
                 additional_data: dict = None,
                 misc: dict = None, **kwargs):
        """
        A class that encapsulates the main work environment objects (img sequence, ROIs, and ROI associated curves) of
        the viewer. Allows for a work environment to be easily spawned from different types of sources and allows for
        a work environment to be easily saved in different ways regardless of the type of original data source.

        :param roi_states:  roi states from ROI Manager module
        :param stim_maps:   {'units': str, 'dataframe': pd.DataFrame}
        :param history_trace: list of dicts containing a traceable history of what what done with the work environment,
                              such as params used from modules to process the data

        :type imgdata:      ImgData
        :type sample_id:    str
        :type UUID:         uuid.UUID
        :type meta:         dict
        :type stim_maps:    dict
        :type comments:     str
        :type cust_col_dict: dict
        :type roi_states:   dict
        :type history_trace: list

        """

        if imgdata is not None:
            self.isEmpty = False  #: Return True if the work environment is empty
            self.imgdata = imgdata
            if isinstance(self.imgdata, ImgData):
                if meta is not None:
                    self.imgdata.meta = meta
        else:
            self.imgdata = ImgData()  #: ImgData instance
            self.isEmpty = True
        self.meta = meta

        if history_trace is None:
            self.history_trace = []  #: history log
        else:
            self.history_trace = history_trace

        self.stim_maps = stim_maps  #: Stimulus maps

        if 'stimMaps' in kwargs.keys():
            self.stim_maps = kwargs['stimMaps']

        self.sample_id = sample_id  #: SampleID, if opened from a project Sample

        self.roi_manager = roi_manager  #: reference to the back-end ROI Manager that is currently in use

        self.changed_items = []
        self.roi_states = roi_states
        self.comments = comments
        self.origin_file = origin_file

        if custom_cols is None:
            self.custom_cols = {}

        if additional_data is not None:
            assert isinstance(additional_data, dict)
            self.additional_data = additional_data
        else:
            self.additional_data = {}

        if misc is not None:
            assert isinstance(misc, dict)
            self.misc = misc
        else:
            self.misc = {}

        self._UUID = UUID  #: UUID, if opened from a project Sample refers to the ImgUUID

        self._saved = True

    # def get_imgdata(self):
    #     return self.imgdata
    #
    # def get_seq(self):
    #     return self.imgdata.seq
    #
    # def get_meta(self):
    #     return self.meta
    #
    # def get_roi_manager(self):
    #     return self.roi_manager

    @property
    def UUID(self) -> UUID_type:
        if self._UUID is None:
            raise ValueError('UUID is not set. UUID can only be set at instantiation')
        if not isinstance(self._UUID, UUID_type):
            raise TypeError('UUID is not of type uuid.UUID. Something went wrong. You should not modify the UUID')
        return self._UUID

    def clear(self):
        """Cleanup of the work environment"""
        self.isEmpty = True
        del self.imgdata.seq
        self.imgdata = None
        if self.roi_manager is not None:
            self.roi_manager.clear()
            # self.roi_manager.parent.start_manual_mode()
        self.roi_states = None
        self.comments = ''
        self.origin_file = ''
        self._saved = True
        self.changed_items = []
        print('Work environment dumped!')

    def restore_rois_from_states(self):
        if (self.roi_manager is not None) and (self.roi_states is not None):
            self.roi_manager.parent.set_all_from_states(self.roi_states)

    @classmethod
    def from_pickle(cls, pickle_file_path: str, tiff_path: str = None):
        """
        Get pickled image data from a pickle file & image sequence from a npz or tiff. Used after motion correction
        & to view a sample from a project DataFrame. Create ImgData class object (See MesmerizeCore.DataTypes) and
        return instance of the work environment.

        :param: pickle_file_path:   full path to the pickle containing image metadata, stim maps, and roi_states
        :param: tiff_path:          str of the full path to a tiff file containing the image sequence
        """

        if tiff_path is not None:
            # seq = tifffile.imread(tiff_path)
            tif = tifffile.TiffFile(tiff_path, is_nih=True)
            seq = tif.asarray(maxworkers=int(get_sys_config()['_MESMERIZE_N_THREADS']))
            seq = seq.T
        else:
            seq = None

        p = pickle.load(open(pickle_file_path, 'rb'))

        # compatibility for older pickle files from older mesmerize
        if 'imdata' in p.keys():
            try:
                sample_id = p['imdata']['sample_id']
            except KeyError:
                sample_id = p['imdata']['SampleID']

            imdata = ImgData(seq, p['imdata']['meta'])

            comments = p['imdata']['comments']

            roi_states = []
            if 'roi_states' in p['imdata']:
                for ID in range(0, len(p['imdata']['roi_states'])):
                    roi_states.append(p['imdata']['roi_states'][ID])

            return cls(imdata, roi_states=roi_states, comments=comments, sample_id=sample_id)
        else:
            # Use with output of new to_pickle() method
            img_data = ImgData(seq)
            return cls(img_data, **p)

    @property
    def saved(self):
        return bool(self._saved)

    @saved.setter
    def saved(self, state: bool):
        self._saved = state
        if state is True:
            self.changed_items = []

    @staticmethod
    def load_mesfile(path: str) -> MES:
        """
        Just passes the path of a .mes file to the constructor of class MES in MesmerizeCore.FileInput.
        Loads .mes file & constructs MES obj from which individual images & their respective metadata can be loaded
        to construct viewer work environments using the classmethod viewerWorkEnv.from_mesfile.

        :param path: full path to a single .mes file.
        """
        return MES(path)

    @staticmethod
    def _organize_meta(meta: dict, origin: str) -> dict:
        """
        Organize input meta data dict into a uniform structure
        :param meta:    meta data dict, origin from a json file for example
        :param origin:  name of the origin source of the meta data, such a program or microscope etc.
        :return:        dict organized with keys that are used throughout Mesmerize.
        """

        if origin == 'mes':
            fps = float(1000/meta['FoldedFrameInfo']['frameTimeLength'])

            date_meta = meta['MeasurementDate'].split('.')
            ymd = date_meta[0] + date_meta[1] + date_meta[2]
            hms_ = date_meta[3].split(':')
            hms = hms_[0].split(' ')[1] + hms_[1] + hms_[2][:2]
            date = ymd + '_' + hms

            vmin = meta['LUTstruct']['lower']
            vmax = meta['LUTstruct']['upper']

            meta_d = {'origin':    origin,
                      'fps':       fps,
                      'date':      date,
                      'vmin':      vmin,
                      'vmax':      vmax,
                      'orig_meta': meta}

            return meta_d

        elif origin == 'AwesomeImager' or origin == 'DeepEyes':
            meta_d = {'origin':     origin,
                      'version':    meta['version'],
                      'fps':        meta['framerate'],
                      'date':       meta['date'] + '_' + meta['time'],
                      'vmin':       meta['level_min'],
                      'vmax':       meta['level_max'],
                      'orig_meta':  meta}
            return meta_d

        else:
            required = ['fps', 'date']

            if not all(k in meta.keys() for k in required):
                raise KeyError(f'Meta data dict must contain all mandatory fields: {required}')

            meta_d = {'origin': origin,
                      'fps':    meta['fps'],
                      'date':   meta['date']}

            if 'orig_meta' in meta.keys():
                meta_d.update({'orig_meta': meta['orig_meta']})

            return meta_d

    @classmethod
    def from_mesfile(cls, mesfile_object: MES, img_reference: str):
        """
        Return instance of work environment with MesmerizeCore.ImgData class object using seq returned from
        MES.load_img from MesmerizeCore.FileInput module and any stimulus map that the user may have specified.

        :param mesfile_object: MES object, created from .mes file
        :param img_reference: image reference to load, see :meth:`mesmerize.viewer.core.mesfile.MES.get_image_references`
        """

        imgseq, raw_meta = mesfile_object.load_img(img_reference)

        meta_data = ViewerWorkEnv._organize_meta(raw_meta, 'mes')
        imdata = ImgData(imgseq, meta_data)
        # imdata.stimMaps = (mesfileMaps, 'mesfile')

        return cls(imdata, meta=meta_data)

    @classmethod
    def from_tiff(cls, path: str, method: str, meta_path: Optional[str] = ''):
        """
        Return instance of work environment with ImgData.seq set from the tiff file.

        :param path:        path to the tiff file
        :param method:      one of 'imread', 'asarray', or 'asarray-multi'. Refers to usage of either tifffile.imread
                            or tifffile.asarray. 'asarray-multi' will load multi-page tiff files.
        :param meta_path:   path to a json file containing meta data
        """

        if method == 'imread':
            seq = tifffile.imread(path)

        elif method == 'asarray':
            tif = tifffile.TiffFile(path, is_nih=True)
            seq = tif.asarray(maxworkers=int(get_sys_config()['_MESMERIZE_N_THREADS']))

        elif method == 'asarray-multi':
            tif = tifffile.TiffFile(path, is_nih=True)

            seq = tif.asarray(key=range(0, len(tif.series)),
                              maxworkers=int(get_sys_config()['_MESMERIZE_N_THREADS']))
        else:
            raise ValueError("Must specify 'imread' or 'asarray' in method argument")

        if meta_path.endswith('.json'):
            jmd = json.load(open(meta_path, 'r'))
            if 'source' not in jmd.keys():
                raise KeyError('Invalid meta data file. Json meta data file must have a "source" entry.')
            else:
                meta = ViewerWorkEnv._organize_meta(meta=jmd, origin=jmd['source'])
        else:
            meta = None

        imdata = ImgData(seq.T, meta)
        return cls(imdata)

    @classmethod
    def from_splits(cls):
        pass

    def _make_dict(self) -> dict:
        # Dict that's later used for pickling
        d = {'sample_id':   self.sample_id,
             'meta':        self.imgdata.meta,
             'stim_maps':   self.stim_maps,
             'comments':    self.comments,
             'history_trace': self.history_trace,
             'additional_data': self.additional_data
             }

        if self.roi_manager is not None:
            if not self.roi_manager.is_empty():
                rois = self.roi_manager.get_all_states()

                for ix in range(len(rois['states'])):
                    for roi_def in rois['states'][ix]['tags'].keys():
                        if rois['states'][ix]['tags'][roi_def] == '':
                            rois['states'][ix]['tags'][roi_def] = 'untagged'

                d['roi_states'] = rois

        return d


    def _prepare_export(self, dir_path: str, filename: Optional[str] = None, save_img_seq: bool = True, UUID: Optional[UUID_type] = None) -> Tuple[str, dict]:
        if UUID is None:
            UUID = uuid4()

        if filename is None:
            filename = os.path.join(dir_path, f'{self.sample_id}-_-{UUID}')
        else:
            filename = os.path.join(dir_path, filename)

        work_env = self._make_dict()

        data = {**work_env, 'UUID': UUID}

        if save_img_seq:
            tifffile.imsave(f'{filename}.tiff', self.imgdata.seq.T, bigtiff=True)

        return (filename, data)

    def to_pickle(self, dir_path: str, filename: Optional[str] = None, save_img_seq=True, UUID=None) -> str:
        """
        Package the current work Env ImgData class object (See MesmerizeCore.DataTypes) and any paramteres such as
        for motion correction and package them into a pickle & image seq array. Used for batch motion correction and
        for saving current sample to the project. Image sequence is saved as a tiff and other information about the
        image is saved in a pickle.
        """
        filename, data = self._prepare_export(dir_path, filename, save_img_seq, UUID)

        pickle.dump(data, open(f'{filename}.pik', 'wb'), protocol=4)

        self.saved = True

        return filename

    def to_pandas(self, proj_path: str, modify_options: Optional[dict] = None) -> list:
        """
        Used for saving the work environment as a project Sample.

        :param      proj_path:      Root path of the current project
        :param      modify_options:
        :return:    list of dicts that each correspond to a single curve that can be appended
                    as rows to the project dataframe
        """
        if self.isEmpty:
            raise ValueError('Work environment is empty')

        save_img_seq = True

        # Path where image (as tiff file) and image metadata, roi_states, and stimulus maps (in a pickle) are stored
        imgdir = os.path.join(proj_path, 'images')  # + self.imgdata.SampleID + '_' + str(time.time())

        if (modify_options is dict) and (self._UUID is None):
            raise ValueError('Error overwriting Sample. Current Work Environment does not have a UUID.\n'
                             'Samples always have a UUID, something went wrong. Reload the sample from the project.')

        if self._UUID is None:
            UUID = uuid4()
        else:
            UUID = self.UUID
        curves_dir = os.path.join(proj_path, 'curves', f'{self.sample_id}-_-{str(UUID)}')

        if modify_options is not None:
            rmtree(curves_dir)
            if modify_options['overwrite_img_seq']:
                save_img_seq = True
            else:
                save_img_seq = False

        img_path = self.to_pickle(imgdir, UUID=UUID, save_img_seq=save_img_seq)

        if save_img_seq:
            max_proj = np.amax(self.imgdata.seq, axis=2)
            max_proj_path = img_path + '_max_proj.tiff'
            tifffile.imsave(max_proj_path, max_proj)

            std_proj = self.imgdata.seq.std(axis=2)
            std_proj_path = img_path + '_std_proj.tiff'
            tifffile.imsave(std_proj_path, std_proj)

        # Since viewerWorkEnv.to_pickle sets the saved property to True, and we're not done saving the dict yet.
        self._saved = False

        # Create a dict that contains all stim definitions as keys that refer to a list of all the stims for that sample
        stimuli_unique_sets = {}
        # This list is just used for gathering all new stims to add to the config file. This is just used for
        # populating the comboBoxes in the stimMapWidget GUI so that the widget doesn't need to access the DataFrame
        # for this simple task.
        # new_stimuli = []
        if self.stim_maps is None:
            for stim_def in get_proj_config().options('STIM_DEFS'):
                stimuli_unique_sets[stim_def] = ['untagged']
        else:
            for stim_def in self.stim_maps.keys():
                stimuli = []

                if self.stim_maps[stim_def] is None:
                    stimuli_unique_sets[stim_def] = ['untagged']
                    continue

                stimuli += list(self.stim_maps[stim_def]['name'].values)

                stimuli_unique_sets[stim_def] = list(set(stimuli))

                # for stim in stimuli_unique_sets[stim_def]:
                #     if stim not in get_proj_config()['ALL_STIMS'].keys():
                        # new_stimuli.append(stim)

        # get_proj_config()['ALL_STIMS'] = {**get_proj_config()['ALL_STIMS'], **dict.fromkeys(new_stimuli)}
        # configuration.save_proj_config()

        if self.imgdata.meta is not None:
            try:
                date = str(self.imgdata.meta['date'])
            except KeyError:
                date = 'unknown'
        else:
            date = 'unknown'

        if self.comments is None or self.comments == '':
            comments = 'untagged'
        else:
            comments = self.comments

        if os.path.isdir(curves_dir) is False:
            os.mkdir(curves_dir)

        dicts = []

        rois = self.roi_manager.get_all_states()

        for ix in range(len(rois['states'])):
            curve_data = rois['states'][ix]['curve_data']

            for roi_def in rois['states'][ix]['tags'].keys():
                if rois['states'][ix]['tags'][roi_def] == '':
                    rois['states'][ix]['tags'][roi_def] = 'untagged'

            roi_tags = rois['states'][ix]['tags']
            curve_path = os.path.join(curves_dir, str(ix).zfill(5) + '.npz')

            np.savez(curve_path, curve=curve_data)#, stimMaps=self.imgdata.stimMaps)

            # if rois['states'][ix]['roi_type'] == 'ManualROI':
            #     roi_state = {'type': 'ManualROI',
            #                  'graphics_object': rois['states'][ix]['roi_graphics_object_state'],
            #                  'shape': rois['states'][ix]['shape']
            #                  }
            # elif rois['states'][ix]['roi_type'] == 'CNMFROI':
            #     roi_state = {'type': 'CNMFROI',
            #                  'roi_xs': rois['states'][ix]['roi_xs'],
            #                  'roi_ys': rois['states'][ix]['roi_ys']
            #                  }

            d = {'SampleID': self.sample_id,
                 'CurvePath': os.path.relpath(curve_path, proj_path),
                 'ImgUUID': str(UUID),
                 'ImgPath': os.path.relpath(f'{img_path}.tiff', proj_path),
                 'ImgInfoPath': os.path.relpath(f'{img_path}.pik', proj_path),
                 'ROI_State': rois['states'][ix],
                 'date': date,
                 'uuid_curve': str(uuid4()),
                 'comments': comments,
                 'misc': self.misc
                 }

            dicts.append({**d,
                          **self.custom_cols,
                          **stimuli_unique_sets,
                          **roi_tags})

        # for ix in range(0, len(self.CurvesList)):
        #     curvePath = curvesDir + '/CURVE_' + str(ix).zfill(3) + '.npz'
        #
        #     if self.rois['origin'] == 'manual':
        #         if isinstance(self.CurvesList[ix], np.ndarray):
        #             curve = self.CurvesList[ix]
        #         else:
        #             curve = self.CurvesList[ix].getData()
        #
        #         np.savez(curvePath, curve=curve,
        #                  roi_state=self.ROIList[ix].saveState(), stimMaps=self.imgdata.stimMaps)
        #
        #     elif self.rois['origin'] == 'CNMFE':
        #         pass
        #
        #     d = {'SampleID':    self.sample_id,
        #          'CurvePath':   curvePath.split(proj_path)[1],
        #          'ImgPath':     img_path.split(proj_path)[1] + '.tiff',
        #          'ImgInfoPath': img_path.split(proj_path)[1] + '.pik',
        #          }
        #
        #     # Final list of dicts that are each appended as rows to the project DataFrame
        #     dicts.append({**d,
        #                   **self.custom_columns_dict,
        #                   **stimMapsSet,
        #                   **self.ROIList[ix].tags,
        #                   'Date':       date,
        #                   'uuid_curve': UUID,
        #                   'comments':   comments
        #                   })

        self.saved = True
        return dicts
