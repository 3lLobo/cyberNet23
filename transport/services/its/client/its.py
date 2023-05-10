#!/usr/bin/env python3
import requests
from textual.app import App, ComposeResult
from textual.widgets import Header, Button, Label, Input, ListView, ListItem, DataTable, Footer
from textual.screen import Screen
from textual.containers import Grid
from textual.binding import Binding

from rich.text import Text

servers = []

#generates the error screen when credentials are incorrect
class ErrorScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label(("The credentials you used is unable to give the data you are looking for.").upper(), id="wrong-cred"),
            Button("TRY AGAIN", variant="warning", id="try-again"),
            id="grid3"
        )
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "try-again":
            self.app.pop_screen()

#generates a screen of data either with location or without based on credentials given
class Data(Screen):
    def __init__(self, server):
        self.error = True
        headers = {}
        try:
            if server["username"]=="admin" and server["password"]:
                response = requests.post(f'http://{server["hostname"]}:4000/authenticate',{"username": server["username"],"password":server["password"]})
                token = response.text
                headers = {"authorization": "Bearer " + token}
            response = requests.get(f'http://{server["hostname"]}:4000/location_records', headers = headers)
            if response.status_code == 200:
                self.error = False
            location_records = [("VIN", "Type", "Timestamp", "GPS Lat", "GPS Lng")]
            for i in response.json():
                location_records.append((i["vehicle"]["vin"], i["vehicle"]['type'], i['timestamp'], i.get("location", {}).get("lat", "-"), i.get("location", {}).get("lng", "-")))
            self.location_records = location_records
        except:
            self.error = True
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        if self.error:
            yield ErrorScreen()
        else:
            yield Grid (
                DataTable(),
                Button("DISCONNECT", variant="error", id="disconnect"),
                id="grid2"
            )
    def on_mount(self) -> None:
        if self.error:
            return
        table = self.query_one(DataTable)
        table.add_columns(*self.location_records[0])
        for row in self.location_records[1:]:
            styled_row = [
                Text(str(cell), style="italic #03AC13", justify="right") for cell in row
            ]
            table.add_row(*styled_row)

#generates a screen where you can create your own server and add credentials
class AddServer(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Add Server:", id="title1"),
            Input(placeholder="Hostname",id="hostname"),
            Label("Optional:", id="italics"),
            Input(placeholder="Username", id="username"),
            Input(placeholder="Password", id="password"),
            Button("ADD SERVER", variant="success", id="server-added"),
            Button("CANCEL", variant="error", id="cancel"),
            id="grid1"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "server-added":
            servers.append({"hostname": self.query_one("#hostname").value, "username": self.query_one("#username").value, "password": self.query_one("#password").value})
            self.app.pop_screen()
            self.app.query_one("#servers").append(
                ListItem(
                    Label("Hostname: "+ self.query_one("#hostname").value+"\nUsername: "+ self.query_one("#username").value, id= "list-label"),
                    Button("CONNECT", id=f"connect_{len(servers)-1}", variant= "success", classes="connect"),
                    id = f"list-item_{len(servers)-1}"
                ),
            )
        elif event.button.id == "cancel":
            self.app.pop_screen()
            
#parent app where everything connected too
class Intelligent_Traffic_System(App):
    CSS_PATH = "its.css"
    TITLE = "INTELLIGENT TRAFFIC SYSTEM"
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield ListView(id="servers")
        yield Button("ADD SERVER", id="add-server",variant="primary")
        yield Footer()
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!", event.item.id)
        server_id = int(event.item.id.lstrip("list-item_"))
        self.push_screen(Data(servers[server_id]))


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-server":
            self.push_screen(AddServer())
        elif event.button.id.startswith("connect_"):
            server_id = int(event.button.id.lstrip("connect_"))
            self.push_screen(Data(servers[server_id]))
        elif event.button.id == "disconnect":
            self.app.pop_screen()

app = Intelligent_Traffic_System()

if __name__ == "__main__":
    app.run()
