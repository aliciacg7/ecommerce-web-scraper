from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import json

from pricescraper import ProductsScraper

class Sailor():

    def esperarCarga(self, webdriver, tipo_elemento, atributo, valor, timeout):

        # Timeout (segundos) para cargar la pagina
        delay = 2

        # XPath del elemento a esperar
        params_busqueda = '//{}[@{}="{}'.format(tipo_elemento, atributo, valor)

        try:
            # Esperar a que cargue el boton de la siguiente pagina
            elemento = WebDriverWait(webdriver, timeout).until(EC.presence_of_element_located((By.XPATH, params_busqueda)))

            return elemento

        except TimeoutException:
            print("Loading took too much time to: \n{}".format(params_busqueda))
            print(webdriver.current_url)
            sys.exit("Error message")

    def search_amazon(self, item, n_paginas):

        # Solo puede haber 7 paginas
        if(n_paginas-1 > 6):
            sys.exit("Número máximo de paginas en Amazon: 7")

        # URLs con las paginas de Amazon
        #urls = []
        
        pscraper = ProductsScraper()

        # Crear webbrowser y entrar en amazon
        driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
        driver.get('https://www.amazon.es')

        # Aceptar cookies
        driver.find_element(by='xpath', value='//*[@id="sp-cc-accept"]').click()

        # Introducir en barra de búsqueda el parámetro
        search_box = driver.find_element(by="id", value='twotabsearchtextbox').send_keys(item)
        search_button = driver.find_element(by="id", value="nav-search-submit-text").click()

        # Abrimos un fichero donde se guardarán los resultados
        f = open("data/amazon_dataset.json", "w", encoding='utf8')
        json_products = []

        # Navegar en las primeras n paginas de amazon
        for y in range(0,n_paginas-1):

            # URL de la pagina actual
            currentPage = driver.current_url
            #urls.append(currentPage)

            # Scrapping de la pagina actual           
            page_list = pscraper.scrappingProductsList(driver.current_url)
            
            # Esperar a que cargue el boton de Siguiente pagina
            nextPageButton = self.esperarCarga(driver, "a", "class", 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]', 3)
            nextPageButton.click()

            json_products += page_list

        driver.quit()

        # Escribimos los resultados
        f.write(json.dumps(json_products, ensure_ascii=False))
        f.close()
        
        #return urls

# Comprobar numero de argumentos
if __name__ == "__main__":
    if(len(sys.argv) == 2):
        buscador = Sailor()
        buscador.search_amazon(sys.argv[1], 7)
    else:
        print("Numero de argumento incorrecto. Uso del script:")
        print('python sailor.py "{}"'.format("TERMINO_DE_BUSQUEDA"))