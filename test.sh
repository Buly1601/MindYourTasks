#NORMAL LINKS***************************************************
echo "GET NORMAL TEST *****************************************"
response=$(curl -s -o /dev/null -w "%{http_code}" https://mindyourtask.tech/)
if [ ${response} = 200 ]; then
        echo "success"
else
        exit -1
fi
echo "POST NORMAL TEST *****************************************"
response=$(curl -X POST -s -o /dev/null -w "%{http_code}" https://mindyourtask.tech/)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 405 ]; then
        echo "error can´t do POST"
else
        exit -1
fi
#ABOUT LINKS***************************************************
echo "GET ABOUT TEST *****************************************"
response=$(curl -s -o /dev/null -w "%{http_code}" https://mindyourtask.tech/about)
if [ ${response} = 200 ]; then
        echo "success"
else
        exit -1
fi
echo "POST ABOUT TEST *****************************************"
response=$(curl -X POST -s -o /dev/null -w "%{http_code}" https://mindyourtask.tech/about)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 405 ]; then
        echo "error can´t do POST"
else
        exit -1
fi
#EXPERIENCE LINKS**********************************************
echo "GET EXPERIENCE TEST *****************************************"
response=$(curl -s -o /dev/null -w "%{http_code}" https://mindyourtask.tech/experience)
if [ ${response} = 200 ]; then
        echo "success"
else
        exit -1
fi
echo "POST EXPERIENCE TEST *****************************************"
response=$(curl -X POST -s -o /dev/null -w "%{http_code}" https://mindyourtask.tech/experience)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 405 ]; then
        echo "error can´t do POST"
else
        exit -1
fi
#PROJECTS LINKS************************************************
echo "GET PROJECTS TEST *****************************************"
response=$(curl -s -o /dev/null -w "%{http_code}" https://mindyourtask.tech/projects)
if [ ${response} = 200 ]; then
        echo "success"
else
        exit -1
fi
echo "POST PROJECTS TEST *****************************************"
response=$(curl -X POST -s -o /dev/null -w "%{http_code}" https://mindyourtask.tech/projects)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 405 ]; then
        echo "error can´t do POST"
else
        exit -1
fi

#REGISTER LINKS*************************************************
echo "GET REGISTER TEST *****************************************"
response=$(curl -s -o /dev/null -w "%{http_code}" https://mindyourtask.tech/register)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 501 ]; then
        echo "error page not implemented"
elif [ ${response} = 418 ]; then
        echo "error wrong data"
else
        exit -1
fi

echo "POST REGISTER TEST WITH USERNAME AND PASSWORD*****************************************"
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -d "username=gi.gamez&password=12345" https://mindyourtask.tech/register)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 501 ]; then
        echo "error page not implemented"
elif [ ${response} = 418 ]; then
        echo "repeated "
else
        exit -1
fi
#LOGIN LINKS*****************************************************
echo "GET LOGIN TEST *****************************************"
response=$(curl -s -o /dev/null -w "%{http_code}" https://mindyourtask.tech/login)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 501 ]; then
        echo "error page not implemented"
elif [ ${response} = 418 ]; then
        echo "error wrong data "
else
        exit -1
fi
echo "POST LOGIN TEST WITH USERNAME AND PASSWORD *****************************************"
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -d "username=gi.gamez&password=12345" https://mindyourtask.tech/login)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 501 ]; then
        echo "error page not implemented"
elif [ ${response} = 418 ]; then
        curl -X POST -d "username=gi.gamez&password=12345" https://mindyourtask.tech/login
        echo "error wrong data "
else
        exit -1
fi
echo "POST LOGIN WITH WRONG PASSWORD *****************************************"
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -d "username=gi.gamez&password=123" https://mindyourtask.tech/login)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 501 ]; then
        echo "error page not implemented"
elif [ ${response} = 418 ]; then
        curl -X POST -d "username=gi.gamez&password=123" https://mindyourtask.tech/login
else
        exit -1
fi
exit 0