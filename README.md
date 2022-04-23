# pixel_cordinate_solver

A repository to hold my pixel image solver source code.

I tried to build code that was primarily robust and readable.

The heart of this is a Flask web service. You can access it in one of three ways. Firstly, you can find it at docker hub: https://hub.docker.com/r/clefspear99/pixel_cordinate_solver Secondly, you can build it yourself. Download all the files and run the following commands "docker build -t clefspear99/pixel_cordinate_solver ." and "docker run -d -p 5000:5000 clefspear99/pixel_cordinate_solver" Finally, you can download the code and run it from Flask without docker.

There is also a folder that contains both a webpage and a python 3 script that sends POST requests to the webpage and displays the response. You can also build your own POST requests with JSON if you are so inclined. Here is the JSON format:

{'corner11': 1.0, 'corner12': 1.0, 'corner21': 1.0, 'corner22': 3.0, 'corner31': 3.0, 'corner32': 1.0, 'corner41': 3.0, 'corner42': 3.0, 'height': 3.0, 'width': 3.0}
