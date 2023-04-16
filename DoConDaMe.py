import sys
import os
import docker
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# |--------------------------------> DOCKER DEPLOYER AND MANAGER MAIN WINDOW
class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # Define the DockerClient connection from the local environment
        self.docker_client = docker.from_env()

        # Set the title for the main window
        self.setWindowTitle("Docker Deployer and Manager")

        # Set the size of the window
        self.resize(800, 600)

        # Center the window on the screen
        screen_size = QDesktopWidget().screenGeometry(-1)
        self.move(int((screen_size.width() - self.width()) / 2), int((screen_size.height() - self.height()) / 2))

        # Set the background color for the main window
        self.setStyleSheet(
            "background-color: #47494d; color: white; font-family: Arial")

        # Create a menu bar
        self.menu_bar = self.menuBar()

        # Create main menus for the menu bar
        self.file_main_menu = self.menu_bar.addMenu("File")
        self.actions_main_menu = self.menu_bar.addMenu("Actions")
        self.help_main_menu = self.menu_bar.addMenu("Help")

        # Create the submenus for the File main menu
        exit_submenu = QMenu("Exit", self)
        self.file_main_menu.addMenu(exit_submenu)

        # Create the submenus for the Actions main menu
        refresh_submenu = QMenu("Refresh", self)
        self.actions_main_menu.addMenu(refresh_submenu)

        # Create the submenus for the Help main menu
        about_submenu = QMenu("About", self)
        self.help_main_menu.addMenu(about_submenu)

        # Add actions to the Exit submenu
        exit_submenu.addAction("Save and Exit")
        exit_submenu.addAction("Exit without Saving")

        # Add actions to the Refresh submenu
        refresh_submenu.addAction("Refresh All")
        refresh_submenu.addAction("Refresh Selected")

        # Add actions to the About submenu
        about_submenu.addAction("About App")
        about_submenu.addAction("About Developer")

        # Create the toolbar
        self.toolbar = QToolBar("My Toolbar")
        # Define the size of the icons
        self.toolbar.setIconSize(QSize(32, 32))
        # Fix the toolbar default to the left side of the main window
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        # Create action buttons for the toolbar
        start = QAction(QIcon("./assets/icons/start.png"), "Start", self)
        stop = QAction(QIcon("./assets/icons/stop.png"), "Stop", self)
        restart = QAction(QIcon("./assets/icons/restart.png"), "Restart", self)
        # Add the buttons to the toolbar
        self.toolbar.addAction(start)
        self.toolbar.addAction(stop)
        self.toolbar.addAction(restart)

        # Create a central widget and layout
        central_widget = QWidget()
        central_layout = QHBoxLayout()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Create tabs
        self.tab_widget = QTabWidget()
        central_layout.addWidget(self.tab_widget)

        # Create a tab for managing containers
        container_tab = QWidget()
        containers_tab_layout = QVBoxLayout()
        container_tab.setLayout(containers_tab_layout)
        self.tab_widget.addTab(container_tab, "Containers")

        # Create widgets for managing containers
        self.containers_table = QTableWidget()
        self.containers_table.setColumnCount(8)
        self.containers_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Status", "Network type", "Network name", "IP address", "Ports", "Default command"])
        self.containers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.containers_table.setSelectionBehavior(QTableWidget.SelectRows)
        containers_tab_layout.addWidget(self.containers_table)

        # Start selected container button
        container_start_button = QPushButton("Start Container")
        container_start_button.setIcon(QIcon("./assets/icons/start.png"))
        container_start_button.setIconSize(QSize(16, 16))
        # Stop selected container button
        container_stop_button = QPushButton("Stop Container")
        container_stop_button.setIcon(QIcon("./assets/icons/stop.png"))
        container_stop_button.setIconSize(QSize(16, 16))
        # Restart selected containerbutton
        container_restart_button = QPushButton("Restart Container")
        container_restart_button.setIcon(QIcon("./assets/icons/restart.png"))
        container_restart_button.setIconSize(QSize(16, 16))
        # Delete selected container button
        container_delete_button = QPushButton("Delete Container")
        container_delete_button.setIcon(QIcon("./assets/icons/delete.png"))
        container_delete_button.setIconSize(QSize(16, 16))
        # View selected container log button
        container_logs_button = QPushButton("View Container Logs")
        container_logs_button.setIcon(QIcon("./assets/icons/deleteAll.png"))
        container_logs_button.setIconSize(QSize(16, 16))
        # Open terminal for selected container button
        container_terminal_open_button = QPushButton("Open Terminal")
        container_terminal_open_button.setIcon(
            QIcon("./assets/icons/openTerminal.png"))
        container_terminal_open_button.setIconSize(QSize(16, 16))
        # Delete all container button
        container_delete_all_button = QPushButton("DELETE ALL")
        container_delete_all_button.setStyleSheet("""
            background-color: red;
            color: white;
            font-weight: bold;
            padding: 4px 8px;
            text-align: center;
        """)
        container_delete_all_button.setIcon(QIcon("./assets/icons/deleteAll.png"))
        container_delete_all_button.setIconSize(QSize(16, 16))

        # Add buttons to the containers layout
        containers_tab_layout.addWidget(self.containers_table)
        containers_tab_layout.addWidget(container_start_button)
        containers_tab_layout.addWidget(container_stop_button)
        containers_tab_layout.addWidget(container_restart_button)
        containers_tab_layout.addWidget(container_delete_button)
        containers_tab_layout.addWidget(container_logs_button)
        containers_tab_layout.addWidget(container_terminal_open_button)
        containers_tab_layout.addWidget(container_delete_all_button)

        # Connect button signals to actions
        container_start_button.clicked.connect(self.start_container)
        container_stop_button.clicked.connect(self.stop_container)
        container_restart_button.clicked.connect(self.restart_container)
        container_logs_button.clicked.connect(self.view_logs)
        container_delete_all_button.clicked.connect(self.delete_all_container)
        self.containers_table.doubleClicked.connect(
            lambda x: self.show_terminal(self.containers_table.currentRow()))

        # Disable editing of the containers table row fields
        self.containers_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # List all existing containers in the table
        self.list_containers()

        # Create a tab for managing images
        self.images_tab = QWidget()
        self.images_tab_layout = QVBoxLayout()
        self.images_tab.setLayout(self.images_tab_layout)
        self.tab_widget.addTab(self.images_tab, "Images")

        # Create widgets for managing images
        self.image_table = QTableWidget()
        self.image_table.setColumnCount(1)
        self.image_table.setHorizontalHeaderLabels(["Name"])
        self.image_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.image_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Retrieve existing Docker images
        images = self.docker_client.images.list()
        for i, image in enumerate(images):
            if image.tags:
                name_item = QTableWidgetItem(image.tags[0])
            else:
                name_item = QTableWidgetItem("No tags")

            self.image_table.insertRow(i)
            self.image_table.setItem(i, 0, name_item)

        # Add buttons for the images layout
        self.images_tab_layout.addWidget(self.image_table)
        self.images_tab_layout.addWidget(container_logs_button)

        # Connect button signals to actions
        self.image_table.doubleClicked.connect(
            lambda x: self.launch_container_creator(self.image_table.currentRow()))

        # Disable editing of the images table row fields
        self.image_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Create a tab for managing networks
        networks_tab = QWidget()
        networks_tab_layout = QVBoxLayout()
        networks_tab.setLayout(networks_tab_layout)
        self.tab_widget.addTab(networks_tab, "Networks")

        # Create and set the status bar of the main window
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Create a QLabel widget for status bar message
        self.message_label = QLabel("Ready")
        self.message_label.setAlignment(Qt.AlignLeft)
        self.status_bar.addWidget(self.message_label)

        # Create a QLabel widget for the clock
        self.clockLabel = QLabel()
        self.clockLabel.setAlignment(Qt.AlignRight)
        self.status_bar.addPermanentWidget(self.clockLabel)

        # Set the font for the clock label
        font = QFont("Arial", 12)
        self.clockLabel.setFont(font)

        # Create a timer that will update the clock every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateClock)
        self.timer.start(1000)

    # Containers Tab Functions

    def start_container(self):
        selected_container = self.containers_table.item(index, 0).text()
        container = self.docker_client.containers.get(container_name)
        container.start()
        self.status_bar().showMessage("Container {} started".format(container_name))
        self.list_containers()

    def stop_container(self):
        container_name = self.container_name.text()
        container = self.docker_client.containers.get(container_name)
        container.stop()
        self.status_bar().showMessage("Container {} stopped".format(container_name))
        self.list_containers()

    def stop_all_containers():
        docker_client = docker.from_env()
        containers = client.containers.list()
        for container in containers:
            self.status_bar().showMessage("Stopping {}".format(container.name))
            container.stop()
            self.status_bar().showMessage("Container {} stopped".format(container.name))

    def restart_container(self):
        if self.container_name != None:
            container_name = self.container_name.text()
            container = self.docker_client.containers.get(container_name)
            container.restart()
            self.status_bar().showMessage("Container {} restarted".format(container_name))
            self.list_containers()

    def delete_container(self):
        pass

    def delete_all_container(self):
        for container in self.docker_client.containers.list(all=True):
            container.remove(force=True)
        self.list_containers()

    def view_logs(self):
        try:
            container = self.docker_client.containers.get(container_name)
        except docker.errors.NotFound:
            self.status_bar().showMessage(
                f"Container '{container_name}' not found")
            return

        logs = container.logs().decode("utf-8")

        logs_text_edit = QTextEdit()
        logs_text_edit.setPlainText(logs)

        logs_scroll_area = QScrollArea()
        logs_scroll_area.setWidget(logs_text_edit)
        logs_scroll_area.setWidgetResizable(True)

        logs_layout = QVBoxLayout()
        logs_layout.addWidget(logs_scroll_area)

        logs_window = QMessageBox()
        logs_window.setWindowTitle(f"{container_name} Logs")
        logs_window.setIcon(QMessageBox.Information)
        logs_window.setText(f"Logs for container '{container_name}':")
        logs_window.setDetailedText(logs)
        logs_window.setSizeGripEnabled(True)
        logs_window.setStandardButtons(QMessageBox.Ok)
        logs_window.setDefaultButton(QMessageBox.Ok)
        logs_window.setLayout(logs_layout)
        logs_window.exec_()

    def list_containers(self):
        # Remove any existing items from the table
        self.containers_table.setRowCount(0)

        # Get the list of all the containers
        containers = self.docker_client.containers.list(all=True)

        # Add each container to the table
        for container in containers:
            id = container.short_id
            name = container.name
            status = container.status

            row_position = self.containers_table.rowCount()
            self.containers_table.insertRow(row_position)

            self.containers_table.setItem(
                row_position, 0, QTableWidgetItem(id))
            self.containers_table.setItem(
                row_position, 1, QTableWidgetItem(name))
            self.containers_table.setItem(
                row_position, 2, QTableWidgetItem(status))
            self.containers_table.setItem(
                row_position, 3, QTableWidgetItem(status))
            self.containers_table.setItem(
                row_position, 4, QTableWidgetItem(status))
            self.containers_table.setItem(
                row_position, 5, QTableWidgetItem(status))

    def show_terminal(self, index):
        # Get the container name from the selected row
        container_name = self.containers_table.item(index, 0).text()
        # Display terminal popup window
        terminal_window = TerminalWindow(container_name)
        terminal_window.exec_()

    # Image Tab Functions

    def list_images(self):
        images = self.docker_client.images.list()
        images_window = QWidget()
        images_window.setWindowTitle("Images")
        images_window.setGeometry(200, 200, 800, 600)
        images_layout = QVBoxLayout()
        images_window.setLayout(images_layout)
        images_scroll_area = QScrollArea()
        images_scroll_area.setWidgetResizable(True)
        images_scroll_widget = QWidget()
        images_scroll_widget_layout = QVBoxLayout()
        images_scroll_widget.setLayout(images_scroll_widget_layout)
        images_scroll_area.setWidget(images_scroll_widget)
        images_layout.addWidget(images_scroll_area)
        for image in images:
            image_label = QLabel(image.tags[0])
            images_scroll_widget_layout.addWidget(image_label)
        images_window.show()

    def create_image(self):
        image_name = self.image_name.text()
        container = self.docker_client.containers.run(
            image_name, name=container_name, detach=True)
        self.docker_client.images.build(path=dockerfile_path, tag=image_name)
        self.status_bar().showMessage("Image {} created".format(image_name))

    def launch_container_creator(self, index):
        selected_image = self.image_table.item(index, 0).text()
        print(selected_image)
        creator = ContainerCreator(self.docker_client, selected_image)
        creator.show()
        creator.exec_()
        # Update container list after new container is created
        self.list_containers()

    # Main Window Functions

    def save_and_exit(self):
        # Save any changes and exit the application
        pass

    def exit_without_save(self):
        pass

    def refresh_all(self):
        pass

    def refresh_selected(self):
        pass

    def about_app(self):
        pass

    def about_dev(self):
        pass

    def updateClock(self):
        # Get the current date and time
        dateTime = QDateTime.currentDateTime()

        # Format the date and time as a string
        dateTimeString = dateTime.toString("dd-MM-yyyy hh:mm:ss")

        # Update the clock label with the current date and time
        self.clockLabel.setText("{}".format(dateTimeString))


