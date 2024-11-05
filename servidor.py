# servidor.py

import os
from concurrent import futures
import grpc
import recomendador_pb2
import recomendador_pb2_grpc
import requests

# Substitua pela sua chave da API TMDB
TMDB_API_KEY = '88a14d3ae04de73aab3f3e8f1695c3b3'

if not TMDB_API_KEY:
    raise ValueError("A chave da API TMDB não foi definida no ambiente.")

def buscar_recomendacoes(tipo, genero, ano, nota):
    """
    Busca recomendações de filmes ou séries na API TMDB com base nos critérios fornecidos.
    
    Args:
        tipo (str): 'movie' ou 'tv'.
        genero (str): Gênero solicitado.
        ano (int): Ano de lançamento.
        nota (float): Nota mínima.
        
    Returns:
        list: Lista de títulos recomendados.
    """
    try:
        # Obter o ID do gênero no TMDB
        url_generos = f'https://api.themoviedb.org/3/genre/{tipo}/list?api_key={TMDB_API_KEY}&language=pt-BR'
        response_generos = requests.get(url_generos)
        response_generos.raise_for_status()
        
        generos = response_generos.json().get('genres', [])
        genero_id = next((g['id'] for g in generos if g['name'].lower() == genero.lower()), None)
        
        if not genero_id:
            raise ValueError("Gênero não encontrado.")
    
        # Definir intervalo de nota
        nota_inferior = nota
        nota_superior = min(nota + 0.99, 10.0)  # Limita a nota superior a 10.0
    
        # Montar a URL para buscar filmes ou séries com os critérios especificados
        url_recomendacoes = (
            f'https://api.themoviedb.org/3/discover/{tipo}?api_key={TMDB_API_KEY}&language=pt-BR'
            f'&with_genres={genero_id}&primary_release_year={ano}&vote_average.gte={nota_inferior}&vote_average.lte={nota_superior}'
        )
        
        response_recomendacoes = requests.get(url_recomendacoes)
        response_recomendacoes.raise_for_status()
        
        recomendacoes = response_recomendacoes.json().get('results', [])
        return [item['title'] if tipo == 'movie' else item['name'] for item in recomendacoes[:5]]  # Retorna os 5 primeiros títulos encontrados
    except requests.HTTPError as http_err:
        raise ValueError(f"Erro na requisição à API TMDB: {http_err}")
    except Exception as err:
        raise ValueError(f"Ocorreu um erro: {err}")

class RecomendadorServicer(recomendador_pb2_grpc.RecomendadorServicer):
    """
    Implementação do serviço Recomendador definido no .proto.
    """
    def Recomendar(self, request, context):
        """
        Retorna recomendações com base nos critérios fornecidos.
        
        Args:
            request (Requisicao): Requisição com os critérios de recomendação.
            context (grpc.ServicerContext): Contexto da chamada RPC.
            
        Returns:
            Resposta: Resposta com a lista de recomendações.
        """
        tipo = 'movie' if request.tipo.lower() == 'filme' else 'tv'
        genero = request.genero.lower()
        ano = request.ano
        nota = request.nota
        try:
            recomendacoes = buscar_recomendacoes(tipo, genero, ano, nota)
            return recomendador_pb2.Resposta(recomendacoes=recomendacoes)
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return recomendador_pb2.Resposta()

def serve():
    """
    Configura e inicia o servidor gRPC.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recomendador_pb2_grpc.add_RecomendadorServicer_to_server(RecomendadorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC em execução na porta 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()