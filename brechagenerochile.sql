-- Brecha_Tit
DROP TABLE IF EXISTS `trabajo-analitica-339815.Datos_brechas.BrechaTIT`;
CREATE TABLE trabajo-analitica-339815.Datos_brechas.BrechaTIT(Anio INT NOT NULL, Region
STRING NOT NULL, Codigo_region INT, Tituladas INT NOT NULL, Hombres_titulados INT NOT NULL,
Mujeres_tituladas INT NOT NULL , Porc_hombres_t FLOAT64 NOT NULL , Porc_mujeres_t FLOAT64
NOT NULL, Brecha_genero FLOAT64 NOT NULL);

-- Brecha_Nac
DROP TABLE IF EXISTS `trabajo-analitica-339815.Datos_brechas.BrechaNAC`;
CREATE TABLE trabajo-analitica-339815.Datos_brechas.BrechaNAC(Anio INT NOT NULL, Region
STRING NOT NULL, Codigo_region INT NOT NULL, Tramos_edad STRING NOT NULL,
Nacidos_padres INT, Nacidos_madres INT NOT NULL, Porc_nacidos_padres FLOAT64,
Porc_nacidos_madres FLOAT64 NOT NULL, Brecha_genero FLOAT64);

-- Brecha_Des
DROP TABLE IF EXISTS trabajo-analitica-339815.Datos_brechas.BrechaDES;
CREATE TABLE trabajo-analitica-339815.Datos_brechas.BrechaDES(Anio INT NOT NULL, Trimestre
STRING NOT NULL, Region STRING NOT NULL, Codigo_region INT NOT NULL, Notat STRING,
Tasa_desocupacion FLOAT64 NOT NULL, Notah STRING , Tasa_des_hombres FLOAT64 NOT NULL ,
Notam STRING, Tasa_des_mujeres FLOAT64 NOT NULL, Brecha_genero FLOAT64 NOT NULL);

-- 1.¿Cuál es la variación porcentual para la brecha de género de títulos profesionales entre el año
-- 2010 y 2019 para cada región?
DROP TABLE IF EXISTS `trabajo-analitica-339815.Datos_brechas.Brecha2010`;
CREATE TABLE `trabajo-analitica-339815.Datos_brechas.Brecha2010` AS
(SELECT Anio, Region, Brecha_genero FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Tit`
WHERE Anio = 2010);
DROP TABLE IF EXISTS `trabajo-analitica-339815.Datos_brechas.Brecha2019`;
CREATE TABLE `trabajo-analitica-339815.Datos_brechas.Brecha2019` AS
(SELECT Anio, Region, Brecha_genero FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Tit`
WHERE Anio = 2019);
SELECT t2.Region, CONCAT(ROUND(((t2.Brecha_genero -
t1.Brecha_genero)*100)/t1.Brecha_genero,2),'','%') AS Variacion_Porcentual FROM
`trabajo-analitica-339815.Datos_brechas.Brecha2010` t1
INNER JOIN `trabajo-analitica-339815.Datos_brechas.Brecha2019` t2 ON t1.Region =
t2.Region
ORDER BY ((t2.Brecha_genero - t1.Brecha_genero)*100)/t1.Brecha_genero DESC;

