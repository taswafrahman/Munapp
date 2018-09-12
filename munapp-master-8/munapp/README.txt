How To Run Application (using Linux Terminal and python3)


1) Create a virtual environment using 'python3 -m venv "yourenvnamehere"'

2) Activate your virtual environment using 'source '"yourenvnamehere"/bin/activate'

3) Change directory to the location of the included zip file

4) Unpackage the zip file by running 'pip install app-0.1.tar.gz'

5) Change directory to /app in the installed location of the virtual environment library
	- should be similar to '"yourenvnamehere"/lib/python3.5(orsimilarversion)/site-packages/app'

6) Execute command 'export FLASK_APP=munapp.py'

7) Execute command 'flask run'

8) Navigate to the web application by typing 'localhost:5000' in your favourite web browser


----------------------------------------------------


Deliverables Locations


1. A) 'app/docs/Gantt Chart.pod'
   
B, C, D, E) 'app/docs/Project Management Plan.pdf'


2. A, B) 'app/docs/Requirements.pdf'


3. A, B) 'app/docs/Design Document.pdf'


4. A) See source code
   
   B) Refer to 'app/docs/Design Document.pdf'


5. A) '/app/tests/tests.py'
   
   B) See 'How to run Tests' below


6. A, B) '/app/docs/User Documentation.pdf'


7. all) Included zip file


----------------------------------------------------


How to run Tests (using Linux Terminal and python3)


1) Activate virtual environment

2) Change directory to '../app/tests'

3) Run command 'python3 -m unittest'
----------------------------------------------------
Usernames/Passwords for database
Usernames: Scott, Tim, Brown, Justin
Password (all): comp2005!

The group was created by Brown with Tim and Justin added to the group already. Brown also has preloaded notifications.
