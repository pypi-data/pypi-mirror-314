"""gr.File() component"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

import gradio_client.utils as client_utils
from gradio_client import handle_file

from gradio import processing_utils
from gradio.components.base import Component
from gradio.data_classes import FileData, ListFiles
from gradio.events import Events
from gradio.exceptions import Error
from gradio.utils import NamedString

if TYPE_CHECKING:
    from gradio.components import Timer


def convert_to_pdf(input_file: Path, temp_dir: Path) -> Union[str, None]:
    output_file = temp_dir / input_file.with_suffix(".pdf").name
    print("in convert_to_pdf")
    print(f"output_file: {output_file}")
    print(temp_dir)
    if output_file.exists() and (time.time() - os.path.getctime(input_file) < 300):
        # si le fichier existe et a été créé il y a moins de 5 minutes, on le transforme à nouveau en pdf
        # sinon on garde le fichier en cache de gradio pour éviter de consommer temps de création (effacé toutes les 24h)
        os.remove(output_file)
    if not output_file.exists():
        result = subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to",
                'pdf:impress_pdf_Export:{"ReduceImageResolution":{"type":"boolean","value":true},"MaxImageResolution":{"type":"long","value":75},"ExportBookmarks":{"type":"boolean","value":false},"ExportFormFields":{"type":"boolean","value":false},"Quality":{"type":"long","value":50},"IsSkipEmptyPages":{"type":"boolean","value":true}}',
                str(input_file),
                "--outdir",
                str(temp_dir),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # Afficher les sorties pour le débogage
        print("stdout:", result.stdout.decode("utf-8"))
        print("stderr:", result.stderr.decode("utf-8"))
    return str(output_file)


def convert_file(file, temp_dir, ms_formats, max_size) -> str:
    path = Path(file)
    if path.suffix in ms_formats and path.stat().st_size < max_size:
        print("in convert_file")
        print(temp_dir)
        return convert_to_pdf(Path(file), Path(temp_dir))
    else:
        return file


def is_libreoffice_installed() -> bool:
    """Vérifie si LibreOffice est installé."""
    possible_executables = ["libreoffice", "soffice"]
    for executable in possible_executables:
        if shutil.which(executable):
            return True
    return False

from gradio.events import Dependency

class NeoViewer(Component):
    """
    A file viewer working with differents types of files such as PDF, images, and MS files (if libre office is installed).
    """

    EVENTS = [Events.change]

    def __init__(
        self,
        value: str | list[str] | Callable | None = None,
        *,
        label: str | None = None,
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        height: int | float | None = None,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
        index_of_file_to_show: int = 0,
        max_size: int = 5000000,
        max_pages: int = 100,
        ms_files: bool = True,  # les fichiers MS sont longs à convertir en PDF, donc on laisse le choix de les enlever
        libre_office: bool = is_libreoffice_installed(),
    ):
        """
        Parameters:
            value: Default file(s) to display, given as a str file path or URL, or a list of str file paths / URLs. If callable, the function will be called whenever the app loads to set the initial value of the component.
            label: the label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.
            every: Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            inputs: Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.
            show_label: if True, will display label.
            container: If True, will place the component in a container - providing some extra padding around the border.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            height: The default height of the file component when no files have been uploaded, or the maximum height of the file component when files are present. Specified in pixels if a number is passed, or in CSS units if a string is passed. If more files are uploaded than can fit in the height, a scrollbar will appear.
            interactive: if True, will allow users to upload a file; if False, can only be used to display files. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
            index_of_file_to_show: int = 0, # index of file to show in case of multiple files
            max_size: maximum size of file to show in bytes
            max_pages: maximum number of pages of file to show
            ms_files: if True, will convert MS files to PDF for display, but it is a long process. Unactive if libre_office is False
            libre_office: if True, means that LibreOffice is installed and can be used to convert MS files to PDF
        """

        self.data_model = ListFiles
        self.height = height
        self.index_of_file_to_show = index_of_file_to_show
        self.max_size = max_size
        self.max_pages = max_pages
        self.ms_files = ms_files
        self.libre_office = libre_office

        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            value=value,
        )

    def _process_single_file(self, f: FileData) -> NamedString | bytes:
        file_name = f.path
        tempfile.NamedTemporaryFile(delete=False, dir=self.GRADIO_CACHE)
        return NamedString(file_name)

    def preprocess(self, payload: ListFiles | None) -> str | list[str] | None:
        """
        Parameters:
            payload: NeoViewer information as a FileData object, or a list of FileData objects.
        Returns:
            Passes the file as a `str`object, or a list of `str`.
        """
        if payload is None:
            return None
        else:
            return [self._process_single_file(f) for f in payload]  # type: ignore

    def _download_files(self, value: str | list[str]) -> str | list[str]:
        downloaded_files = []
        if isinstance(value, list):
            for file in value:
                if client_utils.is_http_url_like(file):
                    downloaded_file = processing_utils.save_url_to_cache(
                        file, self.GRADIO_CACHE
                    )
                    downloaded_files.append(downloaded_file)
                else:
                    downloaded_files.append(file)
            return downloaded_files
        if client_utils.is_http_url_like(value):
            downloaded_file = processing_utils.save_url_to_cache(
                value, self.GRADIO_CACHE
            )
            return downloaded_file
        else:
            return value

    def postprocess(self, value: str | list[str] | None) -> ListFiles | None:
        """
        Parameters:
            value: Expects a `str` filepath or URL, or a `list[str]` of filepaths/URLs.
        Returns:
            NeoViewer information as a list of FileData objects.
        """
        if value is None or value == []:
            return None
        if isinstance(value, str):
            value = [value]
        elif not isinstance(value, list):
            raise ValueError(
                "NeoViewer component expects a string or a list of strings as input."
            )
        ms_formats = [".docx", ".doc", ".pptx", ".ppt", ".xls", ".xlsx"]
        if not self.ms_files:
            value = [files for files in value if Path(files).suffix not in ms_formats]
        files = self._download_files(value)
        if is_libreoffice_installed():
            files = [
                convert_file(f, self.GRADIO_CACHE, ms_formats, self.max_size)
                for f in files
            ]
        return ListFiles(
            root=[
                FileData(
                    path=files[f],
                    orig_name=Path(value[f]).name,
                    size=Path(files[f]).stat().st_size,
                )
                for f in range(len(files))
            ]
        )

    def process_example(self, value: str | list | None) -> str:
        if value is None:
            return ""
        else:
            return ", ".join([Path(file).name for file in value])

    def example_payload(self) -> Any:
        return handle_file(
            "https://github.com/gradio-app/gradio/raw/main/test/test_files/sample_file.pdf"
        )

    def example_value(self) -> Any:
        return "https://github.com/gradio-app/gradio/raw/main/test/test_files/sample_file.pdf"
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer

    
    def change(self,
        fn: Callable[..., Any] | None = None,
        inputs: Block | Sequence[Block] | set[Block] | None = None,
        outputs: Block | Sequence[Block] | None = None,
        api_name: str | None | Literal[False] = None,
        scroll_to_output: bool = False,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        queue: bool | None = None,
        batch: bool = False,
        max_batch_size: int = 4,
        preprocess: bool = True,
        postprocess: bool = True,
        cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
        every: Timer | float | None = None,
        trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
        js: str | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        show_api: bool = True,
    
        ) -> Dependency:
        """
        Parameters:
            fn: the function to call when this event is triggered. Often a machine learning model's prediction function. Each parameter of the function corresponds to one input component, and the function should return a single value or a tuple of values, with each element in the tuple corresponding to one output component.
            inputs: list of gradio.components to use as inputs. If the function takes no inputs, this should be an empty list.
            outputs: list of gradio.components to use as outputs. If the function returns no outputs, this should be an empty list.
            api_name: defines how the endpoint appears in the API docs. Can be a string, None, or False. If False, the endpoint will not be exposed in the api docs. If set to None, the endpoint will be exposed in the api docs as an unnamed endpoint, although this behavior will be changed in Gradio 4.0. If set to a string, the endpoint will be exposed in the api docs with the given name.
            scroll_to_output: if True, will scroll to output component on completion
            show_progress: how to show the progress animation while event is running: "full" shows a spinner which covers the output component area as well as a runtime display in the upper right corner, "minimal" only shows the runtime display, "hidden" shows no progress animation at all
            queue: if True, will place the request on the queue, if the queue has been enabled. If False, will not put this event on the queue, even if the queue has been enabled. If None, will use the queue setting of the gradio app.
            batch: if True, then the function should process a batch of inputs, meaning that it should accept a list of input values for each parameter. The lists should be of equal length (and be up to length `max_batch_size`). The function is then *required* to return a tuple of lists (even if there is only 1 output component), with each list in the tuple corresponding to one output component.
            max_batch_size: maximum number of inputs to batch together if this is called from the queue (only relevant if batch=True)
            preprocess: if False, will not run preprocessing of component data before running 'fn' (e.g. leaving it as a base64 string if this method is called with the `Image` component).
            postprocess: if False, will not run postprocessing of component data before returning 'fn' output to the browser.
            cancels: a list of other events to cancel when this listener is triggered. For example, setting cancels=[click_event] will cancel the click_event, where click_event is the return value of another components .click method. Functions that have not yet run (or generators that are iterating) will be cancelled, but functions that are currently running will be allowed to finish.
            every: continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            trigger_mode: if "once" (default for all events except `.change()`) would not allow any submissions while an event is pending. If set to "multiple", unlimited submissions are allowed while pending, and "always_last" (default for `.change()` and `.key_up()` events) would allow a second submission after the pending event is complete.
            js: optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            concurrency_limit: if set, this is the maximum number of this event that can be running simultaneously. Can be set to None to mean no concurrency_limit (any number of this event can be running simultaneously). Set to "default" to use the default concurrency limit (defined by the `default_concurrency_limit` parameter in `Blocks.queue()`, which itself is 1 by default).
            concurrency_id: if set, this is the id of the concurrency group. Events with the same concurrency_id will be limited by the lowest set concurrency_limit.
            show_api: whether to show this event in the "view API" page of the Gradio app, or in the ".view_api()" method of the Gradio clients. Unlike setting api_name to False, setting show_api to False will still allow downstream apps as well as the Clients to use this event. If fn is None, show_api will automatically be set to False.
        
        """
        ...