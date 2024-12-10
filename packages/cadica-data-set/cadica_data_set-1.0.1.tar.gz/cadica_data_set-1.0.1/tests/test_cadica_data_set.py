import pytest
from cadica_data_set.cadica_data_set import *
from .cadica_test_data import *

VALID_CADICA_TEST_DATA_ROOT_PATH = "/Users/abhaycuram/Desktop/ML Projects/Jeremy Fast AI/Python Scripts/cadica_data_set/tests/resources/valid_cadica_test_data_set"
INVALID_CADICA_TEST_DATA_ROOT_PATH = "/Users/abhaycuram/Desktop/ML Projects/Jeremy Fast AI/Python Scripts/cadica_data_set/tests/valid_cadica_test_data_set"
INVALID_CADICA_TEST_DATA_MISSING_SELECTED_VIDEOS_ROOT_PATH = "/Users/abhaycuram/Desktop/ML Projects/Jeremy Fast AI/Python Scripts/cadica_data_set/tests/resources/invalid_cadica_test_data_set_missing_selected_videos"
INVALID_CADICA_TEST_DATA_MISSING_PATIENT_DATA_ROOT_PATH = "/Users/abhaycuram/Desktop/ML Projects/Jeremy Fast AI/Python Scripts/cadica_data_set/tests/resources/invalid_cadica_test_data_set_missing_patient_data"
INVALID_CADICA_TEST_DATA_MISSING_NONLESION_VIDEOS_TXT_ROOT_PATH = "/Users/abhaycuram/Desktop/ML Projects/Jeremy Fast AI/Python Scripts/cadica_data_set/tests/resources/invalid_cadica_test_data_set_missing_nonlesion_videos_txt"
INVALID_CADICA_TEST_DATA_MISSING_LESION_VIDEOS_TXT_ROOT_PATH = "/Users/abhaycuram/Desktop/ML Projects/Jeremy Fast AI/Python Scripts/cadica_data_set/tests/resources/invalid_cadica_test_data_set_missing_lesion_videos_txt"
INVALID_CADICA_TEST_DATA_MISSING_SELECTED_FRAMES_TXT_ROOT_PATH = "/Users/abhaycuram/Desktop/ML Projects/Jeremy Fast AI/Python Scripts/cadica_data_set/tests/resources/invalid_cadica_test_data_set_missing_selected_frames_txt"
INVALID_CADICA_TEST_DATA_MISSING_VIDEO_DIRS_ROOT_PATH = "/Users/abhaycuram/Desktop/ML Projects/Jeremy Fast AI/Python Scripts/cadica_data_set/tests/resources/invalid_cadica_test_data_set_missing_video_dirs"

# Positive Unit Test Cases
def test_load_method_indexes_valid_data_set_correctly():
    cadica_data_set = CadicaDataSet(VALID_CADICA_TEST_DATA_ROOT_PATH)
    cadica_data_set.load()
    assert cadica_data_set.lesioned_image_paths_dict == CadicaTestData.lesioned_image_paths_dict, "load() API failed, Paths to lesioned images from the data set were not read correctly"
    assert cadica_data_set.nonlesioned_image_paths_dict == CadicaTestData.nonlesioned_image_paths_dict, "load() API failed, Paths to nonlesioned images from the data set were not read correctly"
    assert cadica_data_set.lesioned_images_set == CadicaTestData.lesioned_images_set, "load() API failed, Paths to lesioned images from the data set were not read correctly"
    assert cadica_data_set.nonlesioned_images_set == CadicaTestData.nonlesioned_images_set, "load() API failed, Paths to nonlesioned images from the data set were not read correctly"

def test_is_leison_is_nonlesion_label_methods_work_correctly():
    cadica_data_set = CadicaDataSet(VALID_CADICA_TEST_DATA_ROOT_PATH)
    cadica_data_set.load()
    lesioned_image_path = "/Users/abhaycuram/Desktop/ML Projects/Jeremy Fast AI/Python Scripts/cadica_data_set/tests/resources/valid_cadica_test_data_set/selectedVideos/p14/v1/input/p14_v1_00011.png"
    nonlesioned_image_path = "/Users/abhaycuram/Desktop/ML Projects/Jeremy Fast AI/Python Scripts/cadica_data_set/tests/resources/valid_cadica_test_data_set/selectedVideos/p4/v1/input/p4_v1_00009.png"
    assert cadica_data_set.is_lesioned_image(lesioned_image_path) == True
    assert cadica_data_set.is_nonlesioned_image(lesioned_image_path) == False
    assert cadica_data_set.is_lesioned_image(nonlesioned_image_path) == False
    assert cadica_data_set.is_nonlesioned_image(nonlesioned_image_path) == True

