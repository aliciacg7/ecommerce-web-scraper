# coding=utf-8
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sys
import json
import time

from pricescraper import ProductsScraper

class Sailor():

    # Esperar carga de un elemento determinado de la pagina
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
            return False
            #sys.exit("Error message")

    
    # Realizar busqueda en Amazon 
    def search_amazon(self, item, n_paginas):

        # Solo puede haber 7 paginas
        if(n_paginas > 6):
            sys.exit("Número máximo de paginas en Amazon: 7")
        
        # Numero de paginas pendientes por buscar
        pages_left = n_paginas

        # Creamos el objeto ProductScraper
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
        f = open("data/amazon_dataset.json", "w+", encoding='utf8')
        json_products = []

        # Navegar en las primeras n paginas de amazon
        while True:

            # URL de la pagina actual
            currentPage = driver.current_url
            #urls.append(currentPage)

            # Scrapping de la pagina actual           
            page_list = pscraper.scrappingProductsListAmz(currentPage)
            
            # Si no quedan más paginas por explorar, salir del bucle
            if pages_left == 0:
                break

            # Esperar a que cargue el boton de Siguiente pagina
            nextPageButton = self.esperarCarga(driver, "a", "class", 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]', 3)
            nextPageButton.click()

            json_products += page_list

        driver.quit()

        # Escribimos los resultados
        f.write(json.dumps(json_products, ensure_ascii=False))
        f.close()


    # Formatear archivo de datos
    def formatearJSON(self):

        # Abrir archivo
        f_read = open("data/amazon_dataset.json", "r", encoding='utf8')
        unparsed = json.load(f_read)
        f_read.close()

        parsed = json.dumps(unparsed, indent=1)

        f_write = open("data/amazon_dataset.json", "w+", encoding='utf8')
        f_write.write(parsed)
        f_write.close()
        
    # Realizar busqueda en ECI 
    def search_eci(self, item, n_pages):

         # Creamos el objeto ProductScraper
        pscraper = ProductsScraper()
        
        # Numero de paginas pendientes por buscar
        pages_left = n_pages
        
        # Crear webbrowser y 
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument(pscraper.getUserAgent()) 
        
        driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)
        driver.get('https://www.elcorteingles.es/')

        # Aceptar cookies
        driver.find_element(by='xpath', value='//*[@id="cookies-agree"]').click()
        driver.delete_all_cookies()

        # Introducir en barra de búsqueda el parámetro
        search_box = driver.find_element(by="id", value='main_search').send_keys(item)

        driver.find_element(by='xpath', value='//*[@aria-label="Buscar"]').click()
        
        # Esperar a que termine la validacion
        time.sleep(10)

        # Abrimos un fichero donde se guardarán los resultados
        f = open("eci_dataset.json", "w+", encoding='utf8')
        json_products = []
        
        # Obtenemos el número de páginas disponibles
        pagesInfo = self.esperarCarga(driver, "div", "class", 'pagination c12 js-pagination"]', 3)
                
        # Si existen más paginas además de la principal
        if pagesInfo != False:
            
            total_pages= int(BeautifulSoup(pagesInfo.get_attribute('outerHTML'), 'html.parser').div['data-pagination-total'])
            
            # Comprobar que el usuario no pide más paginas de las que existen
            if n_pages > total_pages:
                print("Info: Numero de paginas especificado mayor al numero de paginas existentes, se devolverán datos de las paginas existentes.")
                n_pages = total_pages
                
            while True:
                
                # Aceptar de nuevo las cookies para cargar el resto de información
                accept_cookies = self.esperarCarga(driver, "a", "id", 'cookies-agree"]', 3)
                accept_cookies.click()

                time.sleep(2)

                # Obtener lista de los resultados de la busqueda
                raw_results = driver.find_element(by='id', value='products-list').get_attribute('innerHTML')
                
                page_list = pscraper.scrappingProductsListEci(raw_results)
                
                # Actualizar el numero de paginas pendientes por revisar
                pages_left = pages_left - 1
                
                # Si no quedan más paginas por explorar, salir del bucle
                if pages_left == 0:
                    break
                    
                # Eliminar las cookies antes de ir a la siguiente pagina para evitar bloqueos
                driver.delete_all_cookies()
                
                # Esperar a que cargue el boton de Siguiente pagina
                next_page = self.esperarCarga(driver, "a", "class", 'event _pagination_link"]', 3)
                driver.execute_script("arguments[0].click();", next_page)
                
                # Esperar a que termine la validacion
                time.sleep(10)
                
                json_products += page_list  

    driver.quit()

# Comprobar numero de argumentos
if __name__ == "__main__":
    if(len(sys.argv) == 3):
        buscador = Sailor()
        buscador.search_amazon(sys.argv[1], sys.argv[2])
        #buscador.formatearJSON()
        buscador.search_eci(sys.argv[1], sys.argv[2])

    elif (len(sys.argv) == 3 and int(sys.argv[2]) <= 0):
        print("Numero de paginas a buscar incorrecto")
    else:
        print("Numero de argumento incorrecto. Uso del script:")
        print('python sailor.py "{}"'.format("TERMINO_DE_BUSQUEDA"))