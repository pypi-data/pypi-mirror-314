class CadicaDataSetError:
    @staticmethod
    def root_dir_not_found():
        return FileNotFoundError("The root path to your cadica data set directory was not found. Please supply a valid path.")
    
    @staticmethod
    def selected_videos_dir_not_found():
        return FileNotFoundError("The selectedVideos/ directory was not found. Please ensure you did not modify the original cadica data set file structure.")
    
    @staticmethod 
    def videos_txt_files_not_found():
        raise FileNotFoundError("lesionVideos.txt and nonLesionVideos.txt files were not found. Please ensure you did not modify the original cadica data set file structure.")
    
    @staticmethod 
    def selected_frames_txt_file_not_found():
        raise FileNotFoundError("A selected image frame definition file was not found. Please ensure you did not modify the original cadica data set file structure.")
    
    @staticmethod
    def video_dirs_not_found():
        return FileNotFoundError("The video directories containing labeled images for each patient weren't found. Please ensure you did not modify the original cadica data set file structure.")
    
    @staticmethod
    def patient_dirs_not_found():
        return FileNotFoundError("The patient directories containing selected videos and labeled images for each patient weren't found. Please ensure you did not modify the original cadica data set file structure.")