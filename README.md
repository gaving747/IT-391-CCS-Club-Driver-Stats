Everything is ran through app.py, run this command in terminal to install necessary flask parts: pip install Flask mysql-connector-python
once you do that you should be good to run : python app.py
this will launch the application


--New instructions--


To run project, 

Run these commands
1. 'python -m venv .venv'

2. 
+If on linux:
    + source .venv/bin/activate
+If on windows
    +./.venv/Scripts/activate.bat

3. pip install -r requirements.txt

4. In ./.venv/Scripts, 
+ for windows:
    + add lines at bottom of activate.bat:
        + set ADMIN_PASS=<password for admin@* on db>
        + set SECRET_KEY=<anything>
    + add lines inside deactivate.bat:
        + set SECRET_KEY=
        + set ADMIN_PASS=

+ for linux:
    + add lines at bottom of the activate file:
        + export SECRET_KEY='<anything>'
        + export ADMIN_PASS='<password for admin@* on db>'
    + add lines in deactivate function in same file:
        + unset SECRET_KEY
        + unset ADMIN_PASS

5. use command 'Python app.py' to run





