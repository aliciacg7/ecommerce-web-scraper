# Práctica 1: Web scraping

## Introducción

Este código forma parte de la **PRA1** de la asignatura Tipología y Ciclo de Vida de los Datos, en la que se utilizan técnicas de web scrapping con Python para la obtención  de datos de productos de Amazon y generar un dataset con ellos.

Esta práctica ha sido realizada por **Alicia Contreras** y **Daniel García**.

## Motivación

El principal motivo del desarrollo de esta herramienta es facilitar una búsqueda preliminar de productos online utilizando técnicas de ciencia de datos en una tarea que se suele hacer manualmente. 

También es destacable la oportunidad de utilizar estas herramientas en datos reales.

## Instrucciones de uso

El código permite al usuario generar un dataset a partir de un término de búsqueda de la siguiente manera:

```
python sailor.py "playstation 4"
```

Utilizando como ejemplo el comando superior, se generará un dataset de los resultados de la búsqueda "playstation 4" con los datos definidos en el siguiente apartado **Descripción de los datos**

## Descripción

Los datos que se extraen de los resultados de la búsqueda de Amazon son:

* **products**: nombre del producto
* **price**: precio del producto
* **rating**: valoración del producto
* **n_coments**: número de comentarios de usuarios
* **image**: url de la imagen principal del producto

## Futuros pasos

Los siguientes pasos a seguir son 

*   La búsqueda de productos en más tiendas online, pudiendo de esta manera comparar productos en función del venededor.
## Licencia

<ins>Attribution-ShareAlike 4.0 International (**CC BY-SA 4.0**):</ins>

El material de este repositorio puede ser compartido, modificado y utilizado para fines comerciales mientras se de el crédito apropiado al autor original. También debe indicarse si se han realizado modificaciones y, en caso afirmativo, dichas modificaciones deben ser publicadas bajo la misma licencia.