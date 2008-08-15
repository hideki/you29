# Create your views here.
from django.http import HttpResponse
def main_page(request):
    output = '''
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<title>you29</title>
<style>
div#logo{
position:absolute;
top:200px;
width:98%;
overflow:hidden;
}
</style>
</head>
<body>
<div id="logo">
<center>
<img id="logo-img" title="you29" src="you29-logo.png"/>
</center>
</div>
</body>
</html>
    '''
    return HttpResponse(output)
