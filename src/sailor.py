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
            print("Page is ready!")

            return elemento

        except TimeoutException:
            print("Loading took too much time to: \n{}".format(params_busqueda))
            print(webdriver.current_url)
            sys.exit("Error message")

    def search_amazon(self, item):
        pscraper = ProductsScraper()

        # Crear webbrowser y entrar en amazon
        driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
        driver.get('https://www.amazon.es')

        # Introducir en barra de búsqueda el parámetro
        search_box = driver.find_element(by="id", value='twotabsearchtextbox').send_keys(item)
        search_button = driver.find_element(by="id", value="nav-search-submit-text").click()

        # Navegar en las primeras 5 paginas de amazon
        for y in range(0,2):

            # URL de la pagina actual
            currentPage = driver.current_url

            # Abrir los primeros 5 primeros elementos
            for i in range(2,20):
                try:

                    # Esperamos a los resultados de la búsqueda se carguen
                    self.esperarCarga(driver, "div", "cel_widget_id", 'MAIN-SEARCH_RESULTS-'+str(i)+'"]/div/div/div/div/div', 8).click()

                    # Esperamos a que carguen los detalles del producto
                    #esperarCarga(driver, "div", "id", 'productDescription"]', 3)

                    # URL del producto
                    print(driver.current_url)
                    pscraper.scrappingProduct(driver.current_url)
                    print("_________")

                    # Volver a la pagina principal
                    driver.get(currentPage)

                except NoSuchElementException as e:
                    print(e)
                    driver.quit()
                print("Producto {} finalizado".format(i))

                # Esperar a que cargue el boton de Siguiente pagina
            nextPageButton = self.esperarCarga(driver, "a", "class", 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]', 3)

            nextPageButton.click()

        driver.quit()

# Buscar cualquier termino
buscador = Sailor()
buscador.search_amazon('pantalones')
