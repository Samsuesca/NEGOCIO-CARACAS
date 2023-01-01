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