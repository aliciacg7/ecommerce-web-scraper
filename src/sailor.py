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
import time
import os
import csv

from pricescraper import ProductsScraper

class Sailor():

    # Esperar carga de un elemento determinado de la pagina
    def esperarCarga(self, webdriver, tipo_elemento, atributo, valor, timeout):

        # Timeout (segundos) para cargar la pagina
        delay = 2

        # XPath del elemento a esperar
        params_busqueda = '//{}[@{}="{}'.format(tipo_elemento, atributo, valor)

        try:
            elemento = WebDriverWait(webdriver, timeout).until(EC.presence_of_element_located((By.XPATH, params_busqueda)))

            return elemento

        except TimeoutException:
            print("Loading took too much time to: \n{}".format(params_busqueda))
            print(webdriver.current_url)
            return False

    
    # Realizar busqueda en Amazon 
    def search_amazon(self, item, n_pages):
        
        pscraper = ProductsScraper()

        # Crear webbrowser y entrar en amazon
        driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
        driver.get('https://www.amazon.es')

        # Aceptar cookies
        driver.find_element(by='xpath', value='//*[@id="sp-cc-accept"]').click()

        # Introducir en barra de búsqueda el parámetro
        search_box = driver.find_element(by="id", value='twotabsearchtextbox').send_keys(item)
        search_button = driver.find_element(by="id", value="nav-search-submit-text").click()

        csv_products = []

        # Esperamos a que cargue la paginación
        pagesInfo = self.esperarCarga(driver, "div", "class", 'a-section a-text-center s-pagination-container"]', 3)
                
        # Comprobamos si existen más paginas además de la principal o el usuario ha introducido
        # un número superior a las páginas existentes
        if pagesInfo != False:
            total_pages = int(BeautifulSoup(pagesInfo.get_attribute('outerHTML'), 'html.parser').find_all(attrs={"class": 's-pagination-item'}, recursive=True)[-2].string)

        else:
            total_pages = 1

        if n_pages > total_pages:
            print(f"Info: Numero de paginas especificado mayor al numero de paginas existentes, se devolverán datos de las paginas existentes: {total_pages}.")
            n_pages = total_pages

        pages_left = n_pages
        
        # Navegar en las primeras n paginas de amazon
        while True:

            # URL de la pagina actual
            currentPage = driver.current_url

            # Scrapping de la pagina actual           
            page_list = pscraper.scrappingProductsListAmz(currentPage, item)
            csv_products += page_list

            # Actualizar el numero de paginas pendientes por revisar
            pages_left = pages_left - 1
            
            # Si no quedan más paginas por explorar, salir del bucle
            if pages_left == 0:
                break

            # Esperar a que cargue el boton de Siguiente pagina
            nextPageButton = self.esperarCarga(driver, "a", "class", 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]', 3)
            nextPageButton.click()

        driver.quit()

        return csv_products


        
    # Realizar busqueda en ECI 
    def search_eci(self, item, n_pages):

        pscraper = ProductsScraper()
        
        # Crear webbrowser y entrar en el corte inglés
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

        csv_products = []
        
        # Comprobamos si existen más paginas además de la principal o el usuario ha introducido
        # un número superior a las páginas existentes
        pagesInfo = self.esperarCarga(driver, "div", "class", 'pagination c12 js-pagination"]', 3)
                
        if pagesInfo != False:
            total_pages = int(BeautifulSoup(pagesInfo.get_attribute('outerHTML'), 'html.parser').div['data-pagination-total'])

        else:
            total_pages = 1
            
        if n_pages > total_pages:
            print(f"Info: Numero de paginas especificado mayor al numero de paginas existentes, se devolverán datos de las paginas existentes: {total_pages}.")
            n_pages = total_pages

        pages_left = n_pages
            
        while True:
            
            # Aceptar de nuevo las cookies para cargar el resto de información
            accept_cookies = self.esperarCarga(driver, "a", "id", 'cookies-agree"]', 3)
            accept_cookies.click()

            time.sleep(2)

            # Obtener lista de los resultados de la busqueda
            raw_results = driver.find_element(by='id', value='products-list').get_attribute('innerHTML')
            
            page_list = pscraper.scrappingProductsListEci(raw_results, item)
            csv_products += page_list
            
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

        driver.quit()

        return csv_products


# Comprobar numero de argumentos
if __name__ == "__main__":
    if(len(sys.argv) == 3):

        searchterm = sys.argv[1]
        searchpages = int(sys.argv[2])

        if (searchpages <= 0):
            print("Numero de paginas a buscar incorrecto")
        
        else:
            buscador = Sailor()

            amz_data = buscador.search_amazon(searchterm, searchpages)
            eci_data = buscador.search_eci(searchterm, searchpages)

            filepath = "data/ecommerce_products_dataset.csv"
            with open(filepath, "a", encoding='utf8') as f:

                writer = csv.writer(f)
                f = open(filepath, "a", encoding='utf8')

                # Si el fichero csv está vacío, creamos la cabecera
                if os.stat(filepath).st_size == 0:
                    writer.writerow(["product","name","brand","price","discount_percent","rating","n_comments","image","express_delivery","ecommerce"])
                    
                writer.writerows(amz_data)
                writer.writerows(eci_data)


    else:
        print("Numero de argumentos incorrecto. Uso del script:")
        print(f'\t> python sailor.py \"TERMINO_DE_BUSQUEDA\" \"NUM_PAGINAS\"')