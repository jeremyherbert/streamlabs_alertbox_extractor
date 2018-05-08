# streamlabs_alertbox_extractor
extracts information from a running streamlabs alertbox


## Instructions

To run this script, you will need three things:

- a streamlabs alertbox URL: (example) https://streamlabs.com/alert-box/v3/SOMERANDOMTEXT1234
- a twitch API key, which you can get from [here](https://dev.twitch.tv/dashboard/apps). In the `OAuth Redirect URL` box, just enter `http://localhost`: (example) abcdefghijk123456
- your twitch login name: (example) jer_emy

You can run this script on windows without installing python by downloading the executable from the releases tab above. Otherwise, using a modern version of python with `asyncio`, run `pip install -r requirements.txt` to install the dependencies.

## Windows instructions (with executable)

1. Create a new text file and save it as `run.bat` in the same folder as the executable.
2. In the file, paste the following text:

```
streamlabs_youtube_extractor.exe C:\Users\Jeremy\something "https://streamlabs.com/alert-box/v3/SOMERANDOMTEXT1234" abcdefghijk123456 jer_emy
pause
```

3. Replace `C:\Users\Jeremy\something` with the path to the folder you would like to save text files into
4. Replace the example alertbox URL, twitch API key and twitch login name with your own
5. Save and double click the `run.bat` file.

# Addendum

shoutouts to simpleflips
