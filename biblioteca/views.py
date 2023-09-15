from django.shortcuts import get_object_or_404, render
from .models import Category, Product
import pyrebase
from firebase_admin import auth



config={ 
  "apiKey": "AIzaSyAVAPeQliHCivo8zXS_PXUC6NDk8Hy8Xc4",
  "authDomain": "banco-f1481.firebaseapp.com",
  "databaseURL": "https://banco-f1481-default-rtdb.firebaseio.com",
  "projectId": "banco-f1481",
  "storageBucket": "banco-f1481.appspot.com",
  "messagingSenderId": "821656580161",
  "appId": "1:821656580161:web:a05aad4383bd89fe8996c0",
  "measurementId": "G-EWT1PBLZ9X",
  "serviceAccount": "bancoCertificate.json"
}

"""*<--------------------------------Banco de bados------------------------------->*"""



firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()


'''*<---------------------------------Teste de amostra-------------------------------->*'''
 
def home(request): 
    abi = database.child('Data').child('abi').get().val() 
    nome = database.child('Data').child('nome').get().val()

#*<-----------------------------------Todos dos livros------------------------------------>*

    all_livros = database.child("livros").get()
    livros_list = []
    for livro in all_livros.each():
        livro_data = {
            "value": livro.val()
        }
        livros_list.append(livro_data)

    return render(request, "biblioteca/home.html", {"abi": abi, "nome": nome, "all_livros": livros_list})

'''data = {"titulo": "Heartstopper",
            "autor": "Alice Oseman"}
    firebase.database() .child("livros").push(data)'''

'''*<-----------------------detalhes do livro/para reservar-------------------->*'''

def detalhe_livro(request, slug):
    # Retrieve the livro by its slug from Firebase
    all_livros = database.child("livros").get()
    livro = None
    for livro_data in all_livros.each():
        if livro_data.val().get('slug') == slug:
            livro = livro_data.val()
            break

    if livro is None:
        # Handle the case when the livro with the given slug is not found
        return render(request, 'error_template.html', {'error_message': 'Livro not found'})

    # Render the livro details using the 'biblioteca/detalhes.html' template
    return render(request, 'biblioteca/detalhes.html', {'livro': livro})

'''-------------------------------------------PESQUISA-----------------------------------------------'''
def procurar(request):
    if request.method == "POST":
        searched = request.POST['searched'] 
        filtro = request.POST['filtro']
        
        if filtro == 'titulo':
            results = database.child('livros').order_by_child('titulo').start_at(searched).end_at(searched + '\uf8ff').get()
        #elif filtro == 'genero':
            #results = database.child('livros').order_by_child('genero').start_at(searched).end_at(searched + '\uf8ff').get()
        elif filtro == 'autor':
            results = database.child('livros').order_by_child('autor').start_at(searched).end_at(searched + '\uf8ff').get()
        elif filtro == 'data':
            results = database.child('livros').order_by_child('data_publicacao').start_at(searched).end_at(searched + '\uf8ff').get()
        else:
            # Caso não haja um filtro válido selecionado, retorne todos os livros
            results = database.child('livros').get()

        livros = []
        if results:
            for livro in results.each():
                livro_data = livro.val()
                # Adicione a lógica para formatar os dados do Firebase conforme necessário
                livros.append(livro_data)

        return render(request, 'biblioteca/procurar.html', {'searched': searched, 'livros': livros, 'filtro': filtro})
    else:
        return render(request, 'biblioteca/procurar.html', {})


'''*<---------------------------------Sistema de LOGIN e LOGOUT-------------------------------->*'''
def entrar(request):
    return render(request, 'biblioteca/entrar.html')

def postentrar(request):
    email=request.POST.get('email')
    senha = request.POST.get("senha")
    nome = database.child('users').child('a').child('detalhes').child('nome').get().val()
    try:
        user = authe.sign_in_with_email_and_password(email,senha)
    except:
        message = "credencial errada"
        return render(request,"biblioteca/entrar.html",{"msg":message})
    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request, "biblioteca/entrou.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request,'biblioteca/entrar.html')

'''*<---------------------------------Sistema de Cadastro-------------------------------->*'''

def cadastro(request):
   return render(request,"biblioteca/cadastro.html")

def postcadastro(request):
    nome=request.POST.get('nome')
    email=request.POST.get('email')
    senha=request.POST.get('senha')
    try:
        user=authe.create_user_with_email_and_password(email,senha)
        uid = user['localId']
        data={"nome":nome,"status":"1"}
        database.child("users").child(uid).child("detalhes").set(data)
    except:
        mensagem="Não foi possivel cirar uma conta"
        return render(request,"biblioteca/cadastro.html",{"messg":mensagem})
    
    return render(request,"biblioteca/entrar.html")



'''*<---------------------------------CATALOGO(DESATUALIZADO)-------------------------------->*'''


'''def generos(request):
    return {
        'generos': Genero.objects.all()
    }'''

def categories(request):
    return {
        'categories': Category.objects.all()
    }


def all_products(request):
    products = Product.products.all()
    return render(request, 'biblioteca/home.html', {'products': products})


def lista_categoria(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'biblioteca/category.html', {'category': category, 'products': products})
'''
def lista_genero(request, genero_slug=None):
    genero = get_object_or_404(Genero, slug=genero_slug)
    products = Product.objects.filter(genero=genero)
    return render(request, 'biblioteca/genero.html', {'genero': genero, 'products': products})
'''

'''def detalhe_livro(request, slug):
    product = get_object_or_404(Product, slug=slug, no_estoque=True)
    return render(request, 'biblioteca/detalhes.html', {'product': product})'''


'''*<---------------------------------PESQUISA-------------------------------->*'''
'''
def procurar(request):
    if request.method == "POST":
        searched = request.POST['searched'] 
        filtro = request.POST['filtro']
        
        if filtro == 'titulo':
            livros = Product.objects.filter(titulo__icontains=searched)
        elif filtro == 'genero':
            livros = Product.objects.filter(autor__icontains=searched)
        elif filtro == 'autor':
            livros = Product.objects.filter(editora__icontains=searched)
        elif filtro == 'data':
            livros = Product.objects.filter(data_publicacao__icontains=searched)
        else:
            # Caso não haja um filtro válido selecionado, retorne todos os livros
            livros = Product.objects.all()
            
        return render(request, 'biblioteca/procurar.html', {'searched': searched, 'livros': livros, 'filtro': filtro})
    else:
        return render(request, 'biblioteca/procurar.html', {})'''
