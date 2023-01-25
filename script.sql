----REINICIO BASE DE DATOS
---CONFIGURAR PERMISOS CARPETA DATA:
--sudo chmod 0700 /Library/PostgreSQL/15/data
---PASAR A USUARIO POSTGRES:
--sudo su - postgres   
---Añadir comando: pg_ctl
--export PATH=$PATH:/Library/PostgreSQL/15/bin
---Ejecutar reinicio:
--pg_ctl -D /Library/PostgreSQL/15/data restart

---Delete clientes que no tienen encargos ni ventas:
DELETE FROM clientes
WHERE NOT EXISTS (SELECT * FROM encargos WHERE encargos.id_cliente = clientes.id)
AND NOT EXISTS (SELECT * FROM ventas WHERE ventas.id_cliente = clientes.id)
AND NOT EXISTS (SELECT * FROM cambios WHERE cambios.id_cliente = clientes.id) ;


---query
(SELECT clientes.nombre AS "Nombre del cliente",
                        ventas.id AS "ID",
                        ventas.fecha AS "Fecha",
                        tipo_prendas.name AS "Nombre de la prenda",
                        prendas.talla AS "Talla",
                        prendas.precio AS "Precio",
                        detalle_venta.cantidad AS "Cantidad",
                        (prendas.precio * detalle_venta.cantidad) AS "Total parcial por prenda",
                        ventas.total AS "Total de la Venta",
                        detalle_venta.id AS "ID_DETALLE"
                        FROM clientes
                        JOIN ventas ON clientes.id = ventas.id_cliente
                        JOIN detalle_venta ON ventas.id = detalle_venta.id_venta
                        JOIN prendas ON detalle_venta.id_prenda = prendas.id
                        JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
                        WHERE ventas.id = 37
                        ORDER BY detalle_venta.id;)


#vista encargos yombers:
CREATE VIEW yombers_encargados AS 
SELECT clientes.nombre AS "Cliente", clientes.telefono AS "Teléfono",  yombers.nombre_nina AS "Niña",
prendas.talla, yombers.delantero AS "D", yombers.trasero AS "T", yombers.espalda AS "E",
 yombers.cintura AS "C", yombers.largo AS "L", encargos.fecha_encargo AS "Encargado el:", encargos.fecha_entrega AS "Para entregar el:", encargos.saldo AS "SALDO"
FROM encargos
JOIN detalle_encargo ON encargos.id = detalle_encargo.id_encargo
JOIN prendas ON detalle_encargo.id_prenda = prendas.id
JOIN clientes ON encargos.id_cliente = clientes.id
JOIN yombers ON encargos.id = yombers.id_encargo
WHERE encargos.entregado = FALSE;


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

--VER INVENTARIO OTROS:
SELECT * FROM otros;
CREATE VIEW otros AS
SELECT prendas.id, tipo_prendas.name, prendas.talla, prendas.precio, inventario.cantidad
FROM prendas
JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
JOIN inventario ON prendas.id = inventario.id_prenda
WHERE prendas.id BETWEEN 87 AND 89;


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

--VER INVENTARIO yomber:
SELECT * FROM yomber;
CREATE VIEW yomber AS
SELECT prendas.id, tipo_prendas.name, prendas.talla, prendas.precio, inventario.cantidad
FROM prendas
JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
JOIN inventario ON prendas.id = inventario.id_prenda
WHERE prendas.id BETWEEN 45 AND 54;

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

--crear tabla movimientos
CREATE TABLE movimientos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT NOW()
);

--function trigger para llevar ventas a registros



CREATE OR REPLACE FUNCTION agregar_movimiento_venta()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.finalizada = TRUE THEN
        -- Registro de venta en la tabla de movimientos
        INSERT INTO movimientos (tipo, descripcion, monto, fecha)
        VALUES ('Venta', 'Ingreso Venta', NEW.total, NOW());

        INSERT INTO movimientos (tipo,fecha, descripcion, monto)
        SELECT 'Venta',NOW(), 'Comisión por venta', -5000 * SUM(CASE WHEN id_prenda BETWEEN 1 AND 54 THEN cantidad ELSE 0 END)
        FROM detalle_venta
        WHERE id_venta = NEW.id;

    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--crear trigger de la funcion
CREATE TRIGGER agregar_movimiento
AFTER UPDATE OF finalizada ON ventas
FOR EACH ROW
EXECUTE FUNCTION agregar_movimiento_venta();

