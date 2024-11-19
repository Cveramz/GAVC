# GAVC

Generación automática de video-clases a partir de lenguaje de marcado (XML)

### Acerca de

Este proyecto es una refactorización del código desarrollado por Cristian Elgueta para su proyecto de título titulado "Creación automática de video-clases a partir de lenguaje de marcado" (2022).

Haz clic [aquí](https://repositorio.usach.cl/discovery/delivery/56USACH_INST:REPOSITORIO/1272594850006116) para ver el trabajo original.

### En qué consiste

El propósito de este proyecto es crear video-clases a partir de un archivo XML con un formato específico, que se procesa y parsea para hacerlo compatible con RevealJS. Esto permite la creación de un archivo HTML que puede visualizarse de manera offline, brindando una experiencia de presentación interactiva y de calidad.

### Motivación para la refactorización

La refactorización de este proyecto se está llevando a cabo debido a varias oportunidades de mejora identificadas en el código original, tales como:

- **Falta de optimización**: El código original no aprovecha prácticas modernas de optimización, lo que reduce su eficiencia.
- **Poca escalabilidad**: La estructura actual dificulta la extensión y el mantenimiento del código, limitando su uso en escenarios más complejos.
- **Excesiva cantidad de líneas de código**: Con aproximadamente 6,000 líneas dedicadas al procesamiento de un solo archivo XML a HTML, existe un margen considerable para reducir la complejidad y mejorar la legibilidad.
- **Documentación insuficiente**: El nuevo enfoque incluirá una documentación detallada para facilitar su comprensión, mantenimiento y contribución de otros desarrolladores.
- **Optimización para entornos de servidor**: Se busca que el nuevo diseño sea más escalable y apto para ser desplegado en servidores.
