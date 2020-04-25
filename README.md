# NightBotNowPlaying
Program for overlaying NightBot's current song on your stream 

## Authorisation
You need to provide this program with access to NightBot in order to use it. This is done as follows:
1. Go to your NightBot control panel's "Applications" page: https://nightbot.tv/account/applications
2. Click on "New App" (see image) ![](res/applications_page.png)
3. In the "Add an Application" window that comes up, input "NightBotNowPlaying" in the "Name" field and "https://localhost" in the "Redirect URIs" field as shown ![](res/applications_add.png)
4. Click "Submit"
5. Click the orange edit button as shown ![](res/applications_page_2.png)
6. An "Edit Application" window should come up, displaying your Client ID and Client Secret as shown ![](res/applications_edit.png). To show the Client Secret, press the "New Secret" button.
7. Edit the provided "auth.json" and paste in these values. The file would look like this in this case:
```json
{
  "client_id": "abcdef123456789abcdef123456789ab",
  "client_secret": "ba987654321fedcba987654321fedcba"
}
```
Don't share this file or these values with anyone!