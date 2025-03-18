<h1>NotebookLM source automation</h1>
<a id="readme-top"></a>

Produced by Nathan Purvis - [Databasyx](https://www.databasyx.com/) co-founder | Data Engineer @ [The Information Lab](https://www.theinformationlab.co.uk/)

<h2>Contact</h2>

[GitHub](https://github.com/DataNath) | [LinkedIn](https://www.linkedin.com/in/nathan-purvis/) | [Twitter](https://x.com/DataNath) | [Alteryx Community](https://community.alteryx.com/t5/user/viewprofilepage/user-id/307299)  
Email: Nathan@databasyx.com

<h2>The problem</h2>

Google's [NotebookLM](https://notebooklm.google.com/) is a tool - powered by Google Gemini - that allows us to quickly generate resources like study guides, briefing documents and audio overviews. To create these assets, we need to make a new notebook and provide sources that the model can then pull from. These sources can be:

- File uploads (PDF, .txt, markdown & audio i.e. mp3)
- Google drive: Docs or Slides
- Links: Website or YouTube
- Paste text: Manually paste in text like meeting notes

However, as pointed out by colleagues and in various Reddit posts, the process for adding link-based sources is incredibly cumbersome; users need to continuously:

- Press 'Add source'
- Select 'Website' or 'YouTube'
- Paste the source URL
- Hit enter/press 'Insert'

This might be fine for a handful of sources but, given you can create notebooks of up to 300 sources, this is less than ideal when scaled.

<h2>The solution</h2>

Given we have a repeated pattern of behaviour in terms of how sources are added, this process is a perfect candidate for browser automation, and that's exactly what is used here. Using [Playwright](https://playwright.dev/python/) - a library created specifically for end-to-end testing and general browser automation tooling - we can easily loop through the steps outlined above to create a new notebook populated with your desired sources.

<h2>How do I use this?</h2>

Follow the steps below to use this yourself!

<h3>1. Clone this repository</h3>

```shell
git clone https://github.com/DataNath/notebooklm_source_automation.git
```

If you're in Documents for example, this will create a new subdirectory here with the project's contents.

<h3>2. Move into the new directory</h3>

```shell
cd notebooklm_source_automation
```

<h3>3. Create a virtual environment (optional)</h3>

```shell
python -m venv .venv
```

This step isn't strictly necessary but is good practice for isolation and keeping projects lean in terms of packages and so on.

<h3>4. Activate your virtual environment</h3>

For Windows users:

```shell
.venv\scripts\activate
```

For Mac users:

```shell
source .venv/bin/activate
```

Again, this isn't strictly necessary i.e. if you're not using a venv as outlined in the step above.

<h3>5. Install required packages</h3>

```shell
pip install -r requirements.txt
```

This will install Playwright and its transitive dependencies.

<h3>6. Install Chromium browser</h3>

```shell
playwright install chromium
```

This installs the [Chromium](https://www.chromium.org/Home/) browser that this project runs on.

<h3>7. Provide your source links</h3>

The project is set up to read a list of up to 300 (NotebookLM's limit) link-based sources from the relevant file within `/sources`. By cloning this repository these will already exist as empty files (other than a header) for you to populate.

>[!WARNING]
>If you create your own file(s) and overwrite the existing, make sure the schema is identical i.e. a single field with a maximum of 300 source rows starting on the second row.

<h3>8. Set your Google login state</h3>

```shell
python set_login_state.py
```

A browser will launch and prompt you to login to Google. Once complete, hit ENTER - the script will terminate and you should see a `state.json` file appear in your directory. This is used to persist authentication and browser session data, saving you from having to log in before every run. Don't worry, this is already in `.gitignore`!

>[!NOTE]
>I haven't tested/checked exact persistence but, for context, only had to re-run the login script once whilst developing the initial release.

<h3>9. Run!</h3>

```shell
python main.py
```

This will prompt you to provide two things in the terminal:

- A source type (currently only 'Website' or 'YouTube')
- A name for the new notebook

<h2>Feedback and/or issues</h2>

Please feel free to leave any feeback or suggestions for improvement. If you spot any issues, let me know and I'll endeavour to address them as soon as I can!

<p align="right">(<a href="#readme-top">Back to top</a>)</p>