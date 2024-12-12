from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, Select, Static, Button
from textual.containers import ScrollableContainer
from textual.validation import Function
import subprocess
import os
import pwd
import argparse
import requests

username = os.getlogin()

class ReadonlyInput(Input):
    """A readonly Input widget that prevents user interaction."""

    def on_key(self, event) -> None:
        """Block all key inputs."""
        event.stop()  # Prevent any key events from being processed.

    def on_paste(self, event) -> None:
        """Block pasting into the input."""
        event.stop()  # Prevent pasting.

    def on_focus(self, event) -> None:
        """Deselect the input when it gets focus."""
        self.screen.set_focus(None)  # Remove focus to prevent user editing.

    def on_click(self, event) -> None:
        """Prevent clicks from focusing the input."""
        event.stop()  # Block click focus.

class ConfigureInstallerApp(App):
    TITLE = "Configure Installer"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit application"),
    ]

    CSS = """
        Footer {
            text-align: left;
            align: left top; /* Horizontally center content */
        }
        Screen {
            layout: grid;
            grid-size: 1;
            grid-columns: 120; /* Two columns: 40 and 80 units wide */
            align: center top; /* Horizontally center content */
        }
        ScrollableContainer {
            layout: grid;
            grid-size: 2;
            grid-columns: 1fr 2fr; /* Two columns: 40 and 80 units wide */
            grid-rows: 3; /* Two columns: 40 and 80 units wide */
            grid-gutter: 1 1;    /* Gutter space between elements */
            align: center top;
            margin-top: 1;
        }
        Input.readonly {
            color: $text-muted;
        }
        .border-red {
            border: solid transparent;  /* Adds a red border */
        }
        .label-app {
            content-align: left middle; /* Centers the text vertically and horizontally */
            padding: 0 1;                 /* Adds padding */
        }
        #install-btn {
            width: 100%;
            column-span: 2;
            margin: 0 36;
        }

        .invalid-input {
            background: red;  /* Adds a red border */
        }

        .hidden {
            display: none;
        }

        .error-message {
            width: 100%;
            height: 1;
            content-align: left top;
            column-span: 2;
            margin: 0 0 1 42;
            color: red;
        }

    """

    def on_mount(self) -> None:
        self.theme = "gruvbox"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer(show_command_palette=False)
        yield ScrollableContainer(
            Static("Access key:", classes="border-red label-app"),
            Input(placeholder="Enter your access key", id="access-key-input", validators=[Function(self.access_key_validator, "Access key cannot be empty!")]),
            Static("Access key cannot be empty!", id="access-key-error", classes="error-message hidden"),  # Hidden error message
            Static("Install the latest app:", classes="border-red label-app"),
            Select(options=[("Release", "released"), ("Beta", "beta"),], id="app-select", allow_blank=False),
            Static("Install the latest config:", classes="border-red label-app"),
            Select(options=[("Release", "released"), ("Beta", "beta"),], id="config-select", allow_blank=False),
            Static("Install the latest web client:", classes="border-red label-app"),
            Select(options=[("Release", "released"), ("Beta", "beta"),], id="web-client-select", allow_blank=False),
            Static("Username:", classes="border-red label-app"),
            ReadonlyInput(placeholder="Username", value=username, id="username-input"),
            Static("Username cannot be empty!", id ="username-error", classes="error-message hidden"),      # Hidden error message
            Static("Installation Mode:", classes="border-red label-app"),
            Select(options=[("Normal mode", "normal"), ("Maintainance mode", "maintainance")], id="install-mode-select", value="normal", allow_blank=False),
            Button("Install", id="install-btn", variant="success"),
            id="config-installer"
        )

    def access_key_validator(self, x):
        """Validates access key input."""
        # error_widget = 
        if x.strip():
            self.query_one("#access-key-error", Static).add_class("hidden")
            return True
        else:
            self.query_one("#access-key-error", Static).remove_class("hidden")
            return False

    def username_validator(self, x):
        """Validates username input."""
        if x.strip():
            # self.query_one("#username-error").add_class("hidden")
            return True
        else:
            # self.query_one("#username-error").remove_class("hidden")
            return False

    @on(Input.Changed)
    def on_input_change(self, event: Input.Changed) -> None:
        """Handles input change event and checks if the input is not empty."""
        if event.input.id == "#access-key-input":
            error_widget = self.query_one("#access-key-error", Static)
            if not event.validation_result.is_valid:  # Check if input is empty
                error_widget.remove_class("hidden")  # Show error message
            else:
                error_widget.add_class("hidden")  # Hide error message
        elif event.input.id == "#username-input":
            error_widget = self.query_one("#username-error", Static)
            if not event.validation_result.is_valid:  # Check if input is empty
                error_widget.remove_class("hidden")  # Show error message
            else:
                error_widget.add_class("hidden")  # Hide error message

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "install-btn":
            access_token_input_widget = self.query_one("#access-key-input", Input)
            access_token_error_widget = self.query_one("#access-key-error", Static)
            username_input_widget = self.query_one("#username-input", Input)
            username_error_widget = self.query_one("#username-error", Static)

            if not access_token_input_widget.value.strip():  # Check if input is empty
                access_token_error_widget.remove_class("hidden")  # Show error message
                access_token_input_widget.focus()
            elif not username_input_widget.value.strip():  # Check if input is empty
                # username_error_widget.remove_class("hidden")  # Show error message
                username_input_widget.focus()
            else:
                access_token_error_widget.add_class("hidden")  # Hide error message
                # username_error_widget.add_class("hidden")  # Hide error message
                self.exit({
                    "access_key": self.query_one("#access-key-input", Input).value,
                    "app_version": self.query_one("#app-select", Select).value,
                    "config_version": self.query_one("#config-select", Select).value,
                    "web_client_version": self.query_one("#web-client-select", Select).value,
                    "username": self.query_one("#username-input", Input).value,
                    "install_mode": self.query_one("#install-mode-select", Select).value,
                })

    def on_toggle_dark(self) -> None:
        self.dark = not self.dark

    def on_quit(self) -> None:
        self.exit()

