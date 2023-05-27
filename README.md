# Qube Project

Operating system - Ubuntu 20.04 LTS

Prerequisite : AWS CLI v2 have to be installed and configured. Reference link - https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html


### Steps to run this project :

1. Clone project
2. Install venv and activate it
3. Install python packages from requirements.txt
4. Run the script.py file


Virtual environments enable us to have an isolated space on our server for Python projects. Install venv which is part of the standard python3 library. To install venv :

1. Open terminal (press ctrl + alt + T).
2. Change directory to Project.

    ```cd Project```

3. Install venv.

    ```sudo apt install -y python3-venv```

4. Venv is installed now. Now we will create a virtual environment.
5. Type "python3 -m venv name" and press enter. You can give the name of your virtual environment in place of "name". Suppose you want name of your virtual environment as qube_venv. So you have to type "python3 -m venv qube_venv".

    ```python3 -m venv qube_venv```

6. Final step is to activate your virtual environment. 

    ```source qube_venv/bin/activate```

7. Now, your terminal will be prefixed with the name of your virtual environment.


### To install the python packages using requirements.txt.

```pip3 install -r requirements.txt```

### Now you are ready to run the script.py file.

```python3 script.py```