--tabla encargo TRIGGERS
CREATE OR REPLACE FUNCTION saldo()
RETURNS TRIGGER AS $$
BEGIN
	NEW.saldo := NEW.total - NEW.abono;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_saldo
AFTER INSERT OR UPDATE OF total,abono
ON encargos
FOR EACH ROW
EXECUTE FUNCTION saldo()

CREATE OR REPLACE FUNCTION update_fecha_entrega()
RETURNS TRIGGER AS $$
BEGIN 
    NEW.fecha_entrega := NEW.fecha_encargo + INTERVAL '1 day'*NEW.dias_entrega;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER actualizar_fecha_entrega
AFTER INSERT OR UPDATE OF dias_entrega,fecha_encargo
ON encargos
FOR EACH ROW
EXECUTE FUNCTION update_fecha_entrega();




--tabla gastos
CREATE TABLE gastos_uniformes (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP NOT NULL DEFAULT NOW(),
    descripcion VARCHAR(255) NOT NULL,
    monto NUMERIC(10, 2) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    detalles VARCHAR(255)
);

--funcion agregar gasto
CREATE OR REPLACE FUNCTION agregar_movimiento_gasto()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO movimientos (fecha, descripcion, monto, tipo)
    VALUES (NEW.fecha, 'Gasto: ' || NEW.descripcion, NEW.monto*-1, 'Gasto');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--trigger agregar gasto
CREATE TRIGGER agregar_movimiento_gasto
AFTER INSERT ON gastos_uniformes
FOR EACH ROW
EXECUTE FUNCTION agregar_movimiento_gasto();


--cuentas por cobrar:
CREATE TABLE cuentas_por_pagar (
    id SERIAL PRIMARY KEY,
    prestamista VARCHAR(255) NOT NULL,
    concepto VARCHAR(255) NOT NULL,
    fecha_compra DATE NOT NULL,
    fecha_pago DATE NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    interes_men DECIMAL(10,2) NOT NULL,
    pagado BOOLEAN DEFAULT FALSE
);

----DIADIOIOASDJISA 
ALTER TABLE detalle_venta
    DROP CONSTRAINT detalle_venta_id_venta_fkey,
    ADD CONSTRAINT detalle_venta_id_venta_fkey
    FOREIGN KEY (id_venta)
    REFERENCES ventas (id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

CREATE TRIGGER guardar_dv_copy
AFTER DELETE ON detalle_venta
FOR EACH ROW
BEGIN
    INSERT INTO detalle_venta_copy
    SELECT * FROM deleted;
END;

select * from detalle_venta_copy;

CREATE OR REPLACE FUNCTION copiar_detalle_venta_eliminado()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO detalle_venta_copy SELECT * FROM detalle_venta WHERE detalle_venta.id = OLD.id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER copia_dv_eliminado
    BEFORE DELETE ON detalle_venta
    FOR EACH ROW
    EXECUTE FUNCTION copiar_detalle_venta_eliminado();

---- CAMBIOS 
CREATE TABLE detalle_cambio (
id SERIAL PRIMARY KEY,	
id_cambio INTEGER REFERENCES cambios (id) ON DELETE CASCADE ON UPDATE CASCADE,
id_prenda_entrante INTEGER REFERENCES prendas(id) ON DELETE CASCADE ON UPDATE CASCADE,
id_prenda_saliente INTEGER REFERENCES prendas(id) ON DELETE CASCADE ON UPDATE CASCADE,
cantidad_entrante INTEGER,
cantidad_saliente INTEGER
);


CREATE FUNCTION actualizar_cambio()
RETURNS TRIGGER AS $$
BEGIN
	UPDATE cambios
    SET total_entrada = total_entrada + (SELECT prendas.precio FROM prendas WHERE prendas.id = NEW.id_prenda_entrante) * NEW.cantidad_entrante,
        total_salida = total_salida + (SELECT prendas.precio FROM prendas WHERE prendas.id = NEW.id_prenda_saliente) * NEW.cantidad_saliente
    WHERE id = NEW.id_cambio;

    -- Actualizar el inventario al hacer un cambio
    UPDATE inventario
    SET cantidad = cantidad + NEW.cantidad_entrante - NEW.cantidad_saliente
    WHERE id_prenda = NEW.id_prenda_entrante OR id_prenda = NEW.id_prenda_saliente;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER actualizar_totales_cambio
AFTER INSERT ON detalle_cambio
FOR EACH ROW
EXECUTE FUNCTION actualizar_cambio();
