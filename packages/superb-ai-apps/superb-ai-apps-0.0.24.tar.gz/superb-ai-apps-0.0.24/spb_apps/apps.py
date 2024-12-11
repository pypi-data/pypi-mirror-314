import logging
from abc import ABC, abstractmethod


class SuperbApps(ABC):
    """
    This abstract class defines the interface for interactions with Superb applications, specifically the Label and Curate platforms.
    It outlines methods for downloading images, uploading images and annotations, retrieving image dimensions, and creating bounding box annotations.
    The specifics of these operations depend on the platform in use.
    """

    def __init__(
        self,
        team_name: str,
        access_key: str,
    ):
        """
        Initializes the SuperbApps instance with the team name and access key, setting up the necessary authentication for platform interaction.

        Parameters:
            team_name (str): The name of the team using the platform.
            access_key (str): The access key for platform authentication.
        """
        self.team_name = team_name
        self.access_key = access_key

    @abstractmethod
    def download_image(self):
        """
        Abstract method to download an image using its unique identifier. The implementation of this method should handle the specifics of downloading
        from the designated platform.

        Parameters:
            data_key (str): The unique identifier for the image.
            path (str, optional): The local file path to save the downloaded image. Defaults to None.
        """
        pass

    @abstractmethod
    def get_width_height(self):
        """
        Abstract method to retrieve the width and height of an image. The implementation should specify how these dimensions are obtained
        from the designated platform.

        Parameters:
            data_handler (spb_label.DataHandle, optional): The data handler object for the 'label' platform. Defaults to None.
            data_key (str, optional): The unique identifier for the image for the 'curate' platform. Defaults to "".

        Returns:
            Tuple[int, int]: A tuple containing the width and height of the image.
        """
        pass

    @abstractmethod
    def make_bbox_annotation(self):
        """
        Abstract method to create a bounding box annotation. The specifics of creating and storing this annotation depend on the platform in use.

        Parameters:
            class_name (str): The class name associated with the bounding box.
            annotation (list): A list containing the x, y coordinates, width, and height of the bounding box.
            data_key (str, optional): The unique identifier for the image. Required for the 'curate' platform.

        Returns:
            The result of the bounding box creation operation, which varies by platform.
        """
        pass

    @abstractmethod
    def upload_images(self):
        """
        Abstract method to upload images to the designated platform. The implementation should handle the specifics of the upload process,
        including any platform-specific requirements such as dataset naming.

        Parameters:
            images_path (str): The path to the images to be uploaded.
            dataset_name (str, optional): The name of the dataset to upload the images to. Required for the 'label' platform.

        Returns:
            The result of the image upload operation, which varies by platform.
        """
        pass
