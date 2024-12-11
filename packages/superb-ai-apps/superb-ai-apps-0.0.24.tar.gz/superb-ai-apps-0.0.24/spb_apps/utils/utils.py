import json
import logging
import os
import time
from pathlib import Path
from typing import Callable, TypeVar, Union
from uuid import uuid4
from zipfile import BadZipFile, ZipFile

import requests
import zipfile_deflate64
from directory_tree import display_tree
from phy_credit.exceptions import InvalidObjectException
from spb_label.exceptions import APIException  # InvaildObjectException,
from spb_label.exceptions import BadRequestException, ConflictException

logger = logging.getLogger("superb_label")


def separate_batches(image_batch_size: int, to_batch_list: list):
    """
    Separates a list of items into batches of a specified size.

    Args:
        image_batch_size (int): The size of each batch.
        to_batch_list (list): The list of items to be batched.

    Returns:
        list: A list of batches, where each batch is a sublist of the original list.
    """
    image_paths = []
    number_of_iteration = len(to_batch_list) // image_batch_size + 1
    for i in range(number_of_iteration):
        start = i * image_batch_size
        end = (
            (i + 1) * image_batch_size
            if (i + 1) * image_batch_size < len(to_batch_list)
            else False
        )
        if end is False:
            subset_image_paths = to_batch_list[start:]
        else:
            subset_image_paths = to_batch_list[start:end]
        image_paths.append(subset_image_paths)

    return image_paths


def read_info_from_zip_yolo(
    dataset_file: str, require_images_folder: bool = True
):
    """
    Reads and extracts information from a YOLO formatted zip file.

    Args:
        dataset_file (str): The path to the dataset zip file.
        require_images_folder (bool, optional): Flag to require an 'images' folder within the zip file. Defaults to True.

    Returns:
        tuple: A tuple containing lists of image paths, annotation paths, and the path to the classes.txt file.
    """
    try:
        with ZipFile(dataset_file, "r") as zip_file:
            file_list = [
                f
                for f in zip_file.namelist()
                if "__MACOSX" not in f and "DS_Store" not in f
            ]
            top_level_folder = os.path.commonprefix(file_list)
            second_level_folders, classes_txt = extract_folders_and_classes(
                file_list, top_level_folder
            )
            image_path_list = extract_paths(
                file_list,
                ["jpg", "jpeg", "png", "bmp"],
                "images",
                require_images_folder,
            )
            annotation_path_list = extract_paths(
                file_list, ["txt"], "labels", True
            )

            validate_contents(
                second_level_folders,
                classes_txt,
                image_path_list,
                annotation_path_list,
                require_images_folder,
            )
            zip_file.extractall(path=Path(dataset_file).parent)

        return image_path_list, annotation_path_list, classes_txt

    except BadZipFile as e:
        raise Exception(
            f"[Invalid zip file] '{dataset_file.split('/')[-1]}' {e}."
        )
    except Exception as e:
        display_error_and_extract(dataset_file, e)


def extract_folders_and_classes(file_list, top_level_folder):
    """
    Extracts second level folders and the classes.txt file from a list of file paths.

    Args:
        file_list (list): The list of file paths within the zip file.
        top_level_folder (str): The common prefix of all file paths, representing the top level folder.

    Returns:
        tuple: A tuple containing a set of second level folder names and the path to the classes.txt file.
    """
    second_level_folders = set()
    classes_txt = None
    for item in file_list:
        split_path = item.split("/")
        if top_level_folder and split_path[-1] == "classes.txt":
            classes_txt = item
        elif not top_level_folder and item.endswith("classes.txt"):
            classes_txt = item
        elif (top_level_folder and len(split_path) == 3) or (
            not top_level_folder and len(split_path) == 2
        ):
            second_level_folders.add(split_path[-2])
    return second_level_folders, classes_txt


def extract_paths(file_list, extensions, folder_name, required):
    """
    Extracts file paths from a list based on file extensions and folder name requirements.

    Args:
        file_list (list): The list of file paths within the zip file.
        extensions (list): A list of file extensions to filter by.
        folder_name (str): The name of the folder to filter by.
        required (bool): Flag to require the specified folder name in the file path.

    Returns:
        list: A list of file paths that match the specified extensions and folder name requirements.
    """
    return [
        f
        for f in file_list
        if f.split("/")[-1].split(".")[-1].lower() in extensions
        and (not required or f.split("/")[-2] == folder_name)
    ]


def validate_contents(
    second_level_folders,
    classes_txt,
    image_path_list,
    annotation_path_list,
    require_images_folder,
):
    """
    Validates the contents of the zip file against expected structure and files.

    Args:
        second_level_folders (set): A set of second level folder names extracted from the zip file.
        classes_txt (str): The path to the classes.txt file.
        image_path_list (list): A list of image file paths.
        annotation_path_list (list): A list of annotation file paths.
        require_images_folder (bool): Flag to require an 'images' folder within the zip file.

    Raises:
        Exception: If the validation fails due to missing required folders or files.
    """
    expected_folders = (
        {"labels", "images"} if require_images_folder else {"labels"}
    )
    if second_level_folders != expected_folders or not classes_txt:
        missing = expected_folders - second_level_folders
        missing_info = (
            f"Required folder(s), {', '.join(missing)}, are missing."
            if missing
            else "Required 'classes.txt' is missing."
        )
        raise Exception(missing_info)
    if require_images_folder and not image_path_list:
        raise Exception(
            "The 'images' folder contains no image files with valid formats."
        )
    if not annotation_path_list:
        raise Exception(
            "The 'labels' folder contains no label files with valid formats."
        )