def test_get_training_data_returns_correct_image_paths_count_for_sampling_policy_none():
    cadica_data_set = CadicaDataSet(VALID_CADICA_TEST_DATA_ROOT_PATH)
    cadica_data_set.load()
    input_image_paths = cadica_data_set.get_training_data_image_paths(CadicaDataSetSamplingPolicy.NONE)
    assert len(input_image_paths) == 43, "get_training_data_image_paths() API failed for CadicaDataSetSamplingPolicy.NONE, all image paths should have been returned"

def test_get_training_data_returns_correct_image_paths_count_for_sampling_policy_balanced():
    cadica_data_set = CadicaDataSet(VALID_CADICA_TEST_DATA_ROOT_PATH)
    cadica_data_set.load()
    input_image_paths = cadica_data_set.get_training_data_image_paths(CadicaDataSetSamplingPolicy.BALANCED_SAMPLING)
    assert len(input_image_paths) < 43, "get_training_data_image_paths() API failed for CadicaDataSetSamplingPolicy.BALANCED_SAMPLING, expected number of image paths were not returned."


# Negative Unit Test Cases
def test_cadica_data_set_creation_raises_exception_for_invalid_root_path():
    with pytest.raises(FileNotFoundError) as exception_info:
        cadica_data_set = CadicaDataSet(INVALID_CADICA_TEST_DATA_ROOT_PATH)
    assert str(exception_info.value) == "The root path to your cadica data set directory was not found. Please supply a valid path."

def test_load_method_raises_exception_for_missing_selected_videos_dir():
    with pytest.raises(FileNotFoundError) as exception_info:
        cadica_data_set = CadicaDataSet(INVALID_CADICA_TEST_DATA_MISSING_SELECTED_VIDEOS_ROOT_PATH)
        cadica_data_set.load()
    assert str(exception_info.value) == "The selectedVideos/ directory was not found. Please ensure you did not modify the original cadica data set file structure."

def test_load_method_raises_exception_for_missing_lesion_videos_txt():
    with pytest.raises(FileNotFoundError) as exception_info:
        cadica_data_set = CadicaDataSet(INVALID_CADICA_TEST_DATA_MISSING_LESION_VIDEOS_TXT_ROOT_PATH)
        cadica_data_set.load()
    assert str(exception_info.value) == "lesionVideos.txt and nonLesionVideos.txt files were not found. Please ensure you did not modify the original cadica data set file structure."

def test_load_method_raises_exception_for_missing_non_lesion_videos_txt():
    with pytest.raises(FileNotFoundError) as exception_info:
        cadica_data_set = CadicaDataSet(INVALID_CADICA_TEST_DATA_MISSING_NONLESION_VIDEOS_TXT_ROOT_PATH)
        cadica_data_set.load()
    assert str(exception_info.value) == "lesionVideos.txt and nonLesionVideos.txt files were not found. Please ensure you did not modify the original cadica data set file structure."

def test_load_method_raises_exception_for_missing_selected_frames_txt():
    with pytest.raises(FileNotFoundError) as exception_info:
        cadica_data_set = CadicaDataSet(INVALID_CADICA_TEST_DATA_MISSING_SELECTED_FRAMES_TXT_ROOT_PATH)
        cadica_data_set.load()
    assert str(exception_info.value) == "A selected image frame definition file was not found. Please ensure you did not modify the original cadica data set file structure."

def test_load_method_indexes_correctly_for_missing_patient_data():
    cadica_data_set = CadicaDataSet(INVALID_CADICA_TEST_DATA_MISSING_PATIENT_DATA_ROOT_PATH)
    cadica_data_set.load()
    assert len(cadica_data_set.lesioned_image_paths_dict) == 0, "load() API failed, no image paths should be indexed because there is NO patient data."
    assert len(cadica_data_set.nonlesioned_image_paths_dict) == 0, "load() API failed, no image paths should be indexed because there is NO patient data."
    assert len(cadica_data_set.lesioned_images_set) == 0, "load() API failed, no image paths should be indexed because there is NO patient data."
    assert len(cadica_data_set.nonlesioned_images_set) == 0, "load() API failed, no image paths should be indexed because there is NO patient data."

def test_load_method_raises_exception_for_missing_video_data():
    with pytest.raises(FileNotFoundError) as exception_info:
        cadica_data_set = CadicaDataSet(INVALID_CADICA_TEST_DATA_MISSING_VIDEO_DIRS_ROOT_PATH)
        cadica_data_set.load()
    assert str(exception_info.value) == "The video directories containing labeled images for each patient weren't found. Please ensure you did not modify the original cadica data set file structure."