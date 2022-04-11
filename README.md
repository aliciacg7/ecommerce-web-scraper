# Práctica 1: Web scraping

## Introducción

Este código forma parte de la **PRA1** de la asignatura Tipología y Ciclo de Vida de los Datos, en la que se utilizan técnicas de web scrapping en Python con BeatifulSoup y Selenium para la obtención  de datos de productos de Amazon y generar un dataset con ellos. 

Esta práctica ha sido realizada por **Alicia Contreras** y **Daniel García**.

## Motivación

El principal motivo del desarrollo de esta herramienta es facilitar una búsqueda preliminar de productos online utilizando técnicas de ciencia de datos en una tarea que se suele hacer manualmente. A continuación se describen otras motivaciones para la utilización de esta herramienta:

* Realizar un análisis comparativo de precios de productos con respecto a otras webs de e-commerce
* Realizar un estudio del posicionamiento de productos y del funcionamiento de los buscadores en webs de e-commerce
* Obtención de datasets de imágenes para entrenamiento de algoritmos de clasificación, categorizados con la clase referente a la palabra de búsqueda utilizada por el usuario

También es destacable la oportunidad de utilizar estas herramientas en datos reales.

## Instrucciones de uso

El código permite al usuario generar un dataset de productos a partir de un término de búsqueda.

Para ejecutar el script es necesario instalar la siguientes bibliotecas:

```
pip install selenium
pip install requests
pip install beautifulsoup4
```

Seguidamente, procederemos a ejecutar el script de la siguiente manera:

```
python src/sailor.py "sudadera negra"
```

Utilizando como ejemplo el comando superior, se generará un dataset de los resultados de la búsqueda "sudadera negra" con los datos definidos en el siguiente apartado.


## Descripción de los datos

Los datos que se extraen de los resultados de la búsqueda de Amazon son:

* **product**: Témino de búsqueda. Se corresponde con el producto buscado. Tipo: *String*
* **name**: Nombre del producto. Tipo: *String*
* **brand**: Marca del producto. Tipo: *String*
* **price**: Precio del producto. Tipo: *Float*
* **discount_percent**: Porcentaje de descuento aplicado. Tipo: *Float*
* **rating**: Valoración del producto sobre 5. Tipo: *Float*
* **n_comments**: Número de comentarios de usuarios. Tipo: *Integer*
* **image**: Url de la imagen principal del producto. Tipo: *String*
* **express_delivery**: Si el producto tiene opción de envío express. Tipo: *Boolean*
* **ecommerce**: Código de la tienda a la que pertenece el producto. Tipo: *String*


## Futuros pasos

Los siguientes pasos a seguir son 

*   La búsqueda de productos en más tiendas online, pudiendo de esta manera comparar productos en función del venededor.
## Licencia

<ins>Attribution-ShareAlike 4.0 International (**CC BY-SA 4.0**):</ins>

El material de este repositorio puede ser compartido, modificado y utilizado para fines comerciales mientras se de el crédito apropiado al autor original. También debe indicarse si se han realizado modificaciones y, en caso afirmativo, dichas modificaciones deben ser publicadas bajo la misma licencia.