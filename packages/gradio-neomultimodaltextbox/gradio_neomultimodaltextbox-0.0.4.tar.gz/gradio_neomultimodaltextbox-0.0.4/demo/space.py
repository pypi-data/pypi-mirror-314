
import gradio as gr
from app import demo as app
import os

_docs = {'NeoMultimodalTextbox': {'description': 'Creates a textarea for users to enter string input or display string output and also allows for the uploading of multimedia files.\n', 'members': {'__init__': {'value': {'type': 'str | dict[str, str | list] | Callable | None', 'default': 'None', 'description': 'Default value to show in NeoMultimodalTextbox. A string value, or a dictionary of the form {"text": "sample text", "files": [{path: "files/file.jpg", orig_name: "file.jpg", url: "http://image_url.jpg", size: 100}]}. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'file_types': {'type': 'list[str] | None', 'default': 'None', 'description': 'List of file extensions or types of files to be uploaded (e.g. [\'image\', \'.json\', \'.mp4\']). "file" allows any file to be uploaded, "image" allows only image files to be uploaded, "audio" allows only audio files to be uploaded, "video" allows only video files to be uploaded, "text" allows only text files to be uploaded.'}, 'file_count': {'type': 'Literal["single", "multiple", "directory"]', 'default': '"single"', 'description': 'if single, allows user to upload one file. If "multiple", user uploads multiple files. If "directory", user uploads all files in selected directory. Return type will be list for each file in case of "multiple" or "directory".'}, 'lines': {'type': 'int', 'default': '1', 'description': 'minimum number of line rows to provide in textarea.'}, 'max_lines': {'type': 'int', 'default': '20', 'description': 'maximum number of line rows to provide in textarea.'}, 'placeholder': {'type': 'str | None', 'default': 'None', 'description': 'placeholder hint to provide behind textarea.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'the label for this component, displayed above the component if `show_label` is `True` and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component corresponds to.'}, 'info': {'type': 'str | None', 'default': 'None', 'description': 'additional component description, appears below the label in smaller font. Supports markdown / HTML syntax.'}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': 'Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.'}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': 'Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.'}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'True', 'description': 'if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'autofocus': {'type': 'bool', 'default': 'False', 'description': 'If True, will focus on the textbox when the page loads. Use this carefully, as it can cause usability issues for sighted and non-sighted users.'}, 'autoscroll': {'type': 'bool', 'default': 'True', 'description': 'If True, will automatically scroll to the bottom of the textbox when the value changes, unless the user scrolls up. If False, will not scroll to the bottom of the textbox when the value changes.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': 'if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.'}, 'text_align': {'type': 'Literal["left", "right"] | None', 'default': 'None', 'description': 'How to align the text in the textbox, can be: "left", "right", or None (default). If None, the alignment is left if `rtl` is False, or right if `rtl` is True. Can only be changed if `type` is "text".'}, 'rtl': {'type': 'bool', 'default': 'False', 'description': 'If True and `type` is "text", sets the direction of the text to right-to-left (cursor appears on the left of the text). Default is False, which renders cursor on the right.'}, 'upload_btn': {'type': 'str | bool | None', 'default': 'True', 'description': None}, 'submit_btn': {'type': 'str | bool | None', 'default': 'True', 'description': 'If False, will not show a submit button. If a string, will use that string as the submit button text.'}, 'stop_btn': {'type': 'str | bool | None', 'default': 'False', 'description': 'If True, will show a stop button (useful for streaming demos). If a string, will use that string as the stop button text.'}, 'loading_message': {'type': 'str', 'default': '"... Loading files ..."', 'description': None}, 'audio_btn': {'type': 'str | bool | None', 'default': 'False', 'description': None}, 'stop_audio_btn': {'type': 'str | bool | None', 'default': 'False', 'description': None}}, 'postprocess': {'value': {'type': 'MultimodalValue | str | None', 'description': 'Expects a {dict} with "text" and "files", both optional. The files array is a list of file paths or URLs.'}}, 'preprocess': {'return': {'type': 'MultimodalValue | None', 'description': 'Passes text value and list of file(s) as a {dict} into the function.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the NeoMultimodalTextbox changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the NeoMultimodalTextbox.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the NeoMultimodalTextbox. Uses event data gradio.SelectData to carry `value` referring to the label of the NeoMultimodalTextbox, and `selected` to refer to state of the NeoMultimodalTextbox. See EventData documentation on how to use this event data'}, 'submit': {'type': None, 'default': None, 'description': 'This listener is triggered when the user presses the Enter key while the NeoMultimodalTextbox is focused.'}, 'focus': {'type': None, 'default': None, 'description': 'This listener is triggered when the NeoMultimodalTextbox is focused.'}, 'blur': {'type': None, 'default': None, 'description': 'This listener is triggered when the NeoMultimodalTextbox is unfocused/blurred.'}, 'stop': {'type': None, 'default': None, 'description': 'This listener is triggered when the user reaches the end of the media playing in the NeoMultimodalTextbox.'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the NeoMultimodalTextbox.'}, 'stream': {'type': None, 'default': None, 'description': 'This listener is triggered when the user streams the NeoMultimodalTextbox.'}}}, '__meta__': {'additional_interfaces': {'MultimodalValue': {'source': 'class MultimodalValue(TypedDict):\n    text: NotRequired[str]\n    files: NotRequired[list[str]]'}}, 'user_fn_refs': {'NeoMultimodalTextbox': ['MultimodalValue']}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_neomultimodaltextbox`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_neomultimodaltextbox/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_neomultimodaltextbox"></a>  
</div>

Python library for Gradio custom component MultimodalTextbox
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_neomultimodaltextbox
```

## Usage

```python
import gradio as gr
from gradio_neomultimodaltextbox import NeoMultimodalTextbox


example = NeoMultimodalTextbox().example_value()


def identity(i):
    return i


with gr.Blocks() as demo:
    box1 = NeoMultimodalTextbox(
        file_count="multiple",
        value={"text": "zouzou", "files": []},
        interactive=True,
    )  # interactive version of your component
    box2 = NeoMultimodalTextbox(
        upload_btn=False, interactive=False, stop_btn=True, audio_btn=True, stop_audio_btn=True
    )  # static version of your component
    box1.submit(fn=identity, inputs=box1, outputs=box2)

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `NeoMultimodalTextbox`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["NeoMultimodalTextbox"]["members"]["__init__"], linkify=['MultimodalValue'])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["NeoMultimodalTextbox"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes text value and list of file(s) as a {dict} into the function.
- **As output:** Should return, expects a {dict} with "text" and "files", both optional. The files array is a list of file paths or URLs.

 ```python
def predict(
    value: MultimodalValue | None
) -> MultimodalValue | str | None:
    return value
```
""", elem_classes=["md-custom", "NeoMultimodalTextbox-user-fn"], header_links=True)




    code_MultimodalValue = gr.Markdown("""
## `MultimodalValue`
```python
class MultimodalValue(TypedDict):
    text: NotRequired[str]
    files: NotRequired[list[str]]
```""", elem_classes=["md-custom", "MultimodalValue"], header_links=True)

    demo.load(None, js=r"""function() {
    const refs = {
            MultimodalValue: [], };
    const user_fn_refs = {
          NeoMultimodalTextbox: ['MultimodalValue'], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