-- 2.¿Cuál fue la brecha máxima de desocupación para cada año entre 2010-2019 y en qué región
-- se dió?
DROP TABLE IF EXISTS `trabajo-analitica-339815.Datos_brechas.Brechamax`;
CREATE TABLE `trabajo-analitica-339815.Datos_brechas.Brechamax` AS
(SELECT DISTINCT Anio, MAX(ABS(Brecha_genero)) AS Brecha_max FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Des`
WHERE Anio IN (2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019)
GROUP BY Anio);
SELECT DISTINCT t1.Anio, t2.Brecha_max, t1.Region FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Des` t1
INNER JOIN `trabajo-analitica-339815.Datos_brechas.Brechamax` t2 ON (t1.Anio = t2.Anio
AND t1.Brecha_genero = t2.Brecha_max)
ORDER BY t1.Anio;

-- 3.¿Cuáles son las tres regiones con más madres y padres adolescentes, con el respectivo rango de
-- edad en el que se encuentran?
SELECT Anio, Region, Tramos_edad, Nacidos_madres, Nacidos_padres FROM

`trabajo-analitica-339815.Datos_brechas.Brecha_Nac`
WHERE Anio = 2019
ORDER BY Nacidos_padres DESC
LIMIT 3;

-- 4.¿Cuál fue la diferencia de proporción entre la cantidad de madres adolescentes y mujeres con
-- títulos, para cada región de Chile del año 2018 al 2019?
DROP TABLE IF EXISTS `trabajo-analitica-339815.Datos_brechas.PROP2018`;
CREATE TABLE `trabajo-analitica-339815.Datos_brechas.PROP2018` AS
(SELECT t1.Region, SUM(t1.Nacidos_madres/t2.Mujeres_tituladas) AS Prop_2018 FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Nac` t1
INNER JOIN `trabajo-analitica-339815.Datos_brechas.Brecha_Tit` t2 ON (t1.Anio = t2.Anio
AND t1.Region = t2.Region)
WHERE t1.Anio = 2018
GROUP BY t1.Region);
DROP TABLE IF EXISTS `trabajo-analitica-339815.Datos_brechas.PROP2019`;
CREATE TABLE `trabajo-analitica-339815.Datos_brechas.PROP2019` AS
(SELECT t1.Region, SUM(t1.Nacidos_madres/t2.Mujeres_tituladas) AS Prop_2019 FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Nac` t1
INNER JOIN `trabajo-analitica-339815.Datos_brechas.Brecha_Tit` t2 ON (t1.Anio = t2.Anio
AND t1.Region = t2.Region)
WHERE t1.Anio = 2019
GROUP BY t1.Region);
SELECT t1.Region, ROUND(Prop_2018, 2) AS Prop2018, ROUND(Prop_2019, 2) AS
Prop2019, ROUND((Prop_2019 - Prop_2018), 3) AS Dif_Proporcion FROM
`trabajo-analitica-339815.Datos_brechas.PROP2018` t1
INNER JOIN `trabajo-analitica-339815.Datos_brechas.PROP2019` t2 ON t1.Region =
t2.Region;

-- 5.¿Cuál es la mayor tasa de desocupación que ha habido cada año entre 2010 y 2019?
DROP TABLE IF EXISTS `trabajo-analitica-339815.Datos_brechas.Brecha_TAS`;
CREATE TABLE `trabajo-analitica-339815.Datos_brechas.Brecha_TAS` AS
(SELECT Anio, MAX(Tasa_desocupacion) AS Tasa FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Des`
WHERE Anio IN (2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019)
GROUP BY Anio);
SELECT DISTINCT t1.Anio, t2.Region, t1.Tasa FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_TAS` t1
INNER JOIN `trabajo-analitica-339815.Datos_brechas.Brecha_Des` t2 ON (t1.Anio =
t2.Anio AND t1.Tasa = t2.Tasa_desocupacion)
ORDER BY Anio;

-- 6.¿En cuál de las regiones cuyo nombre inicia con ‘M’ se presentó la mayor brecha con respecto a
-- los títulos profesionales entre hombres y mujeres, y en qué año se dió?

SELECT Anio, Region, MAX(ABS(Brecha_genero)) AS Porcentaje_de_brecha FROM
trabajo-analitica-339815.Datos_brechas.Brecha_Tit
WHERE Anio IN (2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019) AND
(Region LIKE 'M%')
GROUP BY Anio, Region
ORDER BY Porcentaje_de_brecha DESC
LIMIT 1;

-- 7.¿Cuál es la región con la mayor brecha de maternidad y paternidad en el año 2019?
SELECT Anio, LOWER(Region) AS Region, Brecha FROM (SELECT Anio, Region,
MAX(ABS(Brecha_genero)) AS Brecha FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Nac`
WHERE Anio = 2019
GROUP BY Region, Anio
ORDER BY Brecha DESC
LIMIT 1);

-- 8.¿Cuál es la región con la mayor brecha de títulos en el 2019?
SELECT Anio, LPAD(Region, 15 ,'**') AS Region, Brecha FROM (SELECT Anio, Region,
MAX(ABS(Brecha_genero)) AS Brecha FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Tit`
WHERE Anio = 2019
GROUP BY Region, Anio
ORDER BY Brecha DESC
LIMIT 1);

-- 9.¿Ha habido alguna región dónde la brecha de género de titulados sea positiva?
SELECT Anio, Region, Brecha_genero FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Tit`
WHERE Brecha_genero > 0;

-- 10.¿Cuáles son los 3 mayores promedios de desocupación de todos los años por región?
SELECT Region, AVG(Brecha_genero) AS Brecha_de_desocupacion_de_genero FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Des`
WHERE Anio BETWEEN 2010 and 2019
GROUP BY Region
ORDER BY AVG(Brecha_genero) DESC
LIMIT 3;

-- 11.¿Cuál es la brecha más grande con respecto a la paternidad y maternidad en Chile?
SELECT Anio, MAX(Brecha_genero) AS Brecha_sexo FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Nac`
WHERE Anio BETWEEN 2010 and 2019
GROUP BY Anio
ORDER BY Brecha_sexo DESC
LIMIT 1;

-- 12.En la región con menor brecha de género en paternidad y maternidad, ¿Cuál es el valor de las
-- brechas de títulos y desocupación?
SELECT UPPER(t1.Region) AS region, MIN(ABS(t1.brecha_genero)) AS brecha_nac,
MIN(ABS(t2.brecha_genero)) AS brecha_tit, MIN(ABS(t3.brecha_genero)) AS brecha_des FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Nac` t1
INNER JOIN `trabajo-analitica-339815.Datos_brechas.Brecha_Tit` t2 ON (t1.Region = t2.Region
AND t1.anio = t2.anio)
INNER JOIN `trabajo-analitica-339815.Datos_brechas.Brecha_Des` t3 ON t1.Region = t3.Region
AND t1.anio = t3.anio)
WHERE t1.anio BETWEEN 2010 AND 2019
GROUP BY (t1.region)
ORDER BY brecha_nac ASC
LIMIT 1;

-- 13.Cuáles son los 5 años con menor tasa de desocupación femenina en Chile y cuál fue la cantidad
-- de títulos obtenidos por mujeres en estos años.
DROP TABLE IF EXISTS `trabajo-analitica-339815.Datos_brechas.TASADES`;

CREATE TABLE `trabajo-analitica-339815.Datos_brechas.TASADES` AS
(SELECT Anio, AVG(Tasa_des_mujeres_) AS Tasa_Des_Fem FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Des`
WHERE Anio BETWEEN 2010 AND 2019
GROUP BY Anio
ORDER BY Tasa_Des_Fem ASC);
SELECT t1.Anio, ROUND(MIN(t2.Tasa_Des_Fem), 2) AS Tasa_Des_Mujeres,
SUM(t1.Mujeres_tituladas) AS Cantidad_Tit_Mujeres FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Tit` t1
RIGHT JOIN `trabajo-analitica-339815.Datos_brechas.TASADES` t2 ON (t1.Anio = t2.Anio)
GROUP BY t1.Anio
ORDER BY Tasa_Des_Mujeres ASC
LIMIT 5;

-- 14.¿Cuál es el promedio de la tasa de desocupación del año con menor brecha de género en
maternidad y paternidad?
SELECT t1.Anio, t1.Region, MIN(ABS(t1.brecha_genero)) AS brecha_nac, AVG(t2.brecha_genero)
AS brecha_des_prom FROM `trabajo-analitica-339815.Datos_brechas.Brecha_Nac` t1
INNER JOIN `trabajo-analitica-339815.Datos_brechas.Brecha_Des` t2 ON (t1.Region =
t2.Region AND t1.anio = t2.anio)
WHERE t1.anio BETWEEN 2010 AND 2019
GROUP BY t1.anio, t1.region
ORDER BY brecha_nac ASC
LIMIT 1;

-- 15.¿Cuáles regiones tienen una tasa de desocupación mayor a 10 en algún momento de cada año?
SELECT Anio, Region, MAX(Tasa_desocupacion) AS Tasa FROM
`trabajo-analitica-339815.Datos_brechas.Brecha_Des`
WHERE Anio BETWEEN 2010 AND 2019
GROUP BY Anio, Region
HAVING MAX(Tasa_desocupacion) > 10
ORDER BY Anio ASC;