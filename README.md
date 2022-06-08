SDF WoT Converter Demo
=================

Demo web app for my [SDF WoT Converter](https://github.com/JKRhb/sdf-wot-converter-py). Realized with Flask.

You can visit try out the converter application at https://sdf-wot-converter.herokuapp.com/.

## Local Deployment

To run the web application locally, you need to have Python (version 3.7 or
above) as well as the required dependencies installed. Using pip, you can
install the requird packages by typing

```sh
pip install -r requirements.txt
```

into a terminal of your choice. You can then use

```sh
flask run
```

to start the web application in production mode or

```sh
./run-server.sh
```

to run it in debug mode.[^1] To access the application, visit
`http://127.0.0.1:5000/` in the web browser of your choice.

[^1]: Note that the script must be marked as executable.
