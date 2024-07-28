# NightBotNowPlaying
Program for overlaying NightBot's current song on your stream.

This works with NightBot and so works with Twitch, YouTube and Mixer.
It also works with any streaming software which allows for Text to be read from a file and so works with OBS, XSplit, etc.

## Downloading/Installing
`cd` into the directory where you want to put the program, then:
```
git clone https://github.com/pixelchai/NightBotNowPlaying.git
cd NightBotNowPlaying
python3 -m pip install -r requirements.txt
```


## Authorisation
You need to provide this program with access to NightBot in order to use it. This is done as follows:
1. Go to your NightBot control panel's "Applications" page: https://nightbot.tv/account/applications
2. Click on "New App" ([screenshot](res/applications_page.png))
3. In the "Add an Application" window that comes up, input "NightBotNowPlaying" in the "Name" field and `http://localhost:5771` in the "Redirect URIs" field. Make sure the URL is exactly as shown, there should be no trailing slash, and it should start with `http`!
4. Click "Submit"
5. Click the orange edit button ([screenshot](res/applications_page_2.png))
6. An "Edit Application" window should come up, displaying your Client ID and Client Secret ([screenshot](res/applications_edit.png)). To show the Client Secret, press the "New Secret" button.
7. Edit the provided "auth.json" and paste in these values. The file might look like something like this:
```json
{
  "client_id": "abcdef123456789abcdef123456789ab",
  "client_secret": "ba987654321fedcba987654321fedcba"
}
```
Don't share this file or these values with anyone!

## Usage
```
python3 nowplaying.py
```

If authorisation is required, the program will automatically open up a browser. Simply click "Allow". You won't need to do this very often (usually only once the first time you use this script, then once every month after that).

<!-- Outdated instructions for manual code entering: -->
<!-- 1. In the browser window, log in to NightBot (if not already), and click "Allow"
2. You should be redirected. The page will likely be unable to be reached. The code requested by the program can be found in the URL bar. It should look something like this: `https://localhost:5771/?code=abcdef123456789abcdef123456789ab`.
3. Copy and paste the code from the URL into the program. In this example, the required code would be `abcdef123456789abcdef123456789ab`. -->

### Usage in OBS
1. Make sure the program is running - it should print "Authorized!" in the console if it was able to start successfully
2. Create a Text source
3. In the source's properties, check "Read from file"
4. For the "Text file" field, browse to the folder where you installed the program, and select `np.txt`


## Configuration
The program allows for configuration through the `config.json` file.

The configurable options are detailed below:
| Option       | Default   | Description                                                                                                                                                                                        |
|--------------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| text         | "{title}" | The text to be outputted<br> - this value supports bracketed variable substitution                                                                                                                 |
| path         | "np.txt"  | Where the output file should be. (NB: the containing directory must exist)                                                                                                                         |
| update_delay | 1         | How many seconds to wait between checks for updates to the current song.<br>Note: don't set this too low - you don't want to overload NightBot's servers!                                                        |
| fancy_limit  | false     | Limits the number of updates such that the program updates less <br>during the middle of the song but more at the endings and beginnings.<br>Enable this if you are likely to not skip songs often |

The variables which may be used in the text string are detailed below:
| Option                 | Example                            | Description                                      |
|------------------------|------------------------------------|--------------------------------------------------|
| title                  | Alex Skrindo - Jumbo [NCS Release] | Title of the current song                        |
| artist                 | NoCopyrightSounds                  | Artist (uploader) of the current song            |
| url                    | https://youtu.be/v4Za061pQac       | Url of the current song                          |
| duration               | 191                                | Total duration, in seconds, of the current song  |
| requester              | test_user_1                        | Username of the user who requested that song     |
| requester.display_name | test_user_1                        | Display name of the user who requested that song |


## Common Issues
#### 'Missing required OAuth2 parameter(s)'

Please ensure you have edited the provided `auth.json` file as in the instructions above.

#### 'Unknown error occurred'
This error message may be shown on the NightBot website when clicking the "Allow" button in the steps above. If so, please ensure that the 'Redirect URI' field when adding an application to NightBot is exactly `http://localhost:5771`, and with no trailing backslash. 
You can update/check the 'Redirect URI' field by visiting https://nightbot.tv/account/applications and clicking the orange edit button ([screenshot](res/applications_page_2.png)).
See discussion of this issue here: [#3](https://github.com/pixelchai/NightBotNowPlaying/issues/3).
