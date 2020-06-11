import hashlib
import string
import random

# Retorna 5 caracteres randômicos incluindo letras, caracteres especiais e números
def random_key(size=5):
    chars = string.ascii_uppercase + string.digits # chars recebe todas as letras do alfabeto em maiúsculo mais digitos de 0 a 9.
    return ''.join(random.choice(chars) for x in range(size)) # Escolhe randómicamente 5 caracteres de chars e retorna.

# Pega o que foi retornado pela função random_key e adiciona um salt, que é uma informação fornecida pelo usuário, 
# como por ex, o email ou username. Isso dificulta que seja gerada chaves repetidas.
def generate_hash_key(salt, random_str_size=5):
    random_str = random_key(random_str_size) # Recebe os caracteres rândomicos gerado pela função random_key
    text = random_str + salt # Adiciona o salt
    return hashlib.sha224(text.encode('utf-8')).hexdigest() # Codifica a chave gerada randômicamente com criptografia sha224.