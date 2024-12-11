import glob
import json
import logging
import os
import threading
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from uuid import uuid4

import phy_credit
import requests
import spb_label
from natsort import natsorted
from PIL import Image
from spb_label import sdk as spb_label_sdk
from spb_label.exceptions import NotFoundException, ParameterException
from spb_label.utils import SearchFilter
from tqdm import tqdm

from spb_apps.apps import SuperbApps
from spb_apps.utils.graphql_api import upload_to_platform
from spb_apps.utils.utils import call_with_retry

logger = logging.getLogger("superb_label")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

formatter_debug = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
handler_debug = logging.FileHandler("log_event.log")
handler_debug.setLevel(logging.DEBUG)
handler_debug.setFormatter(formatter_debug)

logger.addHandler(handler)
logger.addHandler(handler_debug)


class SuperbLabel(SuperbApps):
    def __init__(
        self,
        team_name: str,
        access_key: str,
        project_id: str = "",
        project_name: str = "",
        data_type: str = "image",
    ):
        """
        Initializes the SuperbLabel class with necessary details for operation.

        Parameters:
        - team_name (str): The name of the team.
        - access_key (str): The access key for authentication.
        - project_id (str, optional): The ID of the project to be set for the client. Defaults to an empty string.
        - project_name (str, optional): The name of the project. Defaults to an empty string.
        """
        self.team_name: str = team_name
        self.access_key: str = access_key
        super().__init__(team_name, access_key)
        try:
            self.client = spb_label_sdk.Client(
                team_name=team_name,
                access_key=access_key,
                project_id=project_id if project_id else None,
                project_name=project_name if project_name else None,
            )
        except NotFoundException as e:
            print(f"[INFO]: Project not found, creating a new Image project")
            self.client = spb_label_sdk.Client(
                team_name=team_name,
                access_key=access_key,
            )
            if data_type == "image":
                new_label_interface = (
                    phy_credit.imageV2.LabelInterface.get_default()
                )
            elif data_type == "video":
                new_label_interface = (
                    phy_credit.video.LabelInterface.get_default()
                )
            else:  # data_type == "pointclouds"
                new_label_interface = (
                    phy_credit.pointclouds.LabelInterface.get_default()
                )
            self.client.create_project(
                name=project_name,
                label_interface=new_label_interface.to_dict(),
                description="Created from Superb Apps",
            )
            self.client.set_project(name=project_name)
        self.project = self.client.project
        self.project_id = self.client.project.id
        self.project_type = self.client._project.get_project_type()

    def get_project_list(self, max_attempts=10):
        """
        Retrieves the list of all projects available for the current team.

        Args:
            max_attempts (int): Maximum number of attempts to fetch all projects.

        Returns:
            List[Dict]: A list of dictionaries, each containing project details.
        """
        manager = spb_label_sdk.ProjectManager(self.team_name, self.access_key)
        all_projects = []
        page = 1
        page_size = 10  # Maximum allowed page size
        attempts = 0

        while attempts < max_attempts:
            try:
                projects = manager.get_project_list(
                    page=page, page_size=page_size
                )
                all_projects.extend(projects[1])

                if len(projects[1]) < page_size:
                    break  # We've reached the last page

                page += 1
                attempts = 0  # Reset attempts on successful fetch
            except Exception as e:
                print(f"Error fetching page {page}: {str(e)}")
                attempts += 1
                if attempts >= max_attempts:
                    print(
                        f"Max attempts reached. Some projects may be missing."
                    )
                    break

        projects = []
        for project in all_projects:
            hold = {
                "id": project.id,
                "name": project.name,
                "workapp": project.workapp,
                "label_interface": project.label_interface,
                "label_count": project.label_count,
                "progress": project.progress,
            }
            projects.append(hold)
        print(f"Total projects fetched: {len(all_projects)}")
        return projects

    def change_project(self, project_name: str):
        """
        Changes the project context for the label client.

        Parameters:
            project_name (str): The name of the project to switch to.
        """
        self.client.set_project(name=project_name)

    def get_label_interface(self) -> Dict:
        """
        Retrieves the label interface configuration for the 'label' platform.

        Returns:
            Dict: The label interface configuration.
        """
        lb_interface = self.client.project.label_interface
        return lb_interface

    def download_image_by_filter(
        self,
        tags: list = [],
        data_key: str = "",
        status: list = [],
        path: str = None,
    ):
        """
        Downloads images by applying filters such as tags, data key, and status.

        Parameters:
            tags (list, optional): A list of tags to filter images. Defaults to [].
            data_key (str, optional): A specific data key to filter images. Defaults to "".
            status (list, optional): A list of statuses to filter images. Defaults to [].
            path (str, optional): The local file path to save the downloaded images. Defaults to None.
        """
        from concurrent.futures import ThreadPoolExecutor

        def download(label):
            self.download_image(label=label, path=path)

        count, labels = self.client.get_labels(
            tags=tags, data_key=data_key, status=status
        )
        print(f"Downloading {count} data to {path}")
        if count > 50:
            with ThreadPoolExecutor(max_workers=4) as executor:
                executor.map(download, labels)
        else:
            for label in labels:
                download(label)

    def download_export(
        self,
        input_path: str,
        export_id: str,
    ):
        """
        Download an export from the server to a local path.

        Parameters:
        - input_path (str): The local file path where the export will be saved.
        - export_id (str): The ID of the export to download.
        """
        print("[INFO] Checking for the export to be downloaded...")
        download_url = self.client.get_export(id=export_id).download_url
        r = requests.get(download_url)
        if r.status_code == 200:
            print("Saving export to local path")
            Path(input_path).parents[0].mkdir(parents=True, exist_ok=True)
            with open(input_path, "wb") as f:
                f.write(r.content)
        else:
            print(f"Failed to download the file. Status code: {r.status_code}")

    def get_labels(
        self,
        data_key: str = None,
        tags: list = None,
        assignees: list = None,
        status: list = None,
        all: bool = False,
    ) -> Tuple[int, List]:
        """
        Retrieve labels based on provided filters or all labels if specified.

        Parameters:
        - data_key (str, optional): Filter for a specific data key. Defaults to an empty string.
        - tags (list, optional): Filter for specific tags. Defaults to an empty list.
        - assignees (list, optional): Filter for specific assignees. Defaults to an empty list.
        - status (list, optional): Filter for specific status. Defaults to an empty list.
        - all (bool, optional): If True, ignores other filters and retrieves all labels. Defaults to False.

        Returns:
        Tuple[int, List]: A tuple containing the count of labels and a list of labels.
        """
        if all:
            # [ ] BUG: all 일때 커서가 다음으로 넘어가지 않음
            next_cursor = None
            count, labels, next_cursor = call_with_retry(
                fn=self.client.get_labels, cursor=next_cursor
            )

        else:
            filter = SearchFilter(project=self.project)
            if data_key:
                filter.data_key_matches = data_key
            if tags:
                filter.tag_name_all = tags
            if assignees:
                filter.assignee_is_any_one_of = assignees
            if status:
                filter.status_is_any_one_of = status
            next_cursor = None
            count, labels, next_cursor = call_with_retry(
                fn=self.client.get_labels, filter=filter, cursor=next_cursor
            )

            # [x] TODO: 검색된 라벨이 없을 때의 예외처리
            if count == 0:
                labels = None
                return count, labels

        return count, labels

    def download_image(
        self,
        label: spb_label_sdk.DataHandle = None,
        data_key: str = None,
        path: str = "",
    ):
        """
        Download an image associated with a label to a specified path.

        Parameters:
        - label (spb_label.DataHandle, optional): The label data handle containing the image to download. If None, the label is retrieved using the data_key.
        - data_key (str, optional): The unique identifier for the image. Used if label is None.
        - path (str): The local file path where the image will be saved. Defaults to "/".
        """
        if label is None:
            label = self.get_label(data_key=data_key)
        label.download_image(download_to=path)

    def get_width_height(
        self, label: spb_label_sdk.DataHandle = None, data_key: str = None
    ) -> Tuple[int, int]:
        """
        Download an image associated with a label, return its width and height, and delete the image.

        Parameters:
        - label (spb_label.DataHandle, optional): The label data handle containing the image to download. If None, the label is retrieved using the data_key.
        - data_key (str, optional): The unique identifier for the image. Used if label is None.

        Returns:
        Tuple[int, int]: A tuple containing the width and height of the downloaded image.
        """
        if label is None:
            label = self.get_label(data_key=data_key)
        image_url = label.get_image_url()
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        width, height = img.size

        return width, height

    def make_bbox_annotation(
        self,
        class_name: str,
        annotation: list,
        data_type: str = "image",
    ):
        """
        Create a bounding box setting for a given class name and annotation coordinates.

        Parameters:
        - class_name (str): The class name associated with the bounding box.
        - annotation (list)
            - image: A list containing the coordinates of the bounding box in the order [x, y, width, height].
            - video: A list containing the tracking_id and a list of coordinates for each frame, like [tracking_id, [[x, y, width, height, frame_num],...]].

        Returns:
        A tuple containing the class name and a dictionary with the bounding box coordinates.
        """
        if data_type == "image":
            bbox = {
                "class_name": class_name,
                "annotation": {
                    "coord": {
                        "x": annotation[0],
                        "y": annotation[1],
                        "width": annotation[2],
                        "height": annotation[3],
                    }
                },
            }

        elif data_type == "video":
            if len(annotation) != 2 or not isinstance(annotation[1], list):
                raise ValueError(
                    "Annotation for video must be in the format [tracking_id, [[x, y, width, height, frame_num],...]]"
                )

            tracking_id = annotation[0]
            frame_annotations = annotation[1]

            if not all(len(anno) == 5 for anno in frame_annotations):
                raise ValueError(
                    "Each annotation must have 5 elements: [x, y, width, height, frame_num]"
                )

            bbox = {
                "class_name": class_name,
                "annotation_type": "box",
                "tracking_id": tracking_id,
                "annotations": [],
            }

            # annotations 리스트에서 각 프레임의 바운딩 박스 정보를 추가
            for anno in sorted(
                frame_annotations, key=lambda x: x[4]
            ):  # 프레임 번호 기준으로 정렬
                bbox["annotations"].append(
                    {
                        "coord": {
                            "x": anno[0],
                            "y": anno[1],
                            "width": anno[2],
                            "height": anno[3],
                        },
                        "frame_num": anno[4],
                        "properties": [],
                    }
                )

        else:  # data_type == "pointclouds"
            print(
                "The SDK does not yet support making bbox for point clouds data types."
            )
            return

        return bbox

    def build_seg_pieces(self, seg: list) -> list:
        """
        Constructs a list of dictionaries representing points from a segmentation list.

        Parameters:
        - seg (list): A list of integers representing x and y coordinates alternately.

        Returns:
        list: A list of dictionaries, each containing an 'x' and 'y' coordinate.
        """
        poly = []
        x, y = 0, 0
        for index, p in enumerate(seg):
            if index % 2:  # odd -> y
                y = p
                poly.append({"x": x, "y": y})
            else:  # even -> x
                x = p
        if poly:
            poly.append({"x": seg[0], "y": seg[1]})
        return poly

    def parse_segmentation(self, segmentation: list) -> dict:
        """
        Parses a list of segmentations into a structured dictionary format suitable for annotations.

        Parameters:
        - segmentation (list): A list of lists, each sublist contains integers representing x and y coordinates alternately.

        Returns:
        dict: A dictionary with coordinates of points and a flag indicating multiple segmentations.
        """
        points = []
        for seg in segmentation:
            add_poly = self.build_seg_pieces(seg)
            points.append([add_poly])
        annotation = {
            "coord": {"points": points},
            "multiple": True,
        }
        return annotation

    def upload_image(
        self,
        image_path: str,
        dataset_name: str,
        data_key: str = None,
        ignore: bool = False,
    ):
        """
        Upload an image to a specified dataset. If the 'ignore' flag is set to True, the image will be uploaded without checking for existing entries.
        If 'ignore' is False, it checks if the image already exists using the provided 'data_key' or derives a key from the image path.

        Parameters:
        - image_path (str): The path to the image to be uploaded.
        - dataset_name (str): The name of the dataset to upload the image to.
        - data_key (str, optional): The unique identifier for the image. If not provided, it is derived from the image path.
        - ignore (bool, optional): If set to True, the image will be uploaded without checking for existing entries. Defaults to False.

        Raises:
        - ParameterException: If the upload fails due to incorrect parameters.
        """
        if ignore:
            try:
                self.client.upload_image(
                    path=image_path,
                    dataset_name=dataset_name,
                )
            except ParameterException as e:
                print(f"[ERROR]: Uploading went wrong: {e}")
        else:
            if data_key is None:
                key = image_path.split("/")[-1]
                count, labels = self.get_labels(data_key=key)
            else:
                count, labels = self.get_labels(data_key=data_key)
                key = data_key

            if count == 0:
                # try:
                call_with_retry(
                    fn=self.client.upload_image,
                    path=image_path,
                    dataset_name=dataset_name,
                    key=data_key,
                )
                # except ParameterException as e:
                #     print(f"[ERROR]: Uploading went wrong: {e}")

            else:
                print(
                    f"[INFO]: Image already exists, skipping upload for data key {key}"
                )

    def upload_binary_image(
        self,
        binary_data: bytes,
        file_type: str,
        data_key: str,
        dataset_name: str,
    ):
        """
        Upload a binary image to a specified dataset.

        Parameters:
        - binary_data (bytes): The binary data of the image to be uploaded.
        - file_type (str): The file type of the image (e.g., 'jpg', 'png').
        - data_key (str): The unique identifier for the image.
        - dataset_name (str): The name of the dataset to upload the image to.

        Raises:
        - KeyError: If a required key is missing in the parameters.
        - ValueError: If the file size or type is incorrect.
        - Exception: For any other unexpected errors.
        """
        try:
            team_name = self.team_name
            access_key = self.access_key
            project_id = self.project_id
            file_size = len(binary_data)

            params = {}
            params["team_name"] = team_name
            params["access_key"] = access_key
            params["project_id"] = project_id
            params["binary_data"] = binary_data
            params["file_type"] = file_type
            params["file_size"] = file_size
            params["data_key"] = data_key
            params["dataset_name"] = dataset_name

            response = upload_to_platform(params)
            if "success" in response:
                return response
            else:
                return response

        except KeyError as e:
            print(f"Missing key in params: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def upload_video(
        self, video_path: str, dataset_name: str, num_threads: int = 3
    ):
        """
        Uploads video data to a specified dataset. This method handles the upload of multiple video frames concurrently.

        Parameters:
        - video_path (str): The directory path containing video frames.
        - dataset_name (str): The name of the dataset to which the video will be uploaded.
        - num_threads (int, optional): The number of threads to use for concurrent uploads. Defaults to 3.

        Raises:
        - Exception: If the project type does not support video uploads.
        """
        if self.project_type == "image":
            raise Exception("Cannot upload image to a video project")

        file_names = [
            os.path.basename(file_path)
            for file_path in glob.glob(os.path.join(video_path, "*.jpg"))
        ]
        key = os.path.basename(video_path)

        if len(file_names) > 1000:
            print(
                "[INFO] Large video detected, splitting into chunks of 1000 frames"
            )
            self.upload_large_video(
                file_names, video_path, dataset_name, key, num_threads
            )
        else:
            self.upload_small_video(
                file_names, video_path, dataset_name, key, num_threads
            )

    def upload_large_video(
        self, file_names, video_path, dataset_name, key, num_threads
    ):
        chunks = [
            file_names[i : i + 1000] for i in range(0, len(file_names), 1000)
        ]
        for index, chunk in enumerate(chunks):
            folder_key = f"{key}_{index + 1}"
            self.process_video_chunk(
                chunk, video_path, dataset_name, folder_key, num_threads
            )

    def upload_small_video(
        self, file_names, video_path, dataset_name, key, num_threads
    ):
        self.process_video_chunk(
            file_names, video_path, dataset_name, key, num_threads
        )

    def process_video_chunk(
        self, file_names, video_path, dataset_name, key, num_threads
    ):
        asset_video = {
            "dataset": dataset_name,
            "data_key": key,
            "files": {
                "path": video_path,
                "file_names": natsorted(file_names),
            },
        }
        project_id = self.project_id
        command = spb_label.Command(type="create_videodata")
        result = spb_label.run(
            command=command,
            option=asset_video,
            optional={"projectId": project_id},
        )
        file_infos = json.loads(result.file_infos)
        self.upload_files_concurrently(
            file_infos, file_names, num_threads, video_path
        )

    def upload_files_concurrently(
        self, file_infos, file_names, num_threads, video_path
    ):
        print(f"[INFO] Uploading video to dataset")
        threads = []
        for tid in range(num_threads):
            start_index = tid * len(file_infos) // num_threads
            end_index = (tid + 1) * len(file_infos) // num_threads
            thread = threading.Thread(
                target=self.video_upload_worker,
                args=(file_infos[start_index:end_index], tid, video_path),
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def video_upload_worker(self, file_infos, tid, path):
        """
        Worker function for uploading video files. This function is intended to be run in a separate thread.

        Parameters:
        - file_infos (list): List of file information dictionaries containing presigned URLs and file names.
        - tid (int): Thread identifier.
        - path (str): Base path for the video files.
        """
        for file_info in file_infos:
            file_name = file_info["file_name"]
            file_path = os.path.join(path, file_name)
            with open(file_path, "rb") as file_data:
                response = requests.Session().put(
                    file_info["presigned_url"], data=file_data.read()
                )
            if response.status_code != 200:
                with open("error.txt", "a") as error_file:
                    error_file.write(f"Upload failed for {file_path}\n")

    def upload_images(
        self, image_paths: list, dataset_name: str, ignore: bool = False
    ):
        """
        Upload multiple images to a specified dataset. This function iterates over a list of image paths and uploads each using the 'upload_image' method.

        Parameters:
        - image_paths (list): A list of paths to the images to be uploaded.
        - dataset_name (str): The name of the dataset to upload the images to.
        - ignore (bool, optional): If set to True, the images will be uploaded without checking for existing entries. Defaults to False.

        Raises:
        - ParameterException: If the upload fails due to incorrect parameters.
        """
        if self.project_type == "video":
            raise Exception("Cannot upload video to an image project")
        for path in image_paths:
            try:
                self.upload_image(
                    image_path=path, dataset_name=dataset_name, ignore=ignore
                )
            except ParameterException as e:
                print(f"[ERROR]: Uploading went wrong: {e}")

    def upload_annotation(
        self,
        label: spb_label_sdk.DataHandle,
        annotations: list,
        overwrite: bool = False,
        data_type: str = "image",
    ):
        """
        Upload annotations for a given label.

        Parameters:
        - label (spb_label.DataHandle): The label to which the annotations will be added.
        - annotations (list): A list of annotations to be added to the label.
        - overwrite (bool, optional): A flag indicating whether existing annotations should be overwritten. Defaults to False.
        """
        if data_type == "image":
            if overwrite:
                labels = []
                for anno in annotations:
                    try:
                        bbox = self.make_bbox_annotation(
                            class_name=anno[0], annotation=anno[1]
                        )
                    except Exception:
                        raise Exception(
                            f"[ERROR]: Error occurred while making bbox, check the annotation format || {anno}"
                        )
                    labels.append(bbox)
                if len(labels) == 0:
                    raise Exception(
                        f"[ERROR]: No annotations found for the label"
                    )
                call_with_retry(fn=label.set_object_labels, labels=labels)
            else:
                for anno in annotations:
                    try:
                        bbox = self.make_bbox_annotation(
                            class_name=anno[0], annotation=anno[1]
                        )
                    except Exception:
                        raise Exception(
                            f"[ERROR]: Error occurred while making bbox, check the annotation format || {anno}"
                        )
                    if "class_name" not in bbox or "annotation" not in bbox:
                        raise Exception(
                            "[ERROR]: No annotations found for the label"
                        )
                    call_with_retry(
                        fn=label.add_object_label,
                        class_name=bbox["class_name"],
                        annotation=bbox["annotation"],
                    )

        elif data_type == "video":
            overwrite = True  # The current SDK does not support the add_object_label function for video data types.
            labels = []
            for anno in annotations:
                try:
                    bbox = self.make_bbox_annotation(
                        class_name=anno[0],
                        annotation=anno[1],
                        data_type="video",
                    )  # annotation=anno[1] -> [tracking_id, [[x, y, width, height, frame_num],...]]
                except Exception:
                    raise Exception(
                        f"[ERROR]: Error occurred while making bbox, check the annotation format || {anno}"
                    )
                labels.append(bbox)
            if len(labels) == 0:
                raise Exception(f"[ERROR]: No annotations found for the label")
            call_with_retry(fn=label.set_object_labels, labels=labels)

        else:  # data_type == "pointclouds":
            raise Exception(
                f"[ERROR]: Apps SDK does not yet support uploading annotations for pointclouds."
            )

        call_with_retry(fn=label.update_info)

    def add_object_classes_to_project(
        self,
        class_name: str,
        class_type: str,
        data_type: str = "image",
        properties: list = [],
    ):
        """
        Adds a specific type of object class to the label interface of the project based on the specified class type.

        Parameters:
        - class_name (str): The name of the class to be added to the label interface.
        - class_type (str): The type of class to be added. Supported types include 'bbox' (bounding box), 'polygon', 'polyline', 'rbox' (rotated bounding box), and '2dcuboid'.

        Returns:
        A tuple containing the updated label interface.
        """
        existing_label_interface = self.client.project.label_interface
        if data_type == "image":
            if existing_label_interface:
                label_interface = phy_credit.imageV2.LabelInterface.from_dict(
                    existing_label_interface
                )
                object_detection = (
                    phy_credit.imageV2.ObjectDetectionDef.from_dict(
                        existing_label_interface.get("object_detection")
                    )
                )
            else:
                label_interface = (
                    phy_credit.imageV2.LabelInterface.get_default()
                )
                object_detection = (
                    phy_credit.imageV2.ObjectDetectionDef.get_default()
                )
        elif data_type == "video":
            if existing_label_interface:
                label_interface = phy_credit.video.LabelInterface.from_dict(
                    existing_label_interface
                )
                object_tracking = phy_credit.video.ObjectTrackingDef.from_dict(
                    existing_label_interface.get("object_tracking")
                )
            else:
                label_interface = phy_credit.video.LabelInterface.get_default()
                object_tracking = (
                    phy_credit.video.ObjectTrackingDef.get_default()
                )
        else:  # data_type == "pointclouds"
            if existing_label_interface:
                label_interface = (
                    phy_credit.pointclouds.LabelInterface.from_dict(
                        existing_label_interface
                    )
                )
                object_tracking = (
                    phy_credit.pointclouds.ObjectTrackingDef.from_dict(
                        existing_label_interface.get("object_tracking")
                    )
                )
            else:
                label_interface = (
                    phy_credit.pointclouds.LabelInterface.get_default()
                )
                object_tracking = (
                    phy_credit.pointclouds.ObjectTrackingDef.get_default()
                )

        if class_type == "bbox":
            bbox_suite_class_id = str(uuid4())
            bbox_suite_class_name = class_name

            if data_type == "image":
                object_detection.add_box(
                    name=bbox_suite_class_name,
                    id=bbox_suite_class_id,
                    properties=properties,
                )
            else:
                object_tracking.add_box(
                    name=bbox_suite_class_name,
                    id=bbox_suite_class_id,
                    properties=properties,
                )

        if class_type == "polygon":
            seg_suite_class_id = str(uuid4())
            seg_suite_class_name = class_name

            object_detection.add_polygon(
                name=seg_suite_class_name,
                id=seg_suite_class_id,
                properties=properties,
            )

        if class_type == "polyline":
            seg_suite_class_id = str(uuid4())
            seg_suite_class_name = class_name

            if data_type == "image":
                object_detection.add_polyline(
                    name=seg_suite_class_name,
                    id=seg_suite_class_id,
                    properties=properties,
                )
            else:
                object_tracking.add_polyline(
                    name=seg_suite_class_name,
                    id=seg_suite_class_id,
                    properties=properties,
                )

        if class_type == "rbox":
            seg_suite_class_id = str(uuid4())
            seg_suite_class_name = class_name

            if data_type == "image":
                object_detection.add_rbox(
                    name=seg_suite_class_name,
                    id=seg_suite_class_id,
                    properties=properties,
                )
            else:
                object_tracking.add_rbox(
                    name=seg_suite_class_name,
                    id=seg_suite_class_id,
                    properties=properties,
                )

        if class_type == "2dcuboid":
            seg_suite_class_id = str(uuid4())
            seg_suite_class_name = class_name

            if data_type == "image":
                object_detection.add_2dcuboid(
                    name=seg_suite_class_name,
                    id=seg_suite_class_id,
                    properties=properties,
                )
            else:
                object_tracking.add_2dcuboid(
                    name=seg_suite_class_name,
                    id=seg_suite_class_id,
                    properties=properties,
                )

        if data_type == "image":
            label_interface.set_object_detection(
                object_detection=object_detection
            )
        else:
            label_interface.set_object_tracking(
                object_tracking=object_tracking
            )

        call_with_retry(
            fn=self.client.update_project,
            id=self.client.project.id,
            label_interface=label_interface.to_dict(),
        )
        return label_interface

    def update_tags(self, data_key: str, tags: list):
        filter = SearchFilter(project=self.project)
        try:
            filter.data_key_matches = data_key
            data_handler = self.client.get_labels(filter=filter, page_size=1)[
                1
            ][0]
            data_handler.update_tags(tags=tags)
            data_handler.update_info()
        except Exception as e:
            print(f"Failed update tags {data_key}: {e}")
