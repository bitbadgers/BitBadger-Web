#*************************************************************#
        Bit Badger project installation and coding
#*************************************************************#

1.  Install pip
        Open your Terminal if on linux and CMD if on windows
        Run the following commands
        
        Linux
        ================
        sudo apt install python3-pip

        # You need to have python3 installed

        Windows (why?)
        ===============
        1. Search for get-pip.py online // Make sure its pip3
        2. Open your CMD and navigate to the folder containing the get-pip.py i.e the downloaded file
        3. run: 
                py get-pip.py

        alternatively you will be forced to use easy-install i.e its an alternative for
        pir

2.  Install python django 
        run the following on your terminal/CMD
        
        Linux
        ===========
        pip3 install django

        Windows
        ===========
        pip install django 
        
        or

        easy-install django // depending on what will work for you

3.  Running the web app
        Open the folder BitBadger and inside open the terminal / CMD

        run
        
        Linux
        ===========
        python3 manage.py runserver

        Windows
        ===========
        py manage.py runserver

4.  On Browser
        Open your browser (mainly  Mozilla or Chrome to avoid localhost issues)
        type:
            localhost:8000 

            or the address in the terminal after running runserver

5. Accsessing Admin
        Incase you want to use the admin Dashboard use the following credentials:
            username: BitWeb-Devs
            password: BitBadger@2020

    

    +++++++++++++++++++++++++++++ Happy coding ++++++++++++++++++++++++++++++++++++
            

        
        
