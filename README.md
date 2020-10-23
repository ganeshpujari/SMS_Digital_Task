# **Setup**

required python>=3.5

pip install -r requirements.txt

# **To Start the server**

Run "_python manage.py runserver_" under "\SMS_Digital\metallics_optimizer" directory

# **Authentication**

_We are suporting both Session and Basic Authentication_

Username: _admin_
Password: _admin_

# **Database** 

I am using sqlite3 So adding database file in repo.
So no need to run any migration script. If you do any changes in database schema then run
python manage.py makemigrations and python manage.py migrate commands.

Note:- _initial migration scripts added under migrations directory_


#**API ENDPOINTS**

1. Get all chemical elements

[
![Get all chemical elements](https://user-images.githubusercontent.com/12044530/97005240-cff3ca00-155b-11eb-8934-154ae6fd35ef.PNG)
](url)




2. Get a commodity by id

![2  Get a commodity by id](https://user-images.githubusercontent.com/12044530/97006316-50ff9100-155d-11eb-9a58-b72cd1ac3d41.PNG)



3. Update commodity by id

![3  Update commodity by id](https://user-images.githubusercontent.com/12044530/97006372-64aaf780-155d-11eb-9332-bfddd2229c34.PNG)




4. Add chemical concentration

![4 Add consentarion](https://user-images.githubusercontent.com/12044530/97006422-7b514e80-155d-11eb-9bd8-7295786d5ff8.PNG)




5. Remove chemical concentration

![5 delete consentration](https://user-images.githubusercontent.com/12044530/97006571-b0f63780-155d-11eb-81fa-5a4579f9d622.PNG)







