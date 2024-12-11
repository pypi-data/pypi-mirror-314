import json
import os
import time
from pathlib import Path
from timeit import default_timer as timer
from typing import List, Tuple
from uuid import uuid4

import requests
import spb_curate
from spb_curate.error import ConflictError
from spb_curate import Image, ImageSourceLocal

from spb_apps.apps import SuperbApps
from spb_apps.utils.converter import convert_yolo_bbox
from spb_apps.utils.utils import separate_batches

SLEEP_INTERVAL = 5  # Time in seconds to wait between loop iterations.


class SuperbCurate(SuperbApps):
    """
    A class to handle dataset curation tasks including image and annotation uploads for Superb AI.

    Attributes:
        team_name (str): Name of the team.
        access_key (str): Access key for authentication.
        dataset_name (str): Name of the dataset.
        is_dev (bool): Flag to set the environment to development mode.
    """

    def __init__(
        self,
        team_name: str,
        access_key: str,
        dataset_name: str = "",
        is_dev: bool = False,
    ):
        """
        Initializes the SuperbCurate class with team, dataset, and slice details.
        Optionally sets the environment to development mode.

        Args:
            team_name (str): Name of the team.
            access_key (str): Access key for authentication.
            dataset_name (str, optional): Name of the dataset.
            is_dev (bool, optional): Flag to set the environment to development mode.
        """
        super().__init__(team_name, access_key)
        self.team_name: str = team_name
        self.access_key: str = access_key
        self.dataset_name: str = dataset_name
        spb_curate.team_name = self.team_name
        spb_curate.access_key = self.access_key
        if is_dev:
            spb_curate.api_base = "https://api.dev.superb-ai.com"

        if dataset_name:
            try:
                self.dataset = spb_curate.fetch_dataset(name=dataset_name)
            except:
                print(
                    f"Dataset does not exist, Creating Dataset {dataset_name}"
                )
                self.dataset = spb_curate.create_dataset(
                    name=dataset_name, description="Demo dataset."
                )

    def get_slice(self, slice_name: str):
        """
        Fetches a slice from the dataset using its name.

        Args:
            slice_name (str): Name of the slice to fetch.

        Returns:
            The fetched slice object.
        """
        if slice_name:
            slice = self.dataset.fetch_slice(name=slice_name)
        return slice

    def curate_prep_images(self, images_path: list) -> List[spb_curate.Image]:
        """
        Prepares local images for Superb Curate by creating a list of Superb Curate images.

        Args:
            images_path (list): List of paths to images to be uploaded.

        Returns:
            List[spb_curate.Image]: List of prepared images for upload.
        """
        curate_images: List[spb_curate.Image] = []
        for image in images_path:
            curate_images.append(
                spb_curate.Image(
                    key=image.split("/")[-1],
                    source=spb_curate.ImageSourceLocal(asset=image),
                    metadata={},
                )
            )

        return curate_images

    def upload_images(self, image_path: list):
        """
        Uploads images in batches to the dataset.

        Args:
            image_path (list): List of image paths to upload.
        """
        separated_images = separate_batches(
            image_batch_size=500, to_batch_list=image_path
        )
        total_loops = len(separated_images)
        for idx, sep_images in enumerate(separated_images, start=1):
            curate_images = self.curate_prep_images(images_path=sep_images)
            image_import_job = spb_curate.Image.create_bulk(
                dataset_id=self.dataset["id"], images=curate_images
            )

            print(f"created an image import job: ({idx}/{total_loops})")
            start_time = timer()

            while True:
                image_import_job = spb_curate.Job.fetch(
                    id=image_import_job["id"]
                )
                print(
                    f"job progress: {image_import_job['progress']}", end="\r"
                )

                if image_import_job["status"] == "COMPLETE":
                    if image_import_job["result"]["fail_detail"]:
                        print(image_import_job["result"]["fail_detail"])
                        print(image_import_job["fail_reason"])
                    break

                if image_import_job["status"] == "FAILED":
                    if image_import_job["result"]["fail_detail"]:
                        print(
                            "[INFO] Fail detail: ",
                            image_import_job["result"]["fail_detail"],
                        )
                        print(
                            "[INFO] Fail reason: ",
                            image_import_job["fail_reason"],
                        )
                    break
                time.sleep(SLEEP_INTERVAL)

            print(f"total time: {timer() - start_time}")

    def upload_binary_images(self, images: list) -> List:
        """
        Uploads a list of binary image data to the dataset.

        Args:
            images (list): A list of image data to be uploaded. Each element in the list should be a list containing:
                        - [0] str: The file name of the image (used as the key).
                        - [1] bytes: The binary data of the image.

        Returns:
            List: A list of the results from the image upload job.

        Example:
            images = [
                ["image1.jpg", b'binary_data_of_image1'],
                ["image2.png", b'binary_data_of_image2']
            ]
            upload_result = upload_binary_images(images)
        """
        print(f"created an image import job: {len(images)}")
        start_time = timer()

        image_objects = []
        for img_data in images:
            img_object = Image(
                key=img_data[0],
                source=ImageSourceLocal(asset=img_data[1]),
                metadata={
                    "misc-key": "new-value",
                },
            )
            image_objects.append(img_object)

        job = self.dataset.add_images(images=image_objects)
        job.wait_until_complete()

        print(f"{len(images)} images uploaded")
        print(f"total time: {timer() - start_time}")

    def curate_prep_annotations(self, annotation: list) -> List:
        """
        Prepares annotations for upload by creating a list of spb_curate.Annotation objects.

        Args:
            annotation (list): List of dictionaries containing annotation details.

        Returns:
            List[spb_curate.Annotation]: List of prepared annotations for upload.
        """
        curate_annotations: List[spb_curate.Annotation] = []
        for anno in annotation:
            meta = anno.get("metadata", {"iscrowd": 0})
            curate_annotations.append(
                spb_curate.Annotation(
                    image_key=anno["data_key"],
                    annotation_class=anno["class_name"],
                    annotation_type=anno["annotation_type"],
                    annotation_value=anno["annotation"],
                    metadata=meta,
                )
            )

        return curate_annotations

    def curate_upload_annotations(self, annotation_list: list):
        """
        Uploads annotations in batches to the dataset.

        Args:
            annotation_list (list): List of annotations to upload.
        """
        separated_annotations = separate_batches(
            image_batch_size=500, to_batch_list=annotation_list
        )
        for idx, sep_annotations in enumerate(separated_annotations, start=1):
            annotation_import_job = spb_curate.Annotation.create_bulk(
                dataset_id=self.dataset["id"], annotations=sep_annotations
            )

            while True:
                annotation_import_job = spb_curate.Job.fetch(
                    id=annotation_import_job["id"]
                )
                print(
                    f"[INFO] {(idx-1) * 500 + annotation_import_job['progress']} / {len(annotation_list)} annotations updated"
                )

                if annotation_import_job["status"] == "COMPLETE":
                    if annotation_import_job["result"]["fail_detail"]:
                        print(
                            "[INFO] Fail detail: ",
                            annotation_import_job["result"]["fail_detail"],
                        )
                        print(
                            "[INFO] Fail reason: ",
                            annotation_import_job["fail_reason"],
                        )
                    break

                if annotation_import_job["status"] == "FAILED":
                    if annotation_import_job["result"]["fail_detail"]:
                        print(
                            "[INFO] Fail detail: ",
                            annotation_import_job["result"]["fail_detail"],
                        )
                        print(
                            "[INFO] Fail reason: ",
                            annotation_import_job["fail_reason"],
                        )
                    break
                time.sleep(SLEEP_INTERVAL)

    def get_width_height(self, data_key: str) -> Tuple[int, int]:
        """
        Fetches the width and height of an image using its data key.

        Args:
            data_key (str): The unique identifier for the image.

        Returns:
            Tuple[int, int]: A tuple containing the width and height of the image.
        """
        image = self.dataset.fetch_images(key=data_key)[0]
        meta = image["metadata"]
        width, height = meta["_width"], meta["_height"]
        return width, height

    def download_image(self, data_key: str, path: str = ""):
        """
        Downloads an image from the dataset using its data key.

        Args:
            data_key (str): The unique identifier for the image.
            path (str): The path where the image will be downloaded.
        """
        image_url = self.dataset.fetch_images(
            key=data_key, include_image_url=True
        )[0]["image_url"]
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            os.makedirs(
                os.path.dirname(os.path.join(path, data_key)),
                exist_ok=True,
            )
            with open(os.path.join(path, data_key), "wb") as f:
                f.write(response.content)
            print(
                f"[INFO] Image downloaded successfully: {os.path.join(path, data_key)}"
            )
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to download image: {e}")

    def make_bbox_annotation(
        self, data_key: str, class_name: str, annotation: list
    ) -> spb_curate.Annotation:
        """
        Creates a bounding box annotation for a given image.

        Args:
            data_key (str): The unique identifier for the image.
            class_name (str): The class name associated with the bounding box.
            annotation (list): A list containing the x, y coordinates, width, and height of the bounding box.

        Returns:
            spb_curate.Annotation: An Annotation object representing the bounding box.
        """
        bounding_box = spb_curate.BoundingBox(
            raw_data={
                "x": annotation[0],
                "y": annotation[1],
                "width": annotation[2],
                "height": annotation[3],
            }
        )
        bbox_annotation = spb_curate.Annotation(
            image_key=data_key,
            annotation_class=class_name,
            annotation_type="box",
            annotation_value=bounding_box,
            metadata={},
        )

        return bbox_annotation

    def download_image_by_slice(self, slice_name: str, download_path: str):
        """
        Downloads all images within a specified slice of the dataset.

        This method fetches all image keys within a given slice and iteratively
        downloads each image to the specified download path.

        Args:
            slice_name (str): The name of the slice from which to download images.
            download_path (str): The local file path where the images will be saved.
        """
        slice = self.dataset.fetch_images(
            slice=slice_name, include_image_url=True
        )
        for image in slice:
            self.download_image(data_key=image["key"], path=download_path)

    def download_image_by_slice(self, slice_name: str, download_path: str):
        """
        Downloads an image by its slice name to a specified path. This method is exclusive to the Curate platform.

        Args:
            slice_name (str): The name of the slice from which to download the image.
            download_path (str): The local file path where the downloaded image will be saved.
        """
        self.download_image_by_slice(
            slice_name=slice_name, download_path=download_path
        )
