import re
import requests
import json

# Cabeçalho do navegador Mozilla Firefox
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}

def find_google_api_key_in_text(text):
    """Função para encontrar chaves de API do Google no texto."""
    # Regex para encontrar chaves de API do Google (começam com 'AIza')
    api_key_pattern = r'AIza[0-9A-Za-z-_]{35}'
    
    # Encontrar todas as chaves de API no texto
    api_keys = re.findall(api_key_pattern, text)
    
    return api_keys

def check_url_for_api_keys(url):
    """Verifica uma URL em busca de chaves da API do Google."""
    try:
        # Fazer a requisição HTTP com o cabeçalho configurado
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            api_keys = find_google_api_key_in_text(response.text)
            return api_keys
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL {url}: {str(e)}")
        return []

def process_urls_from_file(file_path):
    """Lê as URLs de um arquivo txt e verifica cada uma em busca de chaves de API."""
    with open(file_path, 'r') as file:
        urls = file.readlines()

    results = {}
    
    for url in urls:
        url = url.strip()  # Remover espaços e quebras de linha
        print(f"Verificando URL: {url}...")
        api_keys = check_url_for_api_keys(url)
        
        if api_keys:
            results[url] = api_keys
            print(f"Chaves de API encontradas: {api_keys}")
        else:
            results[url] = []
            print("Nenhuma chave de API encontrada.")

    return results

def save_results_to_json(results, output_file):
    """Salva os resultados em um arquivo JSON."""
    with open(output_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)
    print(f"Resultados salvos em: {output_file}")

if __name__ == "__main__":
    # Caminho para o arquivo de URLs
    urls_file = "urls.txt"  # Substitua pelo caminho do seu arquivo txt de URLs

    # Processar URLs e obter resultados
    results = process_urls_from_file(urls_file)
    
    # Exibir resultados no console
    print("\nResumo das verificações:")
    for url, api_keys in results.items():
        if api_keys:
            print(f"URL: {url} - Chaves encontradas: {api_keys}")
        else:
            print(f"URL: {url} - Nenhuma chave de API encontrada.")
    
    # Perguntar se o usuário quer salvar os resultados em um arquivo JSON
    save_option = input("\nDeseja salvar os resultados em um arquivo JSON? (s/n): ").strip().lower()
    
    if save_option == 's':
        output_file = "resultado_chaves_api.json"  # Arquivo JSON para salvar os resultados
        save_results_to_json(results, output_file)
