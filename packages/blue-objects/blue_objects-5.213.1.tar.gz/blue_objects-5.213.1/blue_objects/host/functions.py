import os
from typing import Union, Tuple, List

from blueness import module
from blue_options.logger import crash_report

from blue_objects import NAME, file
from blue_objects.logger import logger

NAME = module.name(__file__, NAME)


def shell(
    command: str,
    clean_after: bool = False,
    return_output: bool = False,
    work_dir: str = ".",
    log: bool = False,
) -> Union[
    bool,
    Tuple[bool, List[str]],
]:
    if log:
        logger.info(f"{NAME}.shell({command})")

    success = True
    output = []

    if return_output:
        output_filename = file.auxiliary("shell", "txt")
        command += f" > {output_filename}"

    current_path = os.getcwd()
    try:
        os.chdir(work_dir)

        try:
            os.system(command)
        except:
            crash_report(f"host.shell({command}) failed")
            success = False

    finally:
        os.chdir(current_path)

    if success and return_output:
        success, output = file.load_text(output_filename)

        if clean_after:
            file.delete(output_filename)

    return (success, output) if return_output else success


def unzip(
    zip_filename: str,
    output_folder: str = "",
    log: bool = False,
) -> bool:
    if not output_folder:
        output_folder = file.path(zip_filename)

    return shell(
        command=f'unzip -q -o "{zip_filename}" -d "{output_folder}"',
        log=log,
    )
