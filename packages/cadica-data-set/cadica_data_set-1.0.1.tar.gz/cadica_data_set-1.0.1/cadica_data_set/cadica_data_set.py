from .cadica_constants import*
from .cadica_errors import*
import os
from enum import Enum
from itertools import chain

class CadicaDataSetSamplingPolicy(Enum):
    """
    Represents the sampling policy to use when returning the training data.
    
    Attributes
    ----------
    NONE : int
        Applies no sampling policy. This will return all labeled lesion/nonlesion images 
        regardless of the class distribution.
    BALANCED_SAMPLING : int
        Tries to "evenly" sample images to return a 50/50 distribution across lesion/nonlesioned images.
        Use this policy if you don't want your model to "overfit" towards lesioned images or nonlesioned images.
        The CADICA data set has more lesioned images than nonlesioned images. The sampling happens at the "video level."
    """
    NONE = 1
    BALANCED_SAMPLING = 2

class CadicaDataSet:
    """
    Object that indexes the CADICA data set into labeled lesioned/nonlesioned images.
    This object can be used as the "data source" for "labeled" lesioned/nonlesioned image input data
    during image model training or image model finetuning. Useful if building a binary classifier for 
    hear CT scan images that want to be classified along lesion/nonlesion lines (CAD detection).
    """

    #region Initialization
    def __init__(self, path):
        """
        Initializes a CadicaDataSet instance.

        Parameters
        ----------
        path : str 
            The absolute path to the CADICA data set folder on your file system
        """
        if os.path.isdir(path):
            self.base_path = path
            self.lesioned_image_paths_dict = {}
            self.nonlesioned_image_paths_dict = {}
            self.lesioned_images_set = set()
            self.nonlesioned_images_set = set()
        else:
            raise CadicaDataSetError.root_dir_not_found() 
    #endregion

    #region Core Public Methods
    def load(self):
        """
        Loads and indexes the CADICA data set into memory from the path supplied
        in the initializer synchronously. This API reads the CADICA data set folder and indexes all
        selected lesioned and nonlesioned images for easy training data generation and
        generation of "labels." This API must be called before the get_training_data_image_paths(),
        is_lesioned_image(), and is_nonlesioned_image() API's are invoked. 
        """
        if os.path.isdir(self.base_path):
            selectedVideosPath = os.path.join(self.base_path, CadicaConstants.VIDEOS_DIR)
            if os.path.isdir(selectedVideosPath):
                patient_dir_paths = list(map(lambda dir: os.path.join(selectedVideosPath, dir), filter(lambda dir: not dir.startswith('.'), os.listdir(selectedVideosPath))))
                for patient_dir_path in patient_dir_paths:
                    if os.path.isdir(patient_dir_path):
                        lesion_videos_txt_file_path = os.path.join(patient_dir_path, CadicaConstants.LESION_VIDEOS_TXT)
                        non_lesion_videos_txt_file_path = os.path.join(patient_dir_path, CadicaConstants.NONLESION_VIDEOS_TXT)
                        if os.path.isfile(lesion_videos_txt_file_path) and os.path.isfile(non_lesion_videos_txt_file_path):
                            lesion_video_dirs = self._read_cadica_txt_file(lesion_videos_txt_file_path)
                            nonlesion_video_dirs = self._read_cadica_txt_file(non_lesion_videos_txt_file_path)
                            lesion_video_dir_paths = list(map(lambda dir: os.path.join(patient_dir_path, dir), lesion_video_dirs))
                            nonlesion_video_dir_paths = list(map(lambda dir: os.path.join(patient_dir_path, dir), nonlesion_video_dirs))
                            if lesion_video_dir_paths:
                                for lesion_video_dir_path in lesion_video_dir_paths:
                                    if os.path.isdir(lesion_video_dir_path):
                                        path_components = (lesion_video_dir_path.strip(os.sep)).split(os.sep)
                                        video_dir = path_components[-1]
                                        patient_dir = path_components[-2]
                                        selected_image_frame_file_paths = self._get_selected_image_frame_file_paths(patient_dir, video_dir, lesion_video_dir_path)
                                        image_paths_key = os.path.join(patient_dir, video_dir)
                                        self.lesioned_image_paths_dict[image_paths_key] = selected_image_frame_file_paths
                                        self.lesioned_images_set.update(selected_image_frame_file_paths)
                                    else:
                                        raise CadicaDataSetError.video_dirs_not_found()
                            if nonlesion_video_dir_paths:
                                for nonlesion_video_dir_path in nonlesion_video_dir_paths:
                                    if os.path.isdir(nonlesion_video_dir_path):
                                        path_components = (nonlesion_video_dir_path.strip(os.sep)).split(os.sep)
                                        video_dir = path_components[-1]
                                        patient_dir = path_components[-2]
                                        selected_image_frame_file_paths = self._get_selected_image_frame_file_paths(patient_dir, video_dir, nonlesion_video_dir_path)
                                        image_paths_key = os.path.join(patient_dir, video_dir)
                                        self.nonlesioned_image_paths_dict[image_paths_key] = selected_image_frame_file_paths
                                        self.nonlesioned_images_set.update(selected_image_frame_file_paths)
                                    else:
                                        raise CadicaDataSetError.video_dirs_not_found()
                        else:
                            raise CadicaDataSetError.videos_txt_files_not_found()
                    else:
                        raise CadicaDataSetError.patient_dirs_not_found()
            else:
                raise CadicaDataSetError.selected_videos_dir_not_found()
        else:
            raise CadicaDataSetError.root_dir_not_found()
    
    def get_training_data_image_paths(self, sampling_policy: CadicaDataSetSamplingPolicy):
        """
        Returns training data as an array of image paths to all "lesioned" and "nonlesioned"
        labeled images in the CADICA data set. This can be used as the training data and validation data
        to train a image model based on these labels. You must provide a sampling_policy and invoke the 
        load() API before calling this method.   
        
        Parameters
        ----------
        sampling_policy : CadicaDataSetSamplingPolicy 
            A sampling policy to use when generating the training data. 
        """
        image_paths = []
        lesioned_image_paths = list(chain.from_iterable(list(self.lesioned_image_paths_dict.values())))
        nonlesioned_image_paths = list(chain.from_iterable(list(self.nonlesioned_image_paths_dict.values())))
        if sampling_policy == CadicaDataSetSamplingPolicy.NONE:
            image_paths.extend(list(lesioned_image_paths))
            image_paths.extend(list(nonlesioned_image_paths))
        elif sampling_policy == CadicaDataSetSamplingPolicy.BALANCED_SAMPLING:
            max_image_count = min(len(lesioned_image_paths), len(nonlesioned_image_paths))
            self._update_image_paths_for_balanced_sampling(image_paths, max_image_count, self.nonlesioned_image_paths_dict)
            self._update_image_paths_for_balanced_sampling(image_paths, max_image_count, self.lesioned_image_paths_dict)
        return image_paths
    
    def is_lesioned_image(self, image_path):
        """
        Returns True if the image_path is classified as a "lesioned" image in the CADICA data set.
        This can be used as a usefel "labeling" func during image model training if needed.   
        
        Parameters
        ----------
        image_path: The path to the image to "label" 
        """
        return image_path in self.lesioned_images_set

    def is_nonlesioned_image(self, image_path):
        """
        Returns True if the image_path is classified as a "nonlesioned" image in the CADICA data set.
        This can be used as a usefel "labeling" func during image model training if needed.   
        
        Parameters
        ----------
        image_path: The path to the image to "label" 
        """
        return image_path in self.nonlesioned_images_set
    #endregion

    #region Private Helpers
    def _get_selected_image_frame_file_paths(self, patient_dir, video_dir, cur_path):        
        selected_frames_txt_file_name = "_".join([patient_dir, video_dir, CadicaConstants.SELECTED_FRAMES_TXT])
        selected_frames_txt_file_path = os.path.join(cur_path, selected_frames_txt_file_name)
        if os.path.isfile(selected_frames_txt_file_path):
            selected_image_frames = self._read_cadica_txt_file(selected_frames_txt_file_path)
            selected_image_frame_file_names = list(map(lambda image_frame: image_frame + CadicaConstants.PNG_EXT, selected_image_frames))
            return list(map(lambda image_frame_file_name: os.path.join(cur_path, CadicaConstants.INPUT_DIR, image_frame_file_name), selected_image_frame_file_names))
        else:
            raise CadicaDataSetError.selected_frames_txt_file_not_found()

    def _read_cadica_txt_file(self, file):
        lines = []
        f = open(file, "r")
        for line in f:
            sanitized_line = line.strip()
            lines.append(sanitized_line)
        f.close()
        return lines
    
    def _update_image_paths_for_balanced_sampling(self, image_paths, max_count, image_paths_dict):
        local_count = 0
        for image_path_key in image_paths_dict:
            if local_count >= max_count:
                break
            else:
                cur_image_paths = image_paths_dict[image_path_key]
                image_paths.extend(cur_image_paths)
                local_count += len(cur_image_paths)
    #endregion







