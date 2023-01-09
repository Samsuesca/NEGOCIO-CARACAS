----REINICIO BASE DE DATOS
---CONFIGURAR PERMISOS CARPETA DATA:
--sudo chmod 0700 /Library/PostgreSQL/15/data
---PASAR A USUARIO POSTGRES:
--sudo su - postgres   
---Añadir comando: pg_ctl
--export PATH=$PATH:/Library/PostgreSQL/15/bin
---Ejecutar reinicio:
--pg_ctl -D /Library/PostgreSQL/15/data restart

#llaves foraneas tabla tipo_prendas:
ALTER TABLE IF EXISTS public.tipo_prendas
    ADD COLUMN id_bordados integer;

ALTER TABLE IF EXISTS public.tipo_prendas
    ADD COLUMN id_tela integer;
ALTER TABLE IF EXISTS public.tipo_prendas
    ADD CONSTRAINT tprendas_tipo_bordados_fkey FOREIGN KEY (id_bordados)
    REFERENCES public.tipo_bordados (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;

#crear tabla PRENDAS:
CREATE TABLE public.prendas
(
    id serial,
    precio numeric,
    id_tipo_prenda integer,
    talla character varying,
    CONSTRAINT prendas_pkey PRIMARY KEY (id),
    CONSTRAINT prendas_tipo_prendas_fkey FOREIGN KEY (id_tipo_prenda)
        REFERENCES public.tipo_prendas (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE IF EXISTS public.prendas
    OWNER to postgres;

-- create bordados

CREATE TABLE public.bordados
(
    id serial,
    id_prenda integer,
    cantidad numeric,
    negocio character varying,
    CONSTRAINT bordados_pkey PRIMARY KEY (id),
    CONSTRAINT bordados_prendas_fkey FOREIGN KEY (id_prenda)
        REFERENCES public.prendas (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE IF EXISTS public.bordados
    OWNER to postgres;

-- create confeccion

CREATE TABLE public.confeccion
(
    id serial,
    id_prenda integer,
    cantidad numeric,
    negocio character varying,
    CONSTRAINT confeccion_pkey PRIMARY KEY (id),
    CONSTRAINT confeccion_prendas_fkey FOREIGN KEY (id_prenda)
        REFERENCES public.prendas (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE IF EXISTS public.confeccion
    OWNER to postgres;

-- create empaque

CREATE TABLE public.empaque
(
    id serial,
    id_prenda integer,
    cantidad numeric,
    CONSTRAINT empaque_pkey PRIMARY KEY (id),
    CONSTRAINT empaque_prendas_fkey FOREIGN KEY (id_prenda)
        REFERENCES public.prendas (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE IF EXISTS public.empaque
    OWNER to postgres;

-- create inventario

CREATE TABLE public.inventario
(
    id serial,
    id_prenda integer,
    cantidad numeric,
    CONSTRAINT inventario_pkey PRIMARY KEY (id),
    CONSTRAINT inventario_prendas_fkey FOREIGN KEY (id_prenda)
        REFERENCES public.prendas (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE IF EXISTS public.inventario
    OWNER to postgres;

-- create encargos
CREATE TABLE public.encargos
(
    id serial,
    nombre_cliente character varying,
    celular numeric,
    fecha_encargo date,
    id_prenda integer,
    cantidad numeric,
    CONSTRAINT encargos_pkey PRIMARY KEY (id),
    CONSTRAINT encargos_prendas_fkey FOREIGN KEY (id_prenda)
        REFERENCES public.prendas (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE IF EXISTS public.encargos
    OWNER to postgres;

-- create encargos_to_entrega
CREATE TABLE public.encargos_to_entrega
(
    id serial,
    fecha_listo date,
    id_encargo integer,
    cantidad numeric,
    CONSTRAINT encargos_to_entrega_pkey PRIMARY KEY (id),
    CONSTRAINT encargos_to_entrega_encargo_fkey FOREIGN KEY (id_encargo)
        REFERENCES public.encargos (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE IF EXISTS public.encargos_to_entrega
    OWNER to postgres;


--LLENADO DE PRENDAS:
INSERT INTO public.prendas(
	precio, id_tipo_prenda, talla)
	VALUES (30000, 1, '6'),(31000, 1, '8'),(32000, 1, '10'),
    (33000, 1, '12'),(34000, 1, '14'),(35000,1,'16'),(36000, 1, 'S'),
    (37000, 1, 'M'),(38000, 1, 'L'),(39000, 1, 'XL'),(40000,1,'XXL');

INSERT INTO public.prendas(
	precio, id_tipo_prenda, talla)
	VALUES (30000,2,'4'),(31000, 2, '6'),(32000, 2, '8'),(33000, 2, '10'),
    (34000, 2, '12'),(35000, 2, '14'),(36000,2,'16'),(37000, 2, 'S'),
    (38000, 2, 'M'),(39000, 2, 'L'),(40000, 2, 'XL');

INSERT INTO public.prendas(
	precio, id_tipo_prenda, talla)
	VALUES (41000,3,'4'),(42000, 3, '6'),(43000, 3, '8'),(44000, 3, '10'),
    (45000, 3, '12'),(46000, 3, '14'),(47000,3,'16'),(48000, 3, 'S'),
    (49000, 3, 'M'),(50000, 3, 'L'),(51000, 3, 'XL');

INSERT INTO public.prendas(
	precio, id_tipo_prenda, talla)
	VALUES (41000,4,'4'),(42000, 4, '6'),(43000, 4, '8'),(44000, 4, '10'),
    (45000, 4, '12'),(46000, 4, '14'),(47000,4,'16'),(48000, 4, 'S'),
    (49000, 4, 'M'),(50000, 4, 'L'),(51000, 4, 'XL');

INSERT INTO public.prendas(
	precio, id_tipo_prenda, talla)
	VALUES (80000, 5, '6'),(85000, 5, '8'),(90000, 5, '10'),
    (95000, 5, '12'),(100000, 5, '14'),(105000,5,'16'),(110000, 5, 'S'),
    (115000, 5, 'M'),(120000, 5, 'L'),(120000, 5, 'XL');

INSERT INTO public.prendas(
	precio, id_tipo_prenda, talla)
	VALUES (13000, 7, '6'),(13000, 7, '8'),(13000, 7, '113000'),
    (13000, 7, '12'),(13000, 7, '14'),(13000,7,'16'),(15000, 7, 'S'),
    (15000, 7, 'M'),(15000, 7, 'L'),(15000, 7, 'XL');

INSERT INTO public.prendas(
	precio, id_tipo_prenda, talla)
	VALUES (9000, 8, '6-8'),(9000, 8, '8-10'),(9000, 8, '9-11');

INSERT INTO public.prendas(
	precio, id_tipo_prenda, talla)
	VALUES (0, 6, 'B27-32'),(0, 6, 'B33-38'),(0, 6, 'B39-44'),
    (0, 6, 'G27-32'),(0, 6, 'G33-38'),(0, 6, 'G39-44'),
    (0, 6, 'N27-32'),(0, 6, 'N33-38'),(0, 6, 'N39-44');

INSERT INTO public.prendas(
	precio, id_tipo_prenda, talla)
	VALUES (33000, 9, '6'),(33000, 9, '8'),(33000, 9, '10'),
    (35000, 9, '12'),(35000, 9, '14'),(35000,9,'16'),(40000, 9, '28'),
    (40000, 9, '30'),(40000, 9, '32'),(40000, 9, '34');

--LLENADO DE INVENTARIOS:
INSERT INTO inventario(id_prenda,cantidad)
    VALUES (1,26),(2,15),(3,11),(4,55),(5,14),(6,32),(7,0),(8,6),(9,0),(10,0),(11,0),
    (12,2),(13,9),(14,4),(15,1),(16,3),(17,6),(18,19),(19,6),(20,1),(21,0),(22,1),
    (23,2),(24,1),(25,3),(26,1),(27,0),(28,0),(29,0),(30,0),(31,0),(32,0),(33,0),
    (34,1),(35,0),(36,3),(37,1),(38,0),(39,0),(40,0),(41,0),(42,0),(43,0),(44,0),
    (55,6),(56,9),(57,11),(58,11),(59,11),(60,6),(61,2),(62,1),(63,1),(64,0),(65,12),
    (66,12),(66,12),(77,8),(78,6),(79,9),(80,5),(81,7),(82,10),(83,2),(84,0),(85,0),(86,2);




--VER INVENTARIO:
CREATE VIEW total AS
SELECT prendas.id, tipo_prendas.name, prendas.talla, prendas.precio, inventario.cantidad
FROM prendas
JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
JOIN inventario ON prendas.id = inventario.id_prenda;

--VER INVENTARIO CAMISETAS:
SELECT * FROM camisetas;
CREATE VIEW camisetas AS
SELECT prendas.id, tipo_prendas.name, prendas.talla, prendas.precio, inventario.cantidad
FROM prendas
JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
JOIN inventario ON prendas.id = inventario.id_prenda
WHERE prendas.id BETWEEN 1 AND 11;

--VER INVENTARIO SUDADERAS:
SELECT * FROM sudaderas;
CREATE VIEW sudaderas AS
SELECT prendas.id, tipo_prendas.name, prendas.talla, prendas.precio, inventario.cantidad
FROM prendas
JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
JOIN inventario ON prendas.id = inventario.id_prenda
WHERE prendas.id BETWEEN 12 AND 22;

--VER INVENTARIO CHAZUL:
SELECT * FROM chazul;
CREATE VIEW chazul AS
SELECT prendas.id, tipo_prendas.name, prendas.talla, prendas.precio, inventario.cantidad
FROM prendas
JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
JOIN inventario ON prendas.id = inventario.id_prenda
WHERE prendas.id BETWEEN 23 AND 33;

--VER INVENTARIO medias:
SELECT * FROM medias;
CREATE VIEW medias AS
SELECT prendas.id, tipo_prendas.name, prendas.talla, prendas.precio, inventario.cantidad
FROM prendas
JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
JOIN inventario ON prendas.id = inventario.id_prenda
WHERE prendas.id BETWEEN 65 AND 67;

--VER INVENTARIO CHGRIS:
SELECT * FROM chgris;
CREATE VIEW chgris AS
SELECT prendas.id, tipo_prendas.name, prendas.talla, prendas.precio, inventario.cantidad
FROM prendas
JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
JOIN inventario ON prendas.id = inventario.id_prenda
WHERE prendas.id BETWEEN 34 AND 44;

--VER INVENTARIO BLUSAS:
SELECT * FROM blusas;
CREATE VIEW blusas AS
SELECT prendas.id, tipo_prendas.name, prendas.talla, prendas.precio, inventario.cantidad
FROM prendas
JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
JOIN inventario ON prendas.id = inventario.id_prenda
WHERE prendas.id BETWEEN 55 AND 64;

--VER INVENTARIO JEANS:
SELECT * FROM jeans;
CREATE VIEW jeans AS
SELECT prendas.id, tipo_prendas.name, prendas.talla, prendas.precio, inventario.cantidad
FROM prendas
JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
JOIN inventario ON prendas.id = inventario.id_prenda
WHERE prendas.id BETWEEN 77 AND 86;

--CREAR TABLA DE DETALLES DE VENTA:



--CREAR TABLA DE VENTAS:
CREATE TABLE ventas (
    id serial PRIMARY KEY,
    id_cliente integer NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total numeric NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE  
);

CREATE TABLE detalle_venta (
    id serial PRIMARY KEY,
    id_venta integer NOT NULL,
    id_prenda integer NOT NULL,
    cantidad integer NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas (id)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_prenda) REFERENCES prendas (id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

INSERT INTO public.detalle_venta (id_venta,id_prenda,cantidad)
VALUES ((SELECT id FROM ventas WHERE id_cliente = (SELECT id FROM clientes WHERE nombre = 'Manolo')),22,1);