# |--------------------------------> CONTAINER CREATOR
class ContainerCreator(QDialog):
    def __init__(self, docker_client, image, parent=None):
        super().__init__(parent)
        self.docker_client = docker_client
        self.image = image

        # Set window properties
        self.setWindowTitle("Create New Container")
        self.setGeometry(200, 200, 400, 300)

        # Create widgets
        name_label = QLabel("Container Name:")
        self.name_edit = QLineEdit()

        # Create button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.create_container)
        button_box.rejected.connect(self.reject)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(button_box)

        # Set layout
        self.setLayout(layout)

    def create_container(self):
        # Get values from widgets
        name = self.name_edit.text()

        # Create container
        container = self.docker_client.containers.run(
            self.image,
            name=name,
            detach=True,
        )

        # Show message box with container ID
        QMessageBox.information(
            self, "Container Created", f"Container {container.name} created successfully!\n The container has the following ID: {container.id}"
        )

        # Close dialog
        self.accept()


# |--------------------------------> TERMINAL WINDOW
class TerminalWindow(QDialog):
    def __init__(self, container_name):
        super().__init__()
        self.container_name = container_name
        self.setWindowTitle(f"Terminal for {container_name}")
        layout = QVBoxLayout(self)
        label = QLabel(
            f"Terminal for {container_name}")
        layout.addWidget(label)
        button = QPushButton("Close")
        layout.addWidget(button)
        button.clicked.connect(self.accept)


# |--------------------------------> INITIALIZATION
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
