# cliente.py

import grpc
import recomendador_pb2
import recomendador_pb2_grpc
import unicodedata

def remove_acentos(input_str):
    """
    Remove acentos de uma string.
    
    Args:
        input_str (str): String de entrada.
        
    Returns:
        str: String sem acentos.
    """
    nfkd = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def obter_tipo_recomendacao():
    """
    Solicita ao usuário o tipo de recomendação ('filme' ou 'série').
    
    Returns:
        str: Tipo de recomendação normalizado.
    """
    tipos_validos = ['filme', 'serie', 'série']
    while True:
        tipo = input("Você quer recomendação de 'filme' ou 'série'? ").strip().lower()
        tipo_normalizado = remove_acentos(tipo)
        if tipo_normalizado in ['filme', 'serie']:
            # Retorna 'filme' ou 'serie' sem acentos
            return 'filme' if tipo_normalizado == 'filme' else 'serie'
        else:
            print("Tipo inválido. Por favor, digite 'filme' ou 'série'.")

def obter_genero():
    """
    Solicita ao usuário o gênero.
    
    Returns:
        str: Gênero em letras minúsculas.
    """
    while True:
        genero = input("Digite o gênero: ").strip().lower()
        if genero:
            return genero
        else:
            print("Gênero não pode ser vazio. Por favor, tente novamente.")

def obter_ano_lancamento():
    """
    Solicita ao usuário o ano de lançamento.
    
    Returns:
        int: Ano de lançamento.
    """
    import datetime
    ano_atual = datetime.datetime.now().year
    while True:
        ano_str = input("Digite o ano de lançamento: ").strip()
        try:
            ano = int(ano_str)
            if 1900 <= ano <= ano_atual:
                return ano
            else:
                print(f"Ano inválido. Por favor, digite um ano entre 1900 e {ano_atual}.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro para o ano.")

def obter_nota_minima():
    """
    Solicita ao usuário a nota mínima.
    
    Returns:
        float: Nota mínima.
    """
    while True:
        nota_str = input("Digite a nota mínima (0.0 a 10.0): ").strip()
        try:
            nota = float(nota_str)
            if 0.0 <= nota <= 10.0:
                return nota
            else:
                print("Nota inválida. Por favor, digite um valor entre 0.0 e 10.0.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número decimal para a nota.")

def run():
    """
    Executa o cliente gRPC para solicitar recomendações.
    """
    with grpc.insecure_channel('192.168.207.102:50051') as channel:
        stub = recomendador_pb2_grpc.RecomendadorStub(channel)
        
        tipo = obter_tipo_recomendacao()
        genero = obter_genero()
        ano = obter_ano_lancamento()
        nota = obter_nota_minima()
        
        request = recomendador_pb2.Requisicao(tipo=tipo, genero=genero, ano=ano, nota=nota)
        try:
            response = stub.Recomendar(request)
            if response.recomendacoes:
                print(f"\nRecomendações de {tipo} para o gênero '{genero}', ano {ano}, nota mínima {nota}:")
                for idx, recomendacao in enumerate(response.recomendacoes, start=1):
                    print(f"{idx}. {recomendacao}")
            else:
                print("Nenhuma recomendação encontrada com os critérios fornecidos.")
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                print(f"Entrada inválida: {e.details()}")
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                print(f"Não encontrado: {e.details()}")
            else:
                print(f"Ocorreu um erro: {e.details()}")

if __name__ == "__main__":
    run()
