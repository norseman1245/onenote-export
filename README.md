# OneNote Export

Export / Backup your Microsoft [OneNote](https://www.onenote.com/) notes to local html files. It'll create a folder structure for each notebook, section and and finally writes the page name as a html file.

```
notebook-name/section-name/page.html
```

You need to create your own application (client_id) to authenticate against OneNote as described [here](https://msdn.microsoft.com/en-us/library/office/dn575426.aspx).

When creating the app you need to *add* ***Web*** as a *Platform* and use the following as the *Redirect URIs*:

```
https://login.live.com/oauth20_desktop.srf
```

# Configuration

Run `auth.py`, enter your *client/application ID*, allow the application to access your account and paste the return *code* from your browser output back into the script. Save the output to `~/.onenote_export.json` for example.

The *code* might be hidden in the browser *Address Bar*.

# Export Notes

Just run `backup.py ~/your/destination/folder` to export all notes as html files.

# Limitation / TODOs

* Attachments are ignored
* SectionGroup are ignored
* It'll delete the backup folder and re-download all notes
* `auth.py` and `backup.py` should be combined