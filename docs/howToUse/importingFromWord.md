## DOCX to Markdown script

Use `scripts/docx_to_markdown.py` to convert a DOCX lab guide into markdown files.

### What it does

- Reads one `.docx` input file
- Extracts all embedded images into `docs/assets/` (or a custom assets directory)
- Splits each Heading 1/Heading 2 that starts with `Lab` into its own markdown file in `docs/`
- Writes all non-lab content to `docs/non-lab.md`


!!! Important
    ### Preparing your file
    - The script will split your labs into separate files For heading levels 1 and 2 of your document if the text starts with the word **Lab**.
    - If you no not have the word **Lab** in the headings, the contents of that section will go into the **non-lab.md** file.
        - You can append the word **Lab** by using an advanced find and replace in Word to target the heading level and with the replace textbox containing `Lab #: ^&` for numbered labs then you can update the lab numbers
    - If you do not want your level 2 headings to be separate files, demote them to level 3 or lower.
        - If you plan to demote your level 2 heading so that you do not create separate files, make sure that you first demote level 3 to level 4 starting with the lowest level first to preserve your formatting.



!!! Note 
    ### Usage
    - Open up a new terminal in the directory of this repo and if you are not already in the virtual environment, use the appropriate commands for your operating system listed below.
    === "If you are on a PC"
        > In your terminal enter the following commands:
        >
        > <copy>venv\Scripts\activate.ps1</copy>


    === "If you are on a Mac"
        > In your terminal enter the following commands:
        >
        > <copy>source venv/bin/activate</copy>
    - Locate the docx file you want to convert to Markdown, copy the path the the file into the box below and click the **Update Lab Guide** button.  
    <form id="info">
        <label for="path">Path to File:</label>
        <input type="text" id="path" name="path">
        <button onclick="setValues()">Update Lab Guide</button>
        </form>
    - Copy this command into your terminal:   
    <copy>python scripts/docx_to_markdown.py <w class="path">path/to/guide.docx</w></copy>

Optional arguments:

- `--docs-dir` (default: `docs`)
- `--assets-dir` (default: `<docs-dir>/assets`)


### After your files are created
- Add your files to the mkdocs.yml file in the **nav** section and save the file.
- If you are not currently running mkdocs, start the server
- Review your formatting and make any necessary adjustments 