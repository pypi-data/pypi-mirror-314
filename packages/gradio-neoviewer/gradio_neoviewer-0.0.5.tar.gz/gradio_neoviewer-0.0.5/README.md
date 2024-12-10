---
tags: [gradio-custom-component, File]
title: gradio_neoviewer
short_description: A gradio custom component
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_neoviewer`
<a href="https://pypi.org/project/gradio_neoviewer/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_neoviewer"></a>  

A custom viewer for Gradio that allows users to visualize different types of files

## Installation

```bash
pip install gradio_neoviewer
```

## Usage

```python
import gradio as gr
from gradio_neoviewer import NeoViewer


def set_interface():
    print("Setting interface")
    view_with_ms = NeoViewer(
        value=[
            "./demo/data/Le_Petit_Chaperon_Rouge_Modifie.docx",
            "./demo/data/mermaid_graph-2.html",
            "./demo/data/graphique_couts_annuels.png",
            "./demo/data/Le_Petit_Chaperon_Rouge.zouzou",
            "./demo/data/viewer.py",
        ],
        elem_classes=["visualisation"],
        index_of_file_to_show=0,
        height=300,
        visible=True,
        ms_files=True,
    )

    view_without_ms = NeoViewer(
        value=[
            "./demo/data/Le_Petit_Chaperon_Rouge_Modifie.docx",
            "./demo/data/mermaid_graph-2.html",
            "./demo/data/graphique_couts_annuels.png",
            "./demo/data/Le_Petit_Chaperon_Rouge.zouzou",
        ],
        elem_classes=["visualisation"],
        index_of_file_to_show=1,
        height=300,
        visible=True,
        ms_files=False,
    )
    empty_view1 = view_with_ms
    empty_view2 = view_without_ms
    return view_with_ms, view_without_ms, empty_view1, empty_view2


with gr.Blocks() as demo:
    with gr.Row():
        view_with_ms = NeoViewer(visible=False)
        view_without_ms = NeoViewer(visible=False)
        empty_view1 = NeoViewer(visible=False)
        empty_view2 = NeoViewer(visible=False)
    demo.load(
        set_interface,
        outputs=[view_with_ms, view_without_ms, empty_view1, empty_view2],
    ).then(
        fn=lambda: (
            NeoViewer(visible=False, value=None, elem_id="empty1"),
            NeoViewer(visible=False, value=[], elem_id="empty2"),
        ),
        outputs=[empty_view1, empty_view2],
    )

if __name__ == "__main__":
    demo.launch()

```

## `NeoViewer`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
str | list[str] | Callable | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Default file(s) to display, given as a str file path or URL, or a list of str file paths / URLs. If callable, the function will be called whenever the app loads to set the initial value of the component.</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">the label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
Timer | float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.</td>
</tr>

<tr>
<td align="left"><code>inputs</code></td>
<td align="left" style="width: 25%;">

```python
Component | Sequence[Component] | set[Component] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will display label.</td>
</tr>

<tr>
<td align="left"><code>container</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, will place the component in a container - providing some extra padding around the border.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.</td>
</tr>

<tr>
<td align="left"><code>height</code></td>
<td align="left" style="width: 25%;">

```python
int | float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The default height of the file component when no files have been uploaded, or the maximum height of the file component when files are present. Specified in pixels if a number is passed, or in CSS units if a string is passed. If more files are uploaded than can fit in the height, a scrollbar will appear.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will allow users to upload a file; if False, can only be used to display files. If not provided, this is inferred based on whether the component is used as an input or output.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.</td>
</tr>

<tr>
<td align="left"><code>key</code></td>
<td align="left" style="width: 25%;">

```python
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.</td>
</tr>

<tr>
<td align="left"><code>index_of_file_to_show</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>0</code></td>
<td align="left">int = 0, # index of file to show in case of multiple files</td>
</tr>

<tr>
<td align="left"><code>max_size</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>5000000</code></td>
<td align="left">maximum size of file to show in bytes</td>
</tr>

<tr>
<td align="left"><code>max_pages</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>100</code></td>
<td align="left">maximum number of pages of file to show</td>
</tr>

<tr>
<td align="left"><code>ms_files</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">if True, will convert MS files to PDF for display, but it is a long process. Unactive if libre_office is False</td>
</tr>

<tr>
<td align="left"><code>libre_office</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">if True, means that LibreOffice is installed and can be used to convert MS files to PDF</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` | Triggered when the value of the NeoViewer changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, passes the file as a `str`object, or a list of `str`.
- **As input:** Should return, expects a `str` filepath or URL, or a `list[str]` of filepaths/URLs.

 ```python
 def predict(
     value: str | list[str] | None
 ) -> str | list[str] | None:
     return value
 ```
 
