1. Install Python 3.
3. Install postgresql.
4. Create a database with default user.
5. Open cmd in project folder and type this command "pip install -r requirement.txt" . 
6. Open settings.py file in finalyear folder. 
	on line 87 and 89 add database name password.
	on line 148 and 149 add email details but first turn on google less secure app for that email.
7. Open cmd in project folder and types these commands.
	"python manage.py make migrations"
	"python manage.py migrate"
	"python manage.py runserver_plus --cert-file cert.pem --key-file key.pem"
8. You can use django admin to add admin for website.