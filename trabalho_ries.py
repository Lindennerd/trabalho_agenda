import sqlite3
import settings
import os
import smtplib
import sys

def trata_filtro():
    opt = raw_input("""
        Escolha o filtro desejado:

        1 filtro por nome
        2 por sobrenome
        3 filtro por endereco
        4 filtro por email

    """)

    if opt == '1':
        return listar('nome')
    elif opt == '2':
        return listar('sobrenome')
    elif opt == '3':
        return listar('endereco')
    elif opt == '4':
        return listar('email')
    else
        return None

def enviar_email():
    con = sqlite3.connect(os.path.join(settings.local, 'agenda.db'))
    c = con.cursor()
    c.execute("select email from agenda")
    emails = c.fetchall()

    print 'Escolha o email:'
    for email in emails:
        for item in email:
            print str(emails.index(email)) + ' - '+item

    opt = raw_input()

    sender = 'lindennerd@gmail.com'
    receivers = [emails[int(opt)], 'lindennerd@gmail.com', 'aline_saquet@terra.com.br']

    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test

    This is a test e-mail message.
    """

    smtpObj = smtplib.SMTP('smtp.gmail.com')
    smtpObj.sendmail(sender, receivers, message)         
    print "Successfully sent email"
    

def editar(email):
    con = sqlite3.connect(os.path.join(settings.local, 'agenda.db'))
    c = con.cursor()
    c.execute("select * from agenda where email = '"+email+"'")
    contato = c.fetchone()
    exib =''
    for cont in contato:
        exib = cont + '\n' + exib  
    print 'Seu contato: \n' + exib

    novo_nome = ''
    if opt == '1':
        novo_nome = raw_input('digite o novo nome: ')
        c.execute("update agenda set nome_contato = '"+novo_nome+"' where email = '"+email+"'")
    elif opt == '2':
        novo_nome = raw_input('digite o novo sobrenome: ')
        c.execute("update agenda set sobrenome = '"+novo_nome+"' where email = '"+email+"'")
    elif opt == '3':
        novo_nome = raw_input('digite o novo endereco: ')
        c.execute("update agenda set endereco = '"+novo_nome+"' where email = '"+email+"'")
    elif opt == '4':
        novo_nome = raw_input('digite o novo telefone: ')
        c.execute("update agenda set telefone = '"+novo_nome+"' where email = '"+email+"'")
    elif opt == '5':
        novo_nome = raw_input('digite o novo email: ')
        c.execute("update agenda set email = '"+novo_nome+"' where email = '"+email+"'")
    else:
        return 'Opcao Invalida'
        
    con.commit()
    con.close()
    

def excluir(email):
    con = sqlite3.connect(os.path.join(settings.local, 'agenda.db'))
    c = con.cursor()
    c.execute("delete from agenda where email = '"+email+"'")
    try :
        con.commit()
        return 'Contato excluido com sucesso'
    except e:
        return e
    con.close()

def add_contato():
    nome = raw_input('Nome do contato: ')
    sobrenome = raw_input('Sobrenome do contato: ')
    endereco = raw_input('endereco do contato: ')
    telefone = raw_input('Telefone do contato: ')
    email = raw_input('email do contato: ')

    con = sqlite3.connect(os.path.join(settings.local, 'agenda.db'))
    c = con.cursor()
    c.execute("INSERT INTO agenda (nome_contato, sobrenome, endereco, telefon, email) VALUES ('"+nome+"', '"+sobrenome+"', \
               '"+endereco+"', '"+telefone+"', '"+email+"')")
    try :
        con.commit()
        return 'Contato Inserido com sucesso'
    except e:
        return e
    con.close()

def ler_arquivo(arquivo):
    folder = os.path.join(os.path.dirname('__file__'), 'banco')
    op = open(os.path.join(folder, arquivo))
    return op.read().replace(';', '')

def busca_contatos(filtro):
    con = sqlite3.connect(os.path.join(settings.local, 'agenda.db'))
    c = con.cursor()

    if filtro == None:
        c.execute(ler_arquivo('busca_contatos.txt'))
    elif filtro == 'nome':
        pass
            
    return c.fetchall()    
    con.close()
    
def cria_banco():
    con = sqlite3.connect(os.path.join(settings.local, 'agenda.db'))
    c = con.cursor()
    c.execute(ler_arquivo('create_database.txt'))
    con.commit()
    con.close()
    
def listar(filtro):
    cria_banco()
    contatos = busca_contatos(filtro)
    
    if len(contatos) == 0:
        return 'Nenhum contato encontrado'
    
    exib = ''
    for contato in contatos:
            exib = 'email: ' + str(contato[4]) + '\n' + exib
            exib = 'telefone: ' + str(contato[3]) + '\n' + exib
            exib = 'endereco: ' + str(contato[2]) + '\n' + exib
            exib = 'sobrenome: ' + str(contato[1]) + '\n' + exib
            exib = 'nome: ' + str(contato[0]) + '\n' + exib
            exib = '---------------------- ' + '\n' + exib
    
    return exib


def trata_escolha(opt):
    if opt == '1':
        os.system('cls')
        filt = raw_input('filtrar listagem?(s/n)')
        if filt == 's':
            return trata_filtro()
        return listar('')
    elif opt == '2':
        os.system('cls')
        return add_contato()
    elif opt == '3':
        os.system('cls')
        email = raw_input('digite o email do contato a excluir: ')
        return excluir(email)
    elif opt == '4':
        os.system('cls')
        email = raw_input('digite o email do contato a editar: ')
        return editar(email)
    elif opt == '5':
        os.system('cls')
        return enviar_email()
    else:
        return 'sair'


def main():
    opt = raw_input("""

        Escolha a opcao desejada:
        1 - Listar contatos
        2 - Adicionar contato
        3 - excluir contato
        4 - editar
        5 - enviar email
        Qualquer tecla - sair

        """)
    return trata_escolha(opt)


if __name__ == '__main__':
    opt = ''
    while opt != 'sair':
        print main()
