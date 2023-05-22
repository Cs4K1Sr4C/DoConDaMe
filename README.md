<h1>🐋 All-In-One Docker - Containers / Containers' Terminals / Networks / Images - Manager in a PyQt5 environment </h1>
<p>This is a Python3-based application with a PyQt5 GUI implementation which allows you to manage Docker containers, networks and images. It provides a simple and intuitive graphical user interface (GUI) for management; and it is designed to be easy to use. 🖥️</p>

## 🚨 !THIS VERSION IS ONLY A LIMITED VERSION! 🚨<br />
### 🔑 NEEDS ADMINISTRATIVE (SUDO) PERMISSION TO RUN 🔑<br />
### 🛠️ PRE-REQUIREMENT

- 🐋 already pulled Docker images

<h2>🎁 Features in the full version</h2>
<p>The current features of the application include:</p><br />

- 🔍 Listing all containers, including their ID, name, status, network and its type, IP, ports and the default running command in a table
- 🖱️ Doubleclick on the selected table row opens a terminal to the container in a pop-up window
- 🖼️ Ability to open more container terminal windows
- 🚀 Starting, stopping and removing the selected container via buttons
- 🆕 Create and run new containers based on existing images
- 🛠️ Moveable toolbar with icons
- 📢 Statusbar for sending feedbacks to the user
- 📝 In the container creation pop-up window the user can configure some parameters of the container
- 📂 If the container's image allows it then ability to copy files between the host and container via a graphical file explorer
- 📜 Support for run custom commands on the selected container

<p>🔜 In the close future I would like to extend with the following features:</p>
- 🔍 Search and filter functionality to easily find containers based on their name, ID, or status<br />
- 🖼️ Pre-configured images for deploying containers<br />
- ⏸️ Option to pause and resume containers

<h2>💻 Installation</h2>
<h3>For Linux users:</h3>
<p>To use this application, you will need to have Docker, Python3 and PyQt5 installed on your system. You can install them
    using the following commands:</p>
<pre><code>sudo apt-get install python3 docker.io docker && pip3 install pyqt5</code></pre>
<p>You will also need to have Docker installed and running on your system.</p>
<p>Or you can use the <strong>DoConDaMe_Install.sh</strong> file for the automatized installation; to use it you can use the following command in your terminal:</p>
<pre><code>chmod +x ./DoConDaMe_Install.sh && sudo ./DoConDaMe_Install.sh</code></pre>
<p>After the installation you can start the application; simply run the following command in your terminal:</p>
<pre><code>chmod +x ./DoConDaMe.sh && sudo ./DoConDaMe.sh</code></pre>
<p>or with the</p>
<pre><code>python3 ./DoConDaMe.py</code></pre><br />

<h2>Screenshots</h2>
<img src="https://user-images.githubusercontent.com/126985144/222996030-d0aedfa2-cf4e-41dd-b95e-001d55f8e963.png" />
