## 1. Clone the repo
## 2. Use an access token
When prompted for a password, use an access token with write permissions.
> Note: Generate one from your settings: https://huggingface.co/settings/tokens
```
git clone https://huggingface.co/spaces/yrohitha/dataops-mcp
```

### Make sure the hf CLI is installed
```
curl -LsSf https://hf.co/cli/install.sh | bash
```

## 3. Download the Space
```
hf download yrohitha/dataops-mcp --repo-type=space
```

Create your gradio app.py file:
```python
import gradio as gr

def greet(name):
    return "Hello " + name + "!!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
```

## 4. Commit and Push

```
git add app.py
git commit -m "Add application file"
git push
```
Hint Alternatively, you can create the app.py file directly in your browser.
Finally, your Space should be running on this page after a few moments!

## 5. Dependencies

You can add a `requirements.txt` file at the root of the repository to specify Python dependencies

If needed, you can also add a `packages.txt` file at the root of the repository to specify Debian dependencies.

The gradio package is pre-installed and its version is set in the sdk_version field in the README.md file.

## Personalize your Space

Make your Space stand out by customizing its emoji, colors, and description by editing metadata in its `README.md` file.

## Documentation

Read the full documentation for gradio Spaces here.