def display_error_and_extract(dataset_file, e):
    """
    Displays an error message and extracts the contents of the zip file for inspection.

    Args:
        dataset_file (str): The path to the dataset zip file.
        e (Exception): The exception that was raised.

    Raises:
        Exception: Re-raises the exception after displaying the error message and extracting the zip file.
    """
    print("[Zip File]")
    with ZipFile(dataset_file, "r") as zip_file:
        zip_file.extractall(path=Path(dataset_file).parent)
        display_tree(str(Path(dataset_file).parent), max_depth=2)
    raise Exception(f"[Invalid zip file] {e}")


T = TypeVar("T")


def call_with_retry(
    fn: Callable[..., T],
    *args,
    _max_retries: int = 5,
    _sleep_time: int = 6,
    **kwargs,
) -> Union[T, None]:
    retry_count = 0
    while retry_count < _max_retries:
        if retry_count == 0:
            log_id = str(uuid4()).split("-")[0]
        try:
            res = fn(*args, **kwargs)
            break
        except requests.HTTPError as e:
            error_code = e.response.status_code
            if error_code == 503:  # 503: Service Unavailable
                logger.warning(
                    f"({log_id}) 503 Error occured, will be retried || fn: {fn.__name__} || Retry count: {retry_count}"
                )
            retry_count += 1
            time.sleep(_sleep_time)
        except APIException as e:
            logger.warning(
                f"({log_id}) 429 Error occured, will be retried || fn: {fn.__name__} || Retry count: {retry_count}"
            )
            retry_count += 1
            time.sleep(_sleep_time)
        except InvalidObjectException as e:
            raise Exception(
                f"({log_id}) Class name is not vaild, check the class list || fn: {fn.__name__} || Retry count: {retry_count}"
            )
        except Exception as e:

            if "429" in e.message:  # 429: too many request
                logger.error(
                    f"({log_id}) 429 Error occured, will be retried || fn: {fn.__name__} || Retry count: {retry_count}"
                )
                time.sleep(_sleep_time)
                retry_count += 1
            elif "503" in e.message:  # 503: too many request
                logger.error(
                    f"({log_id}) 503 Error occured, will be retried || fn: {fn.__name__} || Retry count: {retry_count}"
                )
                time.sleep(_sleep_time)
                retry_count += 1
            else:
                raise Exception(
                    f"({log_id}) Unknown error occured, will be retried || fn: {fn.__name__} || Retry count: {retry_count}"
                )
        if retry_count > 0:
            logger.debug(
                f"({log_id}) Retrying || fn: {fn.__name__} || Retry count: {retry_count}"
            )
    if retry_count == _max_retries:
        raise Exception(
            f"({log_id}) Max retries reached || fn: {fn.__name__} || Retry count: {retry_count}"
        )
    if retry_count > 0:
        logger.debug(
            f"({log_id}) Successfully completed || fn: {fn.__name__} || Retry count: {retry_count}"
        )

    return res


def safe_decode(text, encodings=("cp932", "cp949", "utf-8")):
    """
    Safely decodes a given byte string using a list of potential encodings.

    Args:
        text (bytes): The byte string to decode.
        encodings (tuple, optional): A tuple of encoding names to try. Defaults to ("cp932", "cp949", "utf-8").

    Returns:
        str: The decoded string.

    Notes:
        - The function tries each encoding in the provided order until one succeeds.
        - If all encodings fail, it returns a string decoded with UTF-8 and replaces undecodable characters.
    """
    for enc in encodings:
        try:
            return text.decode(enc)
        except UnicodeDecodeError:
            pass
    return text.decode("utf-8", "replace")


def unzip_files(zip_file_path: str, extract_dir: str):
    """
    Unzips a given zip file to a specified directory, handling different encodings for file names.

    Args:
        zip_file_path (str): The path to the zip file to extract.
        extract_dir (str): The directory where files will be extracted.

    Returns:
        list: A list of file names that were successfully extracted.

    Notes:
        - The function creates the extract directory if it doesn't exist.
        - It tries to decode file names using a safe decoding function to handle different encodings.
        - Files that can't be decoded are skipped.
        - The function handles the case where the zip file uses deflate64 compression, which requires a special library.
    """
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    try:
        with ZipFile(zip_file_path) as zip_file:
            file_list = []
            for member in zip_file.infolist():
                try:
                    member.filename = safe_decode(
                        member.filename.encode("cp437")
                    )
                except Exception as e:
                    try:
                        member.filename = safe_decode(
                            member.filename.encode("utf-8")
                        )
                    except Exception as e:
                        print(
                            f"Failed to decode {member.filename} in {zip_file_path}. Skipping."
                        )
                        continue

                zip_file.extract(member, path=extract_dir)
                file_list.append(member.filename)
    except:
        with zipfile_deflate64.ZipFile(zip_file_path, "r") as zip_file:
            file_list = []
            for member in zip_file.infolist():
                try:
                    member.filename = safe_decode(
                        member.filename.encode("cp437")
                    )
                except Exception as e:
                    try:
                        member.filename = safe_decode(
                            member.filename.encode("utf-8")
                        )
                    except Exception as e:
                        print(
                            f"Failed to decode {member.filename} in {zip_file_path}. Skipping."
                        )
                        continue

                zip_file.extract(member, path=extract_dir)
                file_list.append(member.filename)

    file_list = [
        f
        for f in file_list
        if "__MACOSX" not in f and "DS_Store" not in f and not f.endswith("/")
    ]

    return file_list
