# Práctica 1: Web scraping

## Introducción

Este código forma parte de la **PRA1** de la asignatura Tipología y Ciclo de Vida de los Datos, en la que se utilizan técnicas de web scrapping con Python para la obtención  de datos de productos de Amazon y generar un dataset con ellos.

Esta práctica ha sido realizada por **Alicia Contreras** y **Daniel García**.

## Motivación

El principal motivo del desarrollo de esta herramienta es facilitar una búsqueda preliminar de productos online utilizando técnicas de ciencia de datos en una tarea que se suele hacer manualmente. A continuación se describen otras motivaciones para la utilización de esta herramienta:

* Realizar un análisis comparativo de precios de productos con respecto a otras webs de e-commerce
* Realizar un estudio del posicionamiento de productos y del funcionamiento de los buscadores en webs de e-commerce
* Obtención de datasets de imágenes para entrenamiento de algoritmos de clasificación, categorizados con la clase referente a la palabra de búsqueda utilizada por el usuario


También es destacable la oportunidad de utilizar estas herramientas en datos reales.

## Instrucciones de uso

El código permite al usuario generar un dataset a partir de un término de búsqueda de la siguiente manera:

```
python sailor.py "playstation 4"
```

Utilizando como ejemplo el comando superior, se generará un dataset de los resultados de la búsqueda "playstation 4" con los datos definidos en el siguiente apartado **Descripción de los datos**

## Descripción

Los datos que se extraen de los resultados de la búsqueda de Amazon son:

* **product**: Nombre del producto. Tipo: *String*
* **brand**: Marca del producto. Tipo: *String*
* **price**: Precio del producto. Tipo: *Float*
* **discount_percent**: Porcentaje de descuento aplicado. Tipo: *Float*
* **rating**: Valoración del producto sobre 5. Tipo: *Float*
* **n_coments**: Número de comentarios de usuarios. Tipo: *Integer*
* **image**: Url de la imagen principal del producto. Tipo: *String*

## Futuros pasos

Los siguientes pasos a seguir son 

*   La búsqueda de productos en más tiendas online, pudiendo de esta manera comparar productos en función del venededor.
## Licencia

<ins>Attribution-ShareAlike 4.0 International (**CC BY-SA 4.0**):</ins>

El material de este repositorio puede ser compartido, modificado y utilizado para fines comerciales mientras se de el crédito apropiado al autor original. También debe indicarse si se han realizado modificaciones y, en caso afirmativo, dichas modificaciones deben ser publicadas bajo la misma licencia.