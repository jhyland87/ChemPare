import webbrowser
import os

# Define the browser's name and path
browser_name = "brave_browser"
browser_path = "/path/to/chrome"  # Replace with the actual path to your browser executable

# Register the browser
try:
    webbrowser.register(browser_name, None, webbrowser.BackgroundBrowser(browser_path))
except webbrowser.Error as e:
    print(f"Error registering browser: {e}")
    # Fallback to using the default browser or handle the error as needed
    browser_name = None

# Open a URL in the custom browser if it was successfully registered
url_to_open = "https://www.example.com"

if browser_name:
    webbrowser.get(browser_name).open(url_to_open)
else:
    print(f"Could not open {url_to_open} in the custom browser. Opening in default browser instead.")
    webbrowser.open(url_to_open)


# /Applications/Brave Browser.app/Contents/Frameworks/Brave Browser Framework.framework/Versions/133.1.75.178/Helpers/Brave Browser Helper (Renderer).app
# cat /Applications/Brave\ Browser.app/Contents/Frameworks/Brave\ Browser\ Framework.framework/Versions/133.1.75.178/Helpers/Brave\ Browser\ Helper\ \(Renderer\).app/Contents/Info.plist