def download_file_from_gitlab(access_token:str, project_id:str, src_path: str, dest_path:str, branch_name:str) -> int:
    url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files/{src_path.replace('/', '%2F')}/raw?ref={branch_name}"
    response = requests.get(url, headers={"PRIVATE-TOKEN": access_token})
    if response.status_code == 200:
        try:
            # Save the file locally
            with open(f"{dest_path}", "wb") as file:
                file.write(response.content)
            # print(f"File downloaded successfully as {dest_path}")
            return 0 # Success
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
            return 1 # Error
    else:
        print(f"Invalid Access Token: {access_token}, error code: {response.status_code}")
        return -1 # Invalid Access Token

def run():
    parser = argparse.ArgumentParser(description="My script")
    parser.add_argument("--branch", "-b", type=str, default="install-file-main", help="The branch to use (default: main)")
    parser.add_argument("--cli", action='store_true', help="Run in CLI mode")
    parser.add_argument("--access-token", "-t", default="", help="Input Access Token")
    parser.add_argument("--app-dev", "-ad", action='store_true', help="Run app in dev mode")
    parser.add_argument("--cfg-dev", "-cd", action='store_true', help="Run config in dev mode")
    parser.add_argument("--web-dev", "-wd", action='store_true', help="Run web client in dev mode")
    parser.add_argument("--maintainance", "-m", action='store_true', help="Run installer in maintenance mode")
    args = parser.parse_args()

    if args.cli:
        reply = {
                    "access_key": args.access_token,
                    "app_version": "beta" if args.app_dev else "released",
                    "config_version": "beta" if args.cfg_dev else "released",
                    "web_client_version": "beta" if args.web_dev else "released",
                    "username": username,
                    "install_mode": "maintainance" if args.maintainance else "normal",
                }
    else:
        app = ConfigureInstallerApp()
        reply = app.run()
    if reply:
        # Extract access_key from reply
        ACCESS_TOKEN = reply["access_key"]
        DEPLOY_PRJ_ID = "65233883"
        USERNAME = reply["username"]

        # Get Home directory
        HOME_DIR = pwd.getpwnam(USERNAME).pw_dir

        os.system(f"sudo -u {USERNAME} mkdir -p {HOME_DIR}/Software")

        # Download encrypted SOFTWARE folder
        if download_file_from_gitlab(access_token=ACCESS_TOKEN,
                                     project_id=DEPLOY_PRJ_ID,
                                     src_path="FHVGVIR.txt",
                                     dest_path=f"{HOME_DIR}/FHVGVIR.txt",
                                     branch_name="software-dir-main") == 0:
            subprocess.run(["chown", f"{USERNAME}:{USERNAME}", f"{HOME_DIR}/FHVGVIR.txt"], check=True)

        # Download encrypted webclient folder
        if download_file_from_gitlab(access_token=ACCESS_TOKEN,
                                     project_id=DEPLOY_PRJ_ID,
                                     src_path="GUR_PENML_XRL_VF_ZL_FRPERG_CBFG.txt",
                                     dest_path=f"{HOME_DIR}/Software/GUR_PENML_XRL_VF_ZL_FRPERG_CBFG.txt",
                                     branch_name="web-client-" + ("main"if reply["web_client_version"]=="released" else "dev")) == 0:
            subprocess.run(["chown", f"{USERNAME}:{USERNAME}", f"{HOME_DIR}/Software/GUR_PENML_XRL_VF_ZL_FRPERG_CBFG.txt"], check=True)

        # Download install_ai.sh
        INSTALL_AI_SH_BRANCH = args.branch
        if download_file_from_gitlab(access_token=ACCESS_TOKEN,
                                     project_id=DEPLOY_PRJ_ID,
                                     src_path="install_ai.sh",
                                     dest_path="install_ai.sh",
                                     branch_name=INSTALL_AI_SH_BRANCH) == 0:
            subprocess.run(["chmod", "+x", "install_ai.sh"], check=True)
            subprocess.run(["chown", f"{USERNAME}:{USERNAME}", f"install_ai.sh"], check=True)
            try:
                install_cmd = f"sudo bash ./install_ai.sh -u {reply['username']}"
                install_cmd = install_cmd + " " + ('-m' if reply['install_mode']=='maintainance' else '')
                install_cmd = install_cmd + " " + ('-ad' if reply['app_version']=='beta' else '')
                install_cmd = install_cmd + " " + ('-cd' if reply['config_version']=='beta' else '')

                os.system(install_cmd)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    run()

# python3 -m pip install textual==0.89.1 textual-dev==1.7.